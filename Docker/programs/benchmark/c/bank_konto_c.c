#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <string.h>
#include <math.h>

typedef struct {
  long int state;
  long int a;
  long int c;
  long int m;
} LCG;

long int LCG_hash_seed(const char *input_str) {
  long int prime = 31;
  long int checksum = 0;

  while (*input_str != '\0') {
    checksum = (checksum * prime + *input_str) & 0xFFFFFFFF;
    input_str++;
  }
  return checksum;
}

void LCG_init(LCG *generator, const char *seed) {
  generator->state = LCG_hash_seed(seed);
  generator->a = 1664525;
  generator->c = 1013904223;
  generator->m = 1294967296;
}

long int LCG_next(LCG *generator) {
  generator->state = (generator->a * generator->state + generator->c) % generator->m;
  return generator->state;
}

float LCG_random(LCG *generator) {
  return (float)LCG_next(generator) / generator->m;
}

long int get_next_number(LCG *generator, int n) {
  return floor(LCG_random(generator) * n);
}

long int get_next_number_between(LCG *generator, int n, int m) {
  return floor((LCG_random(generator) * (m - n)) + n);
}

int numDigits(unsigned long int num) {
  int digits = 0;
  do {
    digits++;
    num /= 10;
  } while (num != 0);
  return digits;
}


typedef struct {
  int *accounts;
  int *initial_accounts;
  pthread_mutex_t lock;
  int num_accounts;
  LCG random_generator;
} BankServer;

void BankServer_init(BankServer *server, int num_accounts, int min_starting_balance, int max_starting_balance, unsigned long seed) {

  char seed_string[4];
  snprintf(seed_string, sizeof(seed_string), "%ld", seed);
  
  LCG_init(&server->random_generator, seed_string);
  server->accounts = (int *)malloc(num_accounts * sizeof(int));
  server->initial_accounts = (int *)malloc(num_accounts * sizeof(int));
  server->num_accounts = num_accounts;
  pthread_mutex_init(&server->lock, NULL);
  for (int i = 0; i < num_accounts; i++) {
    server->initial_accounts[i] = get_next_number_between(&server->random_generator, min_starting_balance, max_starting_balance);
    server->accounts[i] = server->initial_accounts[i];
  }
}


void BankServer_transfer(BankServer *server, int from_account, int to_account, int amount) {
  pthread_mutex_lock(&server->lock);
  if (1 <= from_account && from_account <= server->num_accounts && 1 <= to_account && to_account <= server->num_accounts && from_account != to_account) {
    if (server->accounts[from_account - 1] >= amount) {
      server->accounts[from_account - 1] -= amount;
      server->accounts[to_account - 1] += amount;
    }
  }
  pthread_mutex_unlock(&server->lock);
}

char *BankServer_accounts_to_string(BankServer *server) {
  pthread_mutex_lock(&server->lock);
  int total_balance_end = 0;
  int total_balance_start = 0;

  for (int i = 0; i < server->num_accounts; i++) {
    total_balance_start += server->initial_accounts[i];
    total_balance_end += server->accounts[i];
  }

  // Calculate the length of the string
  int length = snprintf(NULL, 0, "[%d, %d", total_balance_start, total_balance_end);
  for (int i = 0; i < server->num_accounts; i++) {
    length += snprintf(NULL, 0, ", %d, %d", server->initial_accounts[i], server->accounts[i]);
  }
  length += 2; // for the ']' and '\0'

  // Allocate memory for the string
  char *result_string = (char *)malloc((length + 1) * sizeof(char)); // Add 1 for the null terminator
  if (result_string == NULL) {
    pthread_mutex_unlock(&server->lock);
    return NULL; // Allocation failed
  }

  // Construct the string
  snprintf(result_string, length + 1, "[%d, %d", total_balance_start, total_balance_end);
  for (int i = 0; i < server->num_accounts; i++) {
    snprintf(result_string + strlen(result_string), length - strlen(result_string), ", %d, %d", server->initial_accounts[i], server->accounts[i]);
  }
  strcat(result_string, "]");

  pthread_mutex_unlock(&server->lock);
  return result_string;
}

typedef struct {
  BankServer *server;
  int num_accounts;
  int min_transfer_amount;
  int max_transfer_amount;
  int num_operations;
  LCG random_generator;
} BankClientArgs;

void *BankClient_run_operations(void *args) {
  BankClientArgs *client_args = (BankClientArgs *)args;
  for (int i = 0; i < client_args->num_operations; i++) {
    int k1 = get_next_number(&client_args->random_generator, client_args->num_accounts) + 1;
    int k2 = get_next_number(&client_args->random_generator, client_args->num_accounts) + 1;
    int amount = get_next_number_between(&client_args->random_generator, client_args->min_transfer_amount, client_args->max_transfer_amount);
    BankServer_transfer(client_args->server, k1, k2, amount);
  }
  return NULL;
}

void run_simulation(int num_accounts, int num_clients, int num_operations, const char *seed, int min_starting_balance, int max_starting_balance, int min_transfer_amount, int max_transfer_amount) {
  LCG random_generator;
  LCG_init(&random_generator, seed);
    
  BankServer server;
  BankServer_init(&server, num_accounts, min_starting_balance, max_starting_balance, get_next_number(&random_generator, 1000));


  pthread_t threads[num_clients];
  BankClientArgs client_args[num_clients];

  for (int i = 0; i < num_clients; i++) {
    char seed_string[4];
    snprintf(seed_string, sizeof(seed_string), "%ld", get_next_number(&random_generator, 1000));
    LCG_init(&client_args[i].random_generator, seed_string);

    client_args[i].num_accounts = num_accounts;
    client_args[i].min_transfer_amount = min_transfer_amount;
    client_args[i].max_transfer_amount = max_transfer_amount;
    client_args[i].num_operations = num_operations;
    client_args[i].server = &server;
    pthread_create(&threads[i], NULL, BankClient_run_operations, (void *)&client_args[i]);
  }

  for (int i = 0; i < num_clients; i++) {
    pthread_join(threads[i], NULL);
  }

  char *result = BankServer_accounts_to_string(&server);
  printf("%s\n", result);
  free(result);
  free(server.accounts);
  free(server.initial_accounts);
}

int main(int argc, char *argv[]) {
  if (argc != 9) {
    printf("Wrong number of arguments!\n");
    return 1;
  }

  int num_accounts = atoi(argv[2]);
  int num_clients = atoi(argv[7]);
  int num_operations = atoi(argv[8]);
  const char *seed = argv[1];
  int min_starting_balance = atoi(argv[3]);
  int max_starting_balance = atoi(argv[4]);
  int min_transfer_amount = atoi(argv[5]);
  int max_transfer_amount = atoi(argv[6]);

  run_simulation(num_accounts, num_clients, num_operations, seed, min_starting_balance, max_starting_balance, min_transfer_amount, max_transfer_amount);

  return 0;
}

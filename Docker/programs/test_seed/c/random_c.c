#include <stdio.h>
#include <stdlib.h>
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

long int get_next_number(LCG *generator,  int n) {
  return floor(LCG_random(generator) * n);
}

long int get_next_number_between(LCG *generator, int n, int m) {
  return floor((LCG_random(generator) * (m-n))+n);
}

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: %s <seed>\n", argv[0]);
        return 1;
    }

    const char *seed_string = argv[1];
    LCG generator;
    LCG_init(&generator, seed_string);

    for (int i = 0; i < 5; i++) {
      printf("%lu", get_next_number(&generator,100));
        if (i < 4) {
            printf(", ");
        }
    }
    printf("\n");

    return 0;
}

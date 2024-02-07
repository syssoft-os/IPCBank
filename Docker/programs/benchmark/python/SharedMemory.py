import multiprocessing
import copy
import sys

from LCG import LCG


class BankServer:
    def __init__(self, num_accounts, min_starting_balance, max_starting_balance, seed):
        self.random_generator = LCG(str(seed))
        self.initial_accounts = {
            i + 1: self.random_generator.get_next_number_between(min_starting_balance, max_starting_balance) for i in
            range(num_accounts)}
        self.accounts = copy.deepcopy(self.initial_accounts)
        self.lock = multiprocessing.Lock()
        self.num_accounts = num_accounts

    def transfer(self, from_account, to_account, amount):
        with self.lock:
            if 1 <= from_account <= len(self.accounts) and 1 <= to_account <= len(self.accounts):
                if self.accounts[from_account] >= amount:
                    self.accounts[from_account] -= amount
                    self.accounts[to_account] += amount

    def accounts_to_string(self):
        with self.lock:
            total_balance_end = sum(self.accounts.values())
            total_balance_start = sum(self.initial_accounts.values())

            accounts_balance = []

            accounts_balance.extend([total_balance_start, total_balance_end])

            for key in sorted(set(self.accounts.keys()) & set(self.initial_accounts.keys())):
                accounts_balance.extend([self.initial_accounts[key], self.accounts[key]])

            result_string = "[" + ", ".join(map(str, accounts_balance)) + "]"
            return result_string


def print_array_elements(array, n):
    print(f"[{', '.join(map(str, array[:n]))}]")

def run_server(shm, num_accounts, min_starting_balance, max_starting_balance, seed, num_clients):
    server = BankServer(num_accounts, min_starting_balance, max_starting_balance, seed)

    finished_clients = 0
    transaction_counter = 0
    while finished_clients < num_clients:
        finished_clients = 0
        for i in range(num_clients):
            if shm[i] == 1:
                start_index = ((i*3) + num_clients)
                k1, k2, amount = shm[start_index:start_index+3]

                server.transfer(k1, k2, amount)
                transaction_counter += 1
                shm[i] = 0
            if shm[i] == -1:
                finished_clients += 1

    print(server.accounts_to_string())


def run_client(shm, num_operations, num_accounts, min_transfer_amount, max_transfer_amount, seed, id, num_clients):
    random_generator = LCG(str(seed))

    client_index = (id * 3) + num_clients
    counter = 0
    while counter <= num_operations:
        if shm[id] == 0:
            shm[client_index] = random_generator.get_next_number(num_accounts) + 1
            shm[client_index+1] = random_generator.get_next_number(num_accounts) + 1
            shm[client_index+2] = random_generator.get_next_number_between(min_transfer_amount, max_transfer_amount)
            shm[id] = 1
            counter += 1

    shm[id] = -1


if __name__ == "__main__":
    if len(sys.argv) != 9:
        print("Wrong number of arguments!")
        sys.exit(1)

    num_accounts = int(sys.argv[2])
    num_clients = int(sys.argv[7])
    num_operations = int(sys.argv[8])
    seed = sys.argv[1]
    min_starting_balance = int(sys.argv[3])
    max_starting_balance = int(sys.argv[4])
    min_transfer_amount = int(sys.argv[5])
    max_transfer_amount = int(sys.argv[6])

    random_generator = LCG(seed)
    shm = multiprocessing.Array('i', [0] * ((num_clients * 3) + num_clients))


    server_process = multiprocessing.Process(target=run_server, args=(shm, num_accounts, min_starting_balance, max_starting_balance, random_generator.get_next_number(1000), num_clients))
    server_process.start()

    client_processes = [
        multiprocessing.Process(
            target=run_client,
            args=(shm, num_operations, num_accounts, min_transfer_amount, max_transfer_amount,
                  random_generator.get_next_number(1000), i, num_clients)
        )
        for i in range(num_clients)
    ]

    for process in client_processes:
        process.start()

    for process in client_processes:
        process.join()

    server_process.join()

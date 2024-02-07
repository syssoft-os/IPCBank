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


def run_server(pipe, num_accounts, min_starting_balance, max_starting_balance, seed):
    server = BankServer(num_accounts, min_starting_balance, max_starting_balance, seed)
    while True:
        data = pipe.recv()
        if data == "STOP":
            print(server.accounts_to_string())
            break
        k1, k2, amount = data
        server.transfer(k1, k2, amount)
    pipe.close()


def run_client(pipe, num_operations, num_accounts, min_transfer_amount, max_transfer_amount, seed):
    random_generator = LCG(str(seed))

    for _ in range(num_operations):
        k1 = random_generator.get_next_number(num_accounts) + 1
        k2 = random_generator.get_next_number(num_accounts) + 1
        amount = random_generator.get_next_number_between(min_transfer_amount, max_transfer_amount)
        pipe.send((k1, k2, amount))


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
    client_pipe, server_pipe = multiprocessing.Pipe()

    server_process = multiprocessing.Process(target=run_server, args=(server_pipe, num_accounts, min_starting_balance, max_starting_balance, random_generator.get_next_number(1000)))
    server_process.start()

    client_processes = [multiprocessing.Process(target=run_client, args=(client_pipe, num_operations, num_accounts, min_transfer_amount, max_transfer_amount, random_generator.get_next_number(1000))) for _ in range(num_clients)]

    for process in client_processes:
        process.start()

    for process in client_processes:
        process.join()

    client_pipe.send("STOP")

    server_process.join()


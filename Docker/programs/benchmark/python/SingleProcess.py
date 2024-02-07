import sys
import threading
import copy
from LCG import LCG


class BankServer:
    def __init__(self, num_accounts, min_starting_balance, max_starting_balance, seed):
        self.random_generator = LCG(str(seed))
        self.initial_accounts = {i + 1: self.random_generator.get_next_number_between(min_starting_balance, max_starting_balance) for i in range(num_accounts)}
        self.accounts = copy.deepcopy(self.initial_accounts)
        self.lock = threading.Lock()

    def transfer(self, from_account, to_account, amount):
        with self.lock:
            if 1 <= from_account <= len(self.accounts) and 1 <= to_account <= len(self.accounts) and from_account != to_account:
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


class BankClient:
    def __init__(self, server, num_operations, min_transfer_amount, max_transfer_amount, seed):
        self.server = server
        self.num_operations = num_operations
        self.min_transfer_amount = min_transfer_amount
        self.max_transfer_amount = max_transfer_amount
        self.random_generator = LCG(str(seed))

    def run_operations(self):
        for _ in range(self.num_operations):
            k1 = self.random_generator.get_next_number(len(self.server.accounts)) + 1
            k2 = self.random_generator.get_next_number(len(self.server.accounts)) + 1
            amount = self.random_generator.get_next_number_between(self.min_transfer_amount, self.max_transfer_amount)
            self.server.transfer(k1, k2, amount)

def run_simulation(num_accounts, num_clients, num_operations, seed, min_starting_balance, max_starting_balance,
                   min_transfer_amount, max_transfer_amount):
    random_generator = LCG(seed)

    server = BankServer(num_accounts, min_starting_balance, max_starting_balance, random_generator.get_next_number(1000))
    clients = [BankClient(server, num_operations, min_transfer_amount, max_transfer_amount, random_generator.get_next_number(1000)) for _ in range(num_clients)]

    threads = [threading.Thread(target=client.run_operations) for client in clients]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()

    print(server.accounts_to_string())

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

    run_simulation(num_accounts, num_clients, num_operations, seed, min_starting_balance, max_starting_balance,
                   min_transfer_amount, max_transfer_amount)

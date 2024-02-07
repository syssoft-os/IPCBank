import sys
import random
import math
import time


class LCG:
    def __init__(self, seed):
        self.state = self.__hash_seed(seed)
        self.a = 1664525
        self.c = 1013904223
        self.m = 1294967296

    def __next(self):
        self.state = (self.a * self.state + self.c) % self.m
        return self.state

    def random(self):
        return self.__next() / float(self.m)

    def get_next_number(self,n):
        return math.floor(self.random() * n)

    def get_next_number_between(self,n,m):
        return math.floor(self.random() * (m-n))+n

    def __hash_seed(self,input_str):
        prime = 31
        checksum = 0

        for char in input_str:
            checksum = (checksum * prime + ord(char)) & 0xFFFFFFFF

        return checksum


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: {} <seed>".format(sys.argv[0]))
        sys.exit(1)

    seed_string = sys.argv[1]
    generator = LCG(seed_string)
    numbers = [generator.get_next_number(10000) for _ in range(2)]
    numbers += [generator.get_next_number(100) for _ in range(1000)]

    time.sleep(1)

    
    print("[",", ".join(map(str, numbers)),"]")

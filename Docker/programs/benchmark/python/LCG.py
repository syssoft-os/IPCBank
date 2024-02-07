import math

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
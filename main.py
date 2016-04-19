import math

class BaseExponentPair:
    def __init__(self, line):
        self.base, self.exponent = map(int, line.split(","))
        self.logvalue = self.exponent * math.log(self.base)

    def __gt__(self, pair):
        return self.logvalue > pair.logvalue

    def __str__(self):
        return "{},{}".format(self.base, self.exponent)

with open("number_pairs.txt", "r") as f:
    print(max([BaseExponentPair(line) for line in f]))

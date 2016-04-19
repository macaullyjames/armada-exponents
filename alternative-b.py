from math import log

with open("number_pairs.txt", "r") as f:
    pairs = [list(map(int, line.split(","))) for line in f]
    base, exponent = max(pairs, key=lambda p: p[1]*log(p[0]))
    print("{},{}".format(base, exponent))

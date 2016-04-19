import math

with open("number_pairs.txt", "r") as f:
    max_base, max_exponent, max_log = 0, 0, float("-inf")
    for line in f:
        base, exponent = map(int, line.split(","))
        log = exponent * math.log(base)
        if log > max_log:
            max_base, max_exponent, max_log = base, exponent, log

    print("{},{}".format(max_base, max_exponent))

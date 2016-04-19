# armada-exponents
Solutions from a small programming challenge for an interview with [THS Armada](http://armada.nu).

## Challenge description
> Hello,
>
> As part of the interview, we've prepared a pre-interview programming exercise/question:
> Its quite easy to confirm that 2<sup>6</sup> > 5<sup>2</sup> with a calculator. Confirming that 667687<sup>515964</sup> > 636119<sup>517834</sup> is not as easy, since each number is over a million digits long.
>
> Attached to this email is a .txt file with 1000 pairs of positive numbers, on the form: base,exponent
>
> Which base<sup>exponent</sup> pair is the largest?
>
> You can use whatever programming language and libraries you want to solve this. We're currently using Python 3 for our next CRM system, so if you wanted some extra style points, you can use that.

The attached file can be found at [number_pairs.txt](number_pairs.txt).

## Math stuff
The logarithm is a monotonic function, which means that

    a > b <=> log(a) > log(b)

which in turn means that

    x = max([a0, ..., an]) <=> log(x) = max([log(a0), ..., log(an)])
    
so instead of finding `max([a0, ..., an])` directly, we can focus on finding `max([log(a0), ..., log(an)])` which should be a bit easier to compute. In fact, it's a lot easier to compute because we know that

    log(b^e) = e * log(b)

so for a list of base/exponent pairs `[b0^e0, ..., bn^en]` we have that

    bi^ei = max([b0^e0, ..., bn^en]) <=> ei * log(bi) = max([e0 * log(b0), ..., en * log(bn)])

so it is simply a case of finding the base/exponent pair that maximises the expression `exponent * log(base)`. This is computationally feasible, at least if all bases and exponents are integers less than `sys.maxsize`.

## Solutions
Disclaimer: I am not a Python developer.

### First attempt ([alternative-a.py](alternative-a.py))
```Python
import math

with open("number_pairs.txt", "r") as f:
    max_base, max_exponent, max_log = 0, 0, float("-inf")
    for line in f:
        base, exponent = map(int, line.split(","))
        log = exponent * math.log(base)
        if log > max_log:
            max_base, max_exponent, max_log = base, exponent, log

    print("{},{}".format(max_base, max_exponent))
```
I liked this solution for its clarity and the fact that it scales well; only two base/exponent pairs need be in memory at the same time. It is a bit ugly though and doesn't feel very "pythonic", more like a C++ dev trying to write Python for the first time. It's quite verbose as well, and I'm not a fan of reassigning variables; the names `max_exponent` and so on aren't actually semantic until the end of the loop. This makes me sad.

### Second attempt ([alternative-b.py](alternative-b.py))
```Python
from math import log

with open("number_pairs.txt", "r") as f:
    pairs = [list(map(int, line.split(","))) for line in f]
    base, exponent = max(pairs, key=lambda p: p[1]*log(p[0]))
    print("{},{}".format(base, exponent))
```
This felt slightly more pythonic, but is waaay too terse. Figuring out what the `pairs` variable contains is a non-trivial task. `p[0]` and `p[1]` don't make for great variable names either, especially when squashed in a lambda. To be honest I'd have a hard time figuring out what this does if I hadn't written it myself. Not good.

### Final attempt ([main.py](main.py))
```Python
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
```
I'm actually really happy with this solution. It's simple, semantic and feels very pythonic; by overriding the `gt` and `str` methods we're can use the standard library the way it's supposed to be used. Of course, in production code I'd override the other comparison operators (`eq`, `lt` etc.) but for the sake of brevity I didn't do that here.

Hope you like it :)

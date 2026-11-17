# Solution: Exercises Syntax

## Task 02

```python
ects = 2
n_lectures = 14
n_exercises = 12
h_per_lecture = 1
h_per_ects = 27.5

workload = ects * h_per_ects
h_per_exercise = (workload - n_lectures * h_per_lecture) / n_exercises
# 3.42 h/ex


def hours_per_exercise(
    approach='minimalistic', ects=2, h_per_lecture=1, n_lectures=14, n_exercises=12
):
    if approach == 'minimalistic':
        h_per_ects = 25
    elif approach == 'maximalistic':
        h_per_ects = 30
    else:
        raise ValueError("approach must be 'minimalistic' or 'maximalistic'")

    workload = ects * h_per_ects
    hours = (workload - n_lectures * h_per_lecture) / n_exercises

    return hours


print(hours_per_exercise('minimalistic'), hours_per_exercise('maximalistic'))
# 3.0 3.8333333333333335
```

## Task 03

```python
import time


def no_op():
    return


class Numbers:
    def __init__(self):
        self.cannonical = (1, 1j)
        self.primes = [2, 3, 5, 7, 11, 13, 17]
        self.named = dict(c=299792458, h=6.626e-34)
        self.favourites = set([666, 1312, 1337])
        self.answer = 'fourtytwo'


primes = []
candidate = 2

start_time = time.time()
while time.time() - start_time <= 10:
    if all([candidate % i for i in range(2, candidate)]):
        primes.append(candidate)
    candidate += 1


# This is True
((no_op() is None) is True) is not False

# This is two
expression = 1 + 1 - 1 * 1 / 1**1 % 1 // 1


if 0 > 1 >= 2 != 3 == 4:
    print('fyi, you can stack comparison operations')
elif 6.022e23 in primes[0:10:2]:
    print('thanks for all the fish.')
else:
    pass
```

## Task 04

```python
elements = (
    '=',
    'int', 'float', 'complex',
    '+', '-', '/', '*', '**', '%', '//',
    'True', 'False', 'None',
    '==', '!=', '<', '<=', '>', '>=',
    'and', 'or', 'not',
    'if', 'elif', 'else',
    'list', 'dict', 'set', 'tuple', 'str',
    'class',
    'def',
    'import',
    'for', 'while',
    'in',
    '[idx]', '[start:stop:step]',
)

# we could copy the cell above inbetween """<answer>""".
# But even simpler, in notebooks we have `In` and `Out` to
# refer to previous cells.
answer = In[-2]
```

```python
for element in elements:
    if not element in answer:
        print(f'missing element: {element}')

# this lists some elements, because we, for example,
# constructed lists with the bracket notation.
# But since we understand the context, that is an adequate
# solution.
```

## Task 05

```python
def f(x):
    return x * (x * (x**3 - 3*x**2 - 8*x) + 12*x + 19) / 3


fixed_points = []
for x in range(-10, 11):
    if f(x) == x:
        fixed_points.append(x)


# again as list comprehension
fixed_points = [x for x in range(-10, 11) if f(x) == x]

print(f'there are {len(fixed_points)} fixed points: {fixed_points}')
```

## Task -1

This is task -1, because negative indexes count from the back and this is the last exercise.

The surprising result is due to the representation of floating point numbers, which has limited precision (fyi, Python implements IEEE 754). Low integer values happen to be exactly representable. It is a lucky case that the comparison in the first example works.

```python
import math
from decimal import Decimal


print(math.isclose(0.1 + 0.2, 0.3))
# True

print(Decimal('0.1') + Decimal('0.2') == Decimal('0.3'))
# True
```

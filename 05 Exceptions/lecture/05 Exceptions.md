# 05: Exceptions

## TL;DR

```python
conn = connect_to_db()

try:
    data = conn.load()
except TimeoutError:
    data = load_from_cache()
finally:
    conn.close()
```

## Kinds of Errors

There are two broad categories of errors that can occur in a program

- we try to do something that cannot work (e.g., calling an undefined function)
- we try to do something that might fail (e.g., requesting data from a web server)

The first type of error can mean a bug in the program logic or inadequate input to the program. In contrast, the second cannot be avoided no matter how carefully we prepare. In Python, both lead to an _exception_, and can be handled using the `try`/`except` syntax. When an exception occurs, the program is stopped and a _traceback_ (a debug message showing where the error occurred) is printed.

## Your Fault

These kind of errors could also be solved by looking very hard at your code and your input. But instead of spending all this time, we can just assume that things are correct, and be notified by a Python in form of an exception whenever something goes wrong. For *non-critical* code, this is a legitimate way to prototype. In the example below, we read in a list of numbers, but one of them can't be converted by `int`, so our program will fail.

```python
numbers_str = '28, 87, 41, 87, 22, 81, 86, 5, 7, 0, 50, 60, 8, 8, 21, 68, 44, 8, five, 96, '

numbers = []
for n in numbers_str.split(', '):
    numbers.append(int(n))
```

```pytb
---------------------------------------------------------------------------
ValueError                                Traceback (most recent call last)
Cell In[1], line 5
      3 numbers = []
      4 for n in numbers_str.split(', '):
----> 5     numbers.append(int(n))

ValueError: invalid literal for int() with base 10: 'five'
```

An exception in Python is presented as a _traceback_. In the simplest case, this consists of a single block showing where the error occurred and what type of error it was. In more complex situations (e.g., when the error originates inside nested function calls) the traceback will _trace back_ through the full chain of calls, all the way to the original source.

This makes debugging more straightforward: you can follow the traceback, locate the problem in your code (or input), and then fix it.

## Errors Beyond your Control

Let's compute the reciprocals of these numbers. This fails as well, but this time not because of an input error, but because of something more fundamental: We try to do division by zero.

```python
reciprocals = [1 / n for n in numbers]
```

The way around this could be to check whether the divisor is zero before attempting the division. This is perfectly legitimate, but there's another possibility, which is to `try` the division, and handle the special case where a `ZeroDivisionError` occurs explicitly.

```python
import math


def safe_division(a, b):
    if b == 0:
        return math.nan

    return a / b


# both work, but this is more explicit
def safe_division(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        return math.nan


reciprocals = [safe_division(1, n) for n in numbers]
```

Observe:

- Both versions of `safe_division` work as expected.
- `try`/ `except` can be more natural: We attempt the division and explicitly state the reason it might fail.
- In contrast, the `if` version starts with the special case; it requires extra cognitive effort (or a comment) to understand why it's handled separately, and only then we get to the general case.

## Asking for Forgiveness instead of Permission

At first, it may seem unprofessional to __just try it and see what happens__, but in Python, using the `try/except` construct __is considered good practice__.

Instead of checking preconditions before running code, it is often simpler and even more robust to just attempt the operation and handle the exception if it fails.

For example, suppose we want to load data from a cache file. If the file doesn't exist (e.g., on the first run), we need to compute the data and store it. We could check with `os.path.exists` first, but what if the file is deleted after we check and before we open it? Such edge cases disappear if we simply try opening the file and catch the exception:

```python
try:
    with open('/tmp/cache.json', 'r') as file:
        data = json.load(file)
except FileNotFoundError:
    data = _compute_data()
    _save_data(data, '/tmp/cache.json')
```

## Exceptions as Regular Flow

In some situations, exceptions are not errors at all, but part of the normal control flow in Python.

Iterators, for example, work this way. An iterator object implements `__iter__` and `__next__`. The latter returns successive elements on each call, until it finishes by raising `StopIteration`.

```python
class Range:
    def __init__(self, stop):
        self._stop = stop
        self._current = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self._current < self._stop:
            value = self._current
            self._current += 1
            return value

        raise StopIteration


[i for i in Range(5)]  # [0, 1, 2, 3, 4]
```

Similarly, `KeyboardInterrupt` (<kbd>ctrl</kbd>+<kbd>c</kbd>) halts the execution of a script, but we can catch it explicitly and treat it as a regular kind of user input. In the example below, we use it to cleanly break out of an infinite while loop.

```python
import time
from datetime import datetime


while True:
    try:
        now = datetime.now()
        print(now.strftime('%a %d %b %Y, %H:%M:%S'), end='\r')
        time.sleep(0.01)
    except KeyboardInterrupt:
        break
```

## Finally

The `finally` block in Python ensures that certain code always runs, no matter what happens inside the try block. This is especially useful for cleanup tasks such as closing files, releasing locks, or disconnecting from a database.

Even if an exception is raised (whether caught or not caught), the finally block still executes before the program exits.

```python
import pickle


file = open('data.pkl', 'rb')
data = pickle.load(file)  # what happens if this fails?
file.close()  # -> file remains open


# better: use try/finally
file = open('data.pkl', 'rb')
try:
    data = pickle.load(file)
finally:  # finally always runs, even if the `try`-block fails
    file.close()  # -> file is properly closed
```

## Context Managers

As we saw, finally ensures that cleanup code always runs, even if an exception occurs. In Python, this pattern is so common that it has dedicated syntax: the context manager.

The most familiar example is file handling, which we have already seen above, where we used: `with open(path) as file…`.

```python
file = open('data.pkl', 'rb')
try:
    data = pickle.load(file)
finally:
    file.close()


# equivalently, as a context manager
with open('data.pkl', 'rb') as file:
    data = pickle.load(file)
```

As with every Python behaviour, a context manager is a class that implements certain dunder methods, specifically `__enter__` and `__exit__`.

For example, `open()`'s `__exit__` method closes the opened file. When we use it in a with block, Python implicitly wraps the block in a `try`/`finally` and ensures that `__exit__` is always called at the end.

## Raising Exceptions

So fare, we've seen exceptions raised by Python when an operation cannot be performed or as a behaviour within the regular control flow. But your own programs can also raise exceptions explicitly.

For example, suppose we want a Patient class to always store a patient's birth date as a proper datetime.date object. Users might try to provide the date in other formats (e.g. a string like `'14.3.1981'` or a Unix timestamp like `353372400`). To enforce consistency, we can validate the input and raise a `TypeError` if it's not a date instance.
Another common case is using `NotImplementedError` to indicate that a method is intended but not yet implemented. This is a simple way to mark placeholders during development.

```python
from datetime import date


class Patient:
    def __init__(self, birth_date):

        if not isinstance(birth_date, date):
            raise TypeError('birth_date must be a date object')

        self.birth_date = birth_date

    def age(self):
        raise NotImplementedError('Patient.age not implemented yet')
```

### Asserts

Closely related to explicit checks are assertions. It is a common programming style to regularly assert statements you expect to be true, especially in critical code. Assertions help catch problems early, before they cause confusing downstream errors.

You can think of assert as a lightweight tool for internal sanity checks, in contrast to raising explicit exceptions, for example for user-facing input validation.

```python
energy = [p**2 for p in pressure]
# ...
# lengthy computation
# ...

mean = sum(energy) / len(energy)

# sanity check: if this fails, something went wrong above
assert len(energy), 'energy must contain elemenets'
assert mean > 0, 'energy must be positive'
```

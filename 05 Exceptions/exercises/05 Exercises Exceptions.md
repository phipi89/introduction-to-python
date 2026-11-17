# 05 Exercises: Exceptions

## Notes

Remember what we've learned in lecture 03 and continue to create a dedicated virtual environment for each week's exercise.

## Task 01

xdfy327t8zv0me9tzkliü. Oh no! My cat walked across the keyboard and deleted bits of the text. As you work through the tasks, fix any errors that raise exceptions.

## Task 02

The file `src/vocode_with_errors.py` implements a noise-band vocoder (a simple simulation of cochlear-implant hearing). It intentionally contains multiple bugs.

1. Copy it to `vocode.py` in your exercise directory. The input audio is `src/input.wav`.
2. Run it using `uv` (outside the notebook), read the tracebacks, and fix the errors one by one.
3. Reward for fixing all errors: Tweak the setup parameters and listen to the output.

## Task 03

The Zen of Python from 1999 (easter egg: `import this`) still floats around in online tutorials. Principles 10 and 11 are:

> «Errors should never pass silently. Unless explicitly silenced.»

That's today's theme. One important place where exceptions matter is input handling: Python won't stop you from passing the wrong objects to functions. Your code must decide how strict it wants to be about accepting input.

Principle 13 is:

> «There should be one-- and preferably only one --obvious way to do it.»

However, the real world disagrees. Below are four _average_ functions with different validation strategies. Call each with both valid and invalid inputs, read the tracebacks, and compare their behaviour (for the last one, you might need to do some research). What are the advantages and disadvantages of each approach?

```python
# a)
def average_basic(*args):
    return sum(args) / len(args)


# b)
def average_test(*args):
    for arg in args:
        if not isinstance(arg, (int, float, complex)):
            raise TypeError('All arguments must be numbers.')

    return sum(args) / len(args)


# c)
def average_try(*args):
    try:
        return sum(args) / len(args)
    except TypeError:
        raise TypeError('All arguments must be numbers.')


# d)
from pydantic import validate_call

@validate_call
def average_pydantic(*args: float):
    return sum(args) / len(args)


# e.g.
average_basic(1, 2, 3)
average_basic('a', 'b', 'c')
```

## Task 04

In Task 03, we used _Pydantic's_ `validate_call`. Pydantic is a tool built for constructing data models with robust input handling. Two important features are:

- Skip boilerplate `__init__` by declaring fields as class attributes.
- Validate input types using _type hints_.

> Note: We won't go deep into type hints in this introductory lecture. In short, `def f(x: int) -> float:` suggests x should be an int and the function returns a float. Importantly, they are hints, not enforcement (unless a tool like Pydantic does enforce them).

1. Study the Pydantic setup below. Instantiate `Implant` and `Telemetry` with various inputs (both valid and invalid) to see what Pydantic accepts / rejects.
2. Load data from `src/implant_log_1.csv` into `implant_A` (see the builtin module `.csv`).
3. Create `implant_B` and load data from `src/implant_log_2.csv` (this one contains typos you must fix in the source csv).
4. Re-implement the same Telemetry and Implant classes in pure Python (i.e., initialise the attributes and validate inputs with `__init__`, `isinstance`, `ValueError`, etc. You may skip `Implant.dump`.)
5. What are the conceptual differences between Pydantic and the built-in approach?

```python
from pydantic import BaseModel, Field, field_validator
from typing import Literal


class Telemetry(BaseModel):
    timestamp: datetime
    voltage: float
    current: float
    pulse_shape: Literal['square', 'sine']
    battery_voltage: float

class Implant(BaseModel):
    model: str
    serial_number: int
    telemetry: list[Telemetry] = []

    def add_telemetry(self, **kwargs):
        self.telemetry.append(Telemetry(**kwargs))

    def dump(self, path=None):
        if path is None:
            path = f'implant_{self.model}_{self.serial_number}_data.json'
            
        with open(path, 'w') as file:
            file.write(self.model_dump_json(indent=2))


implant_A = Implant(model='Lobotomiser', serial_number=1001)
```

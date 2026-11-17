# 05 Exercises: Exceptions Solution

## Task 03

```python
from decimal import Decimal

test_list = [
    (1, 2, 3),
    (1.5, 2.5, 3.5),
    (1, 2.5, -3),
    (1+2j, 3+4j),
    ("1", "2", "3"),
    ("a", "b", "c"),
    (1, "hello", 3),
    (1, None, 3),
    ([1, 2, 3],),
    (True, False, True),
    (Decimal(1), Decimal(2), Decimal(3)),
    (Decimal(1), 2, 3.0),
    (),
]
    
for fun in (average_basic, average_test, average_try, average_pydantic):

    print(f"\nTesting {fun.__name__}")
    print("-" * 40)

    for test_case in test_list:
        try:
            result = fun(*test_case)
            print(f"{str(test_case):<20} ✔")

        except Exception as e:

            description = str(e)
            if description.count('\n'):
                description = '\n' + description + 2*'\n'
                
            print(f"{str(test_case):<20} ✘ {type(e).__name__}: {description}")
```

```text
Testing average_basic
----------------------------------------
(1, 2, 3)            ✔
(1.5, 2.5, 3.5)      ✔
(1, 2.5, -3)         ✔
((1+2j), (3+4j))     ✔
('1', '2', '3')      ✘ TypeError: unsupported operand type(s) for +: 'int' and 'str'
('a', 'b', 'c')      ✘ TypeError: unsupported operand type(s) for +: 'int' and 'str'
(1, 'hello', 3)      ✘ TypeError: unsupported operand type(s) for +: 'int' and 'str'
(1, None, 3)         ✘ TypeError: unsupported operand type(s) for +: 'int' and 'NoneType'
([1, 2, 3],)         ✘ TypeError: unsupported operand type(s) for +: 'int' and 'list'
(True, False, True)  ✔
(Decimal('1'), Decimal('2'), Decimal('3')) ✔
(Decimal('1'), 2, 3.0) ✘ TypeError: unsupported operand type(s) for +: 'decimal.Decimal' and 'float'
()                   ✘ ZeroDivisionError: division by zero

Testing average_test
----------------------------------------
(1, 2, 3)            ✔
(1.5, 2.5, 3.5)      ✔
(1, 2.5, -3)         ✔
((1+2j), (3+4j))     ✔
('1', '2', '3')      ✘ TypeError: All arguments must be numbers.
('a', 'b', 'c')      ✘ TypeError: All arguments must be numbers.
(1, 'hello', 3)      ✘ TypeError: All arguments must be numbers.
(1, None, 3)         ✘ TypeError: All arguments must be numbers.
([1, 2, 3],)         ✘ TypeError: All arguments must be numbers.
(True, False, True)  ✔
(Decimal('1'), Decimal('2'), Decimal('3')) ✘ TypeError: All arguments must be numbers.
(Decimal('1'), 2, 3.0) ✘ TypeError: All arguments must be numbers.
()                   ✘ ZeroDivisionError: division by zero

Testing average_try
----------------------------------------
(1, 2, 3)            ✔
(1.5, 2.5, 3.5)      ✔
(1, 2.5, -3)         ✔
((1+2j), (3+4j))     ✔
('1', '2', '3')      ✘ TypeError: All arguments must be numbers.
('a', 'b', 'c')      ✘ TypeError: All arguments must be numbers.
(1, 'hello', 3)      ✘ TypeError: All arguments must be numbers.
(1, None, 3)         ✘ TypeError: All arguments must be numbers.
([1, 2, 3],)         ✘ TypeError: All arguments must be numbers.
(True, False, True)  ✔
(Decimal('1'), Decimal('2'), Decimal('3')) ✔
(Decimal('1'), 2, 3.0) ✘ TypeError: All arguments must be numbers.
()                   ✘ ZeroDivisionError: division by zero

Testing average_pydantic
----------------------------------------
(1, 2, 3)            ✔
(1.5, 2.5, 3.5)      ✔
(1, 2.5, -3)         ✔
((1+2j), (3+4j))     ✘ ValidationError: 
2 validation errors for average_pydantic
0
  Input should be a valid number [type=float_type, input_value=(1+2j), input_type=complex]
    For further information visit https://errors.pydantic.dev/2.14/v/float_type
1
  Input should be a valid number [type=float_type, input_value=(3+4j), input_type=complex]
    For further information visit https://errors.pydantic.dev/2.14/v/float_type


('1', '2', '3')      ✔
('a', 'b', 'c')      ✘ ValidationError: 
3 validation errors for average_pydantic
0
  Input should be a valid number, unable to parse string as a number [type=float_parsing, input_value='a', input_type=str]
    For further information visit https://errors.pydantic.dev/2.14/v/float_parsing
1
  Input should be a valid number, unable to parse string as a number [type=float_parsing, input_value='b', input_type=str]
    For further information visit https://errors.pydantic.dev/2.14/v/float_parsing
2
  Input should be a valid number, unable to parse string as a number [type=float_parsing, input_value='c', input_type=str]
    For further information visit https://errors.pydantic.dev/2.14/v/float_parsing


(1, 'hello', 3)      ✘ ValidationError: 
1 validation error for average_pydantic
1
  Input should be a valid number, unable to parse string as a number [type=float_parsing, input_value='hello', input_type=str]
    For further information visit https://errors.pydantic.dev/2.14/v/float_parsing


(1, None, 3)         ✘ ValidationError: 
1 validation error for average_pydantic
1
  Input should be a valid number [type=float_type, input_value=None, input_type=NoneType]
    For further information visit https://errors.pydantic.dev/2.14/v/float_type


([1, 2, 3],)         ✘ ValidationError: 
1 validation error for average_pydantic
0
  Input should be a valid number [type=float_type, input_value=[1, 2, 3], input_type=list]
    For further information visit https://errors.pydantic.dev/2.14/v/float_type


(True, False, True)  ✔
(Decimal('1'), Decimal('2'), Decimal('3')) ✔
(Decimal('1'), 2, 3.0) ✔
()                   ✘ ZeroDivisionError: division by zero
```

### Takeaways

The first three functions behave quite similarly. Option (b) can be helpful because it explicitly communicates that the function expects numeric inputs and provides a clear error message. However, its type check makes it more restrictive: for example, it rejects `Decimal`, even though (a) handles them successfully. This is an advantage of (c) over (b): it preserves the range of valid inputs accepted by (a) while still allowing us to provide a custom error message. One important caveat of catching errors is that it can mask the actual cause. See for example the mixed `Decimal` and float input: only (a) correctly identifies the problem.

Pydantic takes a different approach by validating inputs against the declared type annotation. However, it is not strictly enforcing types by default, as it also converts compatible inputs, e.g., `'1'` to float(1).

This exercise should illustrate that the best approach depends on the context. For simple, local code, (a) is perfectly reasonable. Python's default error messages are often just as informative as the custom messages in (b) and (c). Avoiding unnecessary validation keeps the code simple and readable, and prevents introducing new edge cases. More explicit validation becomes useful when writing functions that can fail in more complex ways or that will be used by others.

Finally, validation is only as effective as the checks we implement. For example, passing no arguments raises a `ZeroDivisionError` in all four functions, since none explicitly handles empty input. Type validation does not necessarily guarantee that a function can safely process its inputs.

## Task 04

```python
import csv


with open("src/implant_log_1.csv") as file:
    reader = csv.reader(file, delimiter=",")
    next(reader)  # Skip header
    for row in reader:
        timestamp, voltage, current, pulse_shape, battery_voltage = row
        implant_A.add_telemetry(
            timestamp=timestamp,
            voltage=voltage,
            current=current,
            pulse_shape=pulse_shape,
            battery_voltage=battery_voltage,
        )
```

For B, we can print the number of each line where we encounter an error, then go into the csv file and manually edit it.

```python
implant_B = Implant(model="Mesmeriser", serial_number=5)


with open("src/implant_log_2.csv") as file:
    reader = csv.reader(file, delimiter=",")
    next(reader)  # Skip header
    for i, row in enumerate(reader):
        try:
            timestamp, voltage, current, pulse_shape, battery_voltage = row
            implant_B.add_telemetry(
                timestamp=timestamp,
                voltage=voltage,
                current=current,
                pulse_shape=pulse_shape,
                battery_voltage=battery_voltage,
            )
        except Exception as e:
            print(f"failed on line {i}:\n\n{e}\n\n\n\n")
```

```text
failed on line 2498:

1 validation error for Telemetry
pulse_shape
  Input should be 'square' or 'sine' [type=literal_error, input_value='rectangular', input_type=str]
    For further information visit https://errors.pydantic.dev/2.14/v/literal_error




failed on line 4998:

too many values to unpack (expected 5, got 6)




failed on line 9998:

1 validation error for Telemetry
timestamp
  Input should be a valid datetime or date, month value is outside expected range of 1-12 [type=datetime_from_date_parsing, input_value='1955-13-19T11:28:38', input_type=str]
    For further information visit https://errors.pydantic.dev/2.14/v/datetime_from_date_parsing
```

For the Python reimplementation, this is just a laborious task. Note that we do some input validation through `float()`, instead of manually testing the instance of the passed object. The advantage of pydantic in this scope is that it moves the input validation one layer further into the backend, making the classes (and intention) much more readable.

```python
from datetime import datetime


class Telemetry:
    def __init__(self, timestamp, voltage, current, pulse_shape, battery_voltage):

        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        if not isinstance(timestamp, datetime):
            raise TypeError("timestamp must be a datetime")

        if pulse_shape not in ("square", "sine"):
            raise ValueError("Invalid pulse shape")

        self.timestamp = timestamp
        self.voltage = float(voltage)
        self.current = float(current)
        self.pulse_shape = pulse_shape
        self.battery_voltage = float(battery_voltage)


class Implant:
    def __init__(self, model, serial_number, telemetry=None):

        if not isinstance(model, str):
            raise TypeError("model must be a string")
        if not isinstance(serial_number, int):
            raise TypeError("serial_number must be an integer")

        self.model = model
        self.serial_number = serial_number
        self.telemetry = [] if telemetry is None else telemetry

    def add_telemetry(self, **kwargs):
        self.telemetry.append(Telemetry(**kwargs))
```

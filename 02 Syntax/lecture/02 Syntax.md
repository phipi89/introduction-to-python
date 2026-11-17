# 02: Syntax

## TL;DR

```python
from statistics import median


class Patient:
    def __init__(self, sv, hr):
        self.sv, self.hr = sv, hr
        
    def cardiac_output(self):
        return self.sv * self.hr


patients = [Patient(0.094, 82), Patient(0.083, 67),
            Patient(0.079, 86), Patient(0.087, 75)]

m = median([p.cardiac_output() for p in patients])

print(f'median is {m:.1f} l/min')
```

## Lecture Aim

Today, we'll focus on learning the *basics* of Python. We will skip some technical details and edge cases, but aim not to oversimplifying the code examples. The snippets you see are written in a style that reflects how Python is typically used in practice.

Python is designed to be easy to read and write. Within an hour, we are able to touch on all relevant built-in functions, objects and keywords that define the language.

This overview will necessarily be dense, and you are not expected to remember everything at once. The most important concepts will stick and the rest will come through practice. The script is structured so you can revisit it throughout the semester and rediscover elements you may have forgotten.

## Running Code

We have not learned how to properly set up and run Python on your machine. This will be the topic of next week. For now, you can use an online tool

- [jupyter.org](https://jupyter.org/try-jupyter/lab/)
- [Ubelix OnDemand](https://ondemand.hpc.unibe.ch/) > interactive Apps > Jupyter Notebook
- [google colab](colab.research.google.com)
- …

## Example: Computing Cardiac Output

We'll start off with a very basic example, using Python as a calculator. From there, we'll expand step by step to visit all relevant elements you need to know. In the end, we'll return to the most important concepts.

### Computations

Suppose we have *stroke volume* and *heart rate* of a patient, from which we want to compute his / her cardiac output:

```python
# compute the cardiac output
# given a stroke volume of 94 mL
# and a heart rate of 82 bpm.

0.094 * 82           # 7.708
```

### Variables

We can define _variables_ with the `=` operator. Variables assign a value to a label, so that we can reference it later, but they also help to improve the readability of the code.

```python
stroke_volume = 0.094                             # floating point
heart_rate = 82                                   # integer

cardiac_output = stroke_volume * heart_rate       # 7.708
```

Observe:

- Python knows different types of number (floats, ints, complex). The type of a variable is inferred from the code, so we don't need to specify it explicitly.
- By convention, variable names are written in `lower_case_with_underscores`.

### Functions

If we need to calculate the cardiac output of multiple patients, we can `def`ine a *function*. Functions obtain arguments as input, do some work, and can `return` an output.

```python
def cardiac_output(stroke_volume, heart_rate):
    
    # everything indented by 4 spaces belongs
    # to the function definition
    
    return stroke_volume * heart_rate


# calling the function
co_1 = cardiac_output(0.094, 82)

# optionally, argument names can be used
co_2 = cardiac_output(stroke_volume=0.083,
                      heart_rate=67)
```

Observe:

- In Python, structure is defined by indentation. After the first line that defines the function, all associated code is indented by 4 characters.
- In function calls, arguments can be passed as pure objects (e.g., `82`) or as named attributes (e.g., `heart_rate=67`).

### Collections

Above, we provided values directly as numbers. Let's try to organize this by creating *collections*, i.e., containers that contain multiple objects.

```python
patient_list = [0.094, 82]
patient_tuple = 0.094, 82

# list and tuple elements are accessed by their position
cardiac_output(patient_list[0],
               patient_list[1])


patient_dict = dict(stroke_volume=0.094,
                    heart_rate=82)

# dictionary elements are accessed by a key
cardiac_output(patient_dict['stroke_volume'],
               patient_dict['heart_rate'])
```

Observe:

- `list`s are constructed by square brackets, with elements separated by commas.
- The built-in dict function can be used to construct `dict`ionaries, that map elements to names.
- `tuple`s are comparable to lists, but in contrast to lists and dicts, tuples are immutable. This means once defined, they can't be changed.

```python
patient_list[0] = 0.089            # ✓ changes the value of the first element
patient_tuple[0] = 0.089           # ✗ raises an Error because tuples are immutable
```

### Classes

Above, we used `int`egers and `float`ing point numbers, `list`s, and `dict`ionaries. They are all examples of built-in objects and are designed to fulfil different general purposes.

When we have a more specific use case, we can define our own objects by creating a `class`. Classes are objects that can hold data as _attributes_ and functionality as _methods_.

Let's create a Patient class, that stores the medical data and provides a function to calculate the cardiac output.

```python
class Patient:
    def __init__(self, stroke_volume, heart_rate):
        # associated data are called attributes
        self.stroke_volume = stroke_volume
        self.heart_rate = heart_rate

    # associated functions are called methods
    def cardiac_output(self):
        return self.stroke_volume * self.heart_rate


# class instance
patient = Patient(0.094, 82)

# attributes and methods are accessed with `.`
patient.cardiac_output()
```

Observe:

- Upper case `Patient` is a *class*, lower case `patient` is an *instance* of the class.
- Associated data are called *attributes*, and accessed using the dot notation (e.g., `patient.heart_rate`).
- Associated functionalities are called *methods*, and accessed the same way (e.g., `patient.cardiac_output()`).
- One part that may catch your eye is the `__init__(self, …)`. For now, it is enough to understand that this attaches the attributes when we create the class instance. We'll return to this in more detail in lecture 6.
- There can be multiple instances of the same class. Each instance holds its own data as attributes, but they all share the same structure and functionality.

### Iteration

Below, we have raw data from 20 patients in the form of a list of lists. Let us go element-wise through the data (using a `for` loop), for each element `in` it, create an instance of the Patient class, and `append` it to a list.

```python
raw_data = [
    [0.079, 92], [0.096, 103], [0.110, 94], [0.077, 92], 
    [0.106, 83], [0.086, 95], [0.115, 87], [0.082, 76], 
    [0.098, 79], [0.105, 72], [0.116, 86], [0.096, 79], 
    [0.103, 59], [0.077, 83], [0.068, 90], [0.091, 91], 
    [0.073, 81], [0.093, 88], [0.097, 97], [0.099, 78], 
]


patients = []                               # empty list

for vol, rate in raw_data:                  # vol = 0.079, rate = 92 …
    patient = Patient(vol, rate)
    patients.append(patient)
```

Observe:

- Each element of raw_data that we iterate over is a list of two elements. Python allows to directly assign the tuple (vol, rate), so the first element of the list is assigned to vol, and the second element of the list is assigned to rate.
- Very helpful: Whitespace in between parentheses is ignored, so we can distribute the elements of raw_data onto multiple lines.

Since the creation of a list based on another collection is a very common operation, Python has a special syntax to do the same in one line, called a _list comprehension_.

```python
# patients = []
# # for vol, rate in raw_data:
#     patient = Patient(vol, rate)
#     patients.append(patient)


# equivalently as list comprehension
patients = [Patient(vol, rate) for vol, rate in raw_data]
```

### Conditionals

Another typical element to control the flow of a program are conditionals. In Python, we have `if`, `elif`, `else` to do this.

```python
for patient in patients:
    if patient.heart_rate > 100:
        patient.stressed = True
    else:
        patient.stressed = False
```

Observe:

- We use `>` to compare the heart rates to a threshold value. This comparison return a boolean (`True` or `False`).
- Note how we can add new attributes to patient instances, even if they are not defined in the class definition. Classes are mutable objects as well in Python.

### Membership and Slicing

Maybe you have just found a sticky note on your desk with your last measurement data, and you're not sure whether it is already in raw_data? We can check whether an object is (`not`) `in` a collection.

```python
data_point = [0.099, 78]
data_point in raw_data                       # True

# slice collections with [start:stop:step]
data_point not in raw_data[:-3]              # True
```

Observe:

- Here, we use slicing to check whether the data point appears anywhere before the last three elements of raw_data.
- Note that `in` is overloaded: In the context of a for loop, it defines which elements to iterate over; otherwise it does membership testing.
- Boolean values can be inverted with the `not` keyword, e.g., `elem not in collection`, or also `if not (patient.heart_rate > 100)`.

### Built-In Functions

Let's compute some statistics on our cardiac output values. For common operations, Python has built-in functions, for example to `sum` all elements of an iterable, or to return its `len`gth.

```python
cardiac_outputs = [patient.cardiac_output() for patient in patients]
mean = sum(cardiac_outputs) / len(cardiac_outputs)
```

If you want to know more about any function, you can use the built-in function `help`, to display additional information.

```python
help(sum)
```

```output
Help on built-in function sum in module builtins:

sum(iterable, /, start=0)
    Return the sum of a 'start' value (default: 0) plus an iterable of numbers

    When the iterable is empty, return the start value.
    This function is intended specifically for use with numeric values and may
    reject non-numeric types.
```

### Exceptions

What happens if anything goes wrong? If Python can't execute a command for any reason, it will throw an _exception_, and the program will halt. Python will print a _traceback_, a structured description of what element and what error caused the problem.

```python
squared_diffs = [(patient.cardiac_output - mean) ** 2 for patient in patients]
std = (sum(squared_diffs) / len(patients)) ** 0.5
```

```pytb
---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
Cell In[30], line 1
----> 1 squared_diffs = [(patient.cardiac_output - mean) ** 2 for patient in patients]
      2 std = (sum(squared_diffs) / len(patients)) ** 0.5

TypeError: unsupported operand type(s) for -: 'method' and 'float'
```

Observe:

- The traceback shows the sequence of function calls that led to the error.
- The last line indicates the type of error that occurred (here we have a `TypeError`, because we tried to subtract mean from a class method).

### Imports

Obviously, we're not the first to compute statistics on a list of values. While there are no built-in functions for this, python comes with an extensive standard library that covers many fields. For our purposes, we can for example `import` the stats _module_ and use its predefined median function.

```python
import statistics


median = statistics.median(cardiac_outputs)
std = statistics.stdev(cardiac_outputs)
```

Observe:

- You can understand this as adding an object `statistics` to the namespace of your current program. Among others, this object has a method `median` and `stdev`.
- There is really just a `statistics.py` file shipped with Python, that defines the functionality. For performant code, modules will often be written in other programming languages like C; but as an end user, you won't notice the difference, you can import these like any other python files.

### Printing

Finally, let's `print` our results to the screen.

```python
print('median:', median)                           # median: 7.732
print('standard deviation:', std)                  # standard deviation: 1.429715783312415

print(f'median: {median:.1f} L/min')               # median: 7.7 L/min
print(f'standard deviation: {std:.2f} L/min')      # standard deviation: 1.43 L/min
```

Observe:

- Here we also first meet `str`ings. Strings are yet another form of a collection, but one that holds sequences of characters.
- Strings are defined by 'single' or "double" quotes.
- A helpful special version is the f-string, where we can integrate the string representation of other objects into the string, and define its formatting.

## What to Remember, What to Try

Python programs are built by creating and manipulating objects. The most important building blocks are:

- `=` to assign an object to a variable
- `int`, `float`, `complex` are built-in numerical data types
- `+`, `-`, `/`, `*`, `**`, `%`, and `//` are arithmetic operators
- `True`, `False`, `None` are built-in singletons
- `==`, `!=`, `<`, `<=`, `>`, and `>=` are comparison operators
- `and`, `or`, and `not` to operate on booleans
- `if`, `elif`, `else` for conditional branching
- `list`, `dict`, `set`, `tuple`, and `str` are built-in collection-based data types
- `class` to construct arbitrary objects
- `def` to define a function
- `import` to bring in libraries
- `for` and `while` to repeat code blocks
- `in`, to check if something is in a collection
- `[idx]`, `[start:stop:step]` to access elements

Below, we go through these elements in some more detail. Don't worry, you can't retain all of it immediately. We'll introduce these details step by step in the exercises.

### Expansion

```python
# multiple assignment
a, b, c = 2, 1, 3

# swap
a, b = b, a

# extended unpacking: star-target becomes a list
a, b, *c = 1, 2, 3, 4, 5      # c == [3, 4, 5]

first, *middle, last = 10, 20, 30, 40
*head, tail = 1, 2, 3

# throwaway name
nums = 1, 2, 3, 4, 5
a, b, *_ = nums
a, b = nums[:2]
```

```python
values = [75, 1.71, 25.64]
options = dict(sep=' 🙈 ', end=' 🎉\n')

# expansions also work in function calls
print(*values, **options)                   # 75 🙈 1.71 🙈 25.64 🎉
```

### List Comprehensions

```python
# list comprehension
[i for i in range(10)]                      # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

# filter by condition
[i for i in range(10) if i % 2]             # [1, 3, 5, 7, 9]

# conditional elements
[i if i % 2 else -1 for i in range(10)]     # [-1, 1, -1, 3, -1, 5, -1, 7, -1, 9]
```

### Booleans

```python
# much different from the real world, everything *except*
# empty collections, False, 0, and None is True
bool([])                                    # False
bool(0)                                     # False
bool('')                                    # False

bool(0.000000000000000000000000000001)      # True
bool(statistics)                            # True
bool('all I want for Christmas is you')      # True
```

### Strings

```python
'Strings can be' + ' ' + 'concatenated with the `+` operator.'
'Or even' 'without any explicit operator.'

('and because whitespace is '
'ignored within parentheses, '
'this is a single line string')


"Strings can also be defined with double quotes."

"""Triple quotes
define multiline
strings."""


result = 42
f'f-strings allow to integrate expressions: Answer is {result}.'


'Strings can also contain \n\t• newlines `\\n`\n\t• tabulators `\\t`\n\t• 🎉 unicode 🎉'
```

### Functions

```python
def task(arg1, arg2, optional_arg=True, *args, **kwargs):
    """A description of what this function does is called
    a docstring, and goes here. This text will be shown
    if you use `help(taks)`.
    
    arg1: Description of first argument
    arg2: Description of second argument
    
    …etc
    """

    # do some work here

    # args is a tuple of arguments provided after the named arguments
    # kwargs is a dict of key - value pairs of any additional named arguments

    # returning something is optional
    return answer
```

### Classes

```python
class Object(ParentObject):
    """Classes can have docstrings as well."""
    
    def __init__(self, init_arg):
        self.attr = init_arg
        self._done = False

    def __repr__(self):
        return f'< Object ({"done" if self._done else "not done"})>'

    def process(self):
        if not self._done:
            self.attr = None
            self._done = True
```

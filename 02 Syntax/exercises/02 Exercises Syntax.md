# Exercises: 02 Syntax

## Notes

1. These exercises are voluntary.
2. Exercises are essentially collections of carefully crafted prompts, so modern LLMs will be very good at solving them. I recommend to solve the first weeks exercises without help from the internet (including code completion tools in IDEs), otherwise you won't learn much.
3. We did not learn to set up Python on your system yet. For this first exercise, create an online notebook at [jupyter.org](https://jupyter.org/try-jupyter/lab/).

## Task 01

Copy all instructions and exercises from this document as markdown cells into your notebook, and create code cells for your answers in-between. Use this exercise to learn how to navigate through notebooks.

- move through cells with <kbd>up</kbd>, <kbd>down</kbd>
- create new cells with <kbd>a</kbd>, <kbd>b</kbd>
- set cell type with <kbd>y</kbd>, <kbd>m</kbd>
- <kbd>enter</kbd> cells, and run them with <kbd>cmd</kbd>+<kbd>enter</kbd>
- exit cells with <kbd>esc</kbd>

## Task 02

The course consists of 14 lectures and 12 exercise sessions. It awards 2 ECTS, where one ECTS corresponds to 25-30 hours of workload.

1. Write Python code that computes and prints the expected time commitment per exercise. Use descriptive variable names so that others can easily follow your calculation.
2. In a separate cell below, define a function that performs the same computation. The function should take a keyword argument `approach` that expects either `'minimalistic'` or `'maximalistic'`. Call the function twice, once for each approach, and display the results.

```python
# your solution for task 02 goes here.
```

## Task 03

In the lecture we've seen this list of Python building blocks.
For each element, write a line (or, where necessary, multiple lines) of Python that illustrates its use. Try to combine multiple elements into the same expression, but keep it readable.

- `=`
- `int`, `float`, `complex`
- `+`, `-`, `/`, `*`, `**`, `%`, `//`
- `True`, `False`, `None`
- `==`, `!=`, `<`, `<=`, `>`, `>=`
- `and`, `or`, `not`
- `if`, `elif`, `else`
- `list`, `dict`, `set`, `tuple`, `str`
- `class`
- `def`
- `import`
- `for`, `while`
- `in`
- `[idx]`, `[start:stop:step]`

```python
# your solution for task 03 goes here.
```

## Task 04

1. Define a tuple `elements`, whose elements are the expressions from the above bullet point list, expressed as strings.
2. Assign your previous answer as a multiline string to a variable `answer`.
3. Iterate through `elements` and verify that each element is in `answer`.

```python
# your solution for task 04 goes here.

elements = …
answer = …
…
```

## Task 05

Consider the function `f` below. Find all integer fixed points of the function between -10 and 10 (a fixed point is a value ξ that satisfies f(ξ) = ξ).
Do this first using a for loop and then also rewrite it as a list comprehension.

Finally, print an f-string that lists the values and says how many there are.

```python
def f(x):
    return x * (x * (x**3 - 3*x**2 - 8*x) + 12*x + 19) / 3
```

```python
# your solution to task 05 goes here.
```

## Task -1

(Why does this task have the number -1?). Check out the two comparisons below. We would expect both of them to be `True`, however the second one is `False`. What do you think goes wrong? Can you make an educated guess (write it in a markdown cell)?

```python
print(1.0 + 2.0 == 3.0)     # True, as expected
print(0.1 + 0.2 == 0.3)     # False, wtf?
```

Now, import the built-in modules `decimal` and `math`. Use the built-in function `help` to look at their documentation, and for both modules, write a solution that resolves the unexpected behaviour.

```python
# your solution to task -1 goes here.
```

# Exercises: 04 Objects and Classes

## Notes

Complete and run this session locally on your own computer in a dedicated virtual environment.

> Note: Task 1 and 2 require iterative tweaking. This exercise aims to illustrate prototyping code in notebooks. You can start with a basic implementation of task 1, continue to task 2, see what does and does not run in task 4, come back to task 1, tweak, etc. You can always test some part in a new cell, tweak, and once that works, delete that cell again.

## Task 01

```python
task_01_question = """\
- Create a class `Exercise`.
- It should initialise with metadata as attributes:
 `lecture`, `index`, `title`.
- Define an expressive `__str__` method.
- Implement everything needed so that Task 04 runs successfully.
    - Hint: A class becomes iterable, if it defines `__getitem__`
      and `__len__` methods.
    - The write method should create a markdown file, with
        - Title
        - Header block that contains the metadata information
        - For each task: Subtitle, the assignment_text and the
          output of task.solution_text() for each task.
"""


class Exercise:
  pass
```

## Task 02

```python
from src.utils import objects_to_sourcecode


task_02_question = """ \
- Create a class `BaseTask`.
- It should initialise with metadata as attributes:
  `assignment_text`, `index`, `solution=None`.
- Create `EssayTask` and `CodeTask` that inherit from `BaseTask`.
- Implement everything needed so that Task 04 runs successfully.
    - For CodeTask's `solution_to_text` method, use the function
      `utils.object_to_sourcecode`.
"""
```

## Task 03

```python
task_03_question = """\
Add docstrings to classes and methods in Task 1 & 2. Explore the
automatic documentation, e.g., with help(Exercise).
What should you include in a good docstring to help future users
(including yourself) to understand and maintain the code?
"""

task_03_answer = 
```

## Task 04

```python
import os
import sys
import pathlib


# Setup
task_01 = CodeTask(index=1,
                   assignment_text=task_01_question)

task_01.set_solution(Exercise)


task_02 = CodeTask(index=2,
                   assignment_text=task_02_question)

task_02.set_solution(BaseTask, CodeTask, EssayTask)


task_03 = EssayTask(index=3,
                    assignment_text=task_03_question)

task_03.set_solution(task_03_answer)


exercise = Exercise(index=4,
                    title='Objects and Classes')
exercise.add_task(task_03)
exercise.add_task(task_02)
exercise.add_task(task_01)


# Validation
for i, task in enumerate(exercise, start=1):
    assert i == task.index, 'tasks must be ordered'
    assert task.has_solution(), 'tasks must have a solution'

executable_path = pathlib.Path(sys.executable)
document_base = pathlib.Path(os.getcwd())

assert executable_path.is_relative_to(document_base), (
    'you must use a local virtual environment within the working directory'
)


# Export
exercise.write('Exercices-04_Surname-Name.md')
```

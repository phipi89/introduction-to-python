# 04 Exercises: Objects and Classes Solution

````python
from src.utils import objects_to_sourcecode


class Exercise:
    """Represent a coding exercise containing multiple tasks.

    Attributes:
        course: Name of the course.
        index: Exercise index.
        title: Exercise title or lecture name.
        tasks: Tasks belonging to the exercise.
    """

    course = "Introduction to Python"

    def __init__(self, index, title):
        self.index = index
        self.title = title
        self.tasks = []

    def __str__(self):
        return f"<{self.course}: {self.index:02d} {self.title}>"

    def __getitem__(self, index):
        return self.tasks[index]

    def __len__(self):
        return len(self.tasks)

    def add_task(self, task):
        """Add a task to the exercise."""

        self.tasks.append(task)

    def write(self, file_path):
        """Write the exercise and its solutions to a Markdown file at `file_path`."""

        lines = []
        lines.append("# Exercise Solution")
        lines.append("")
        lines.append(f"* Course: {self.course}")
        lines.append(f"* Lecture: {self.title}")
        lines.append(f"* Index: {self.index}")

        lines.append("---")

        for task in self.tasks:
            lines.append("")
            lines.append(f"## Task {task.index:02d}")
            lines.append("### Assignment")
            lines.append(task.assignment_text)
            lines.append("")
            lines.append("### Solution")
            lines.append(task.solution_text())
        lines.append("")

        output = "\n".join(lines)
        with open(file_path, "w") as file:
            file.write(output)


class BaseTask:
    """Base class for an exercise task.

    Specific task classes should inherit from this class and
    override `BaseTask.solution_text`.
    """

    def __init__(self, index, assignment_text):
        self.index = index
        self.assignment_text = assignment_text
        self.solution = None

    def set_solution(self, *solution):
        """Store one or more objects into a list."""

        self.solution = solution

    def has_solution(self):
        return self.solution is not None

    def solution_text(self):
        return "\n".join(self.solution)


class EssayTask(BaseTask):
    def __init__(self, index, assignment_text):
        BaseTask.__init__(self, index, assignment_text)


class CodeTask(BaseTask):
    def __init__(self, index, assignment_text):
        BaseTask.__init__(self, index, assignment_text)

    def solution_text(self):
        # this overwrites BaseTask's solution_text method

        code = [objects_to_sourcecode(object) for object in self.solution]
        return "```python\n" + "\n\n".join(code) + "\n```"
````

```python
task_01_question = """\
- Create a class `Exercise`.
- It should initialise with metadata as attributes:
 `lecture`, `index`, `title`.
- Define an expressive `__str__` method.
- Implement everything needed so that Task 04 runs successfully.
    - Hint: A class becomes iterable, if it defines `__getitem__`
      and `__len__` methods.
    - The sign method should use the same signature box as in the
      previous exercise.
    - The write method should create a markdown file, with
        - Title
        - Header block that contains the metadata information
        - For each task: Subtitle, the assignment_text and the
          output of task.solution_text() for each task.
"""


task_02_question = """ \
- Create a class `BaseTask`.
- It should initialise with metadata as attributes:
  `assignment_text`, `index`, `solution=None`.
- Create `EssayTask` and `CodeTask` that inherit from `BaseTask`.
- Implement everything needed so that Task 04 runs successfully.
    - For CodeTask's `solution_to_text` method, use the function
      `utils.object_to_sourcecode`.
"""

task_03_question = """\
Add docstrings to classes and methods in Task 1 & 2. Explore the
automatic documentation, e.g., with help(Exercise).
What should you include in a good docstring to help future users
(including yourself) to understand and maintain the code?
"""

task_03_answer = """\
A good docstring should tell readers the purpose of an object and
how to use it. When not self-explanatory, it should explain
arguments and return values.

Where appropriate, document relevant attributes, but generally, do
not document methods, as they can do that in their own docstring
when necessary.

Don't write docstrings when they add nothing (e.g., there's nothing
of interest in our implementation of  `Exercise.__str__`).
"""
```

```python
import os
import sys
import pathlib


# Setup
task_01 = CodeTask(index=1, assignment_text=task_01_question)

task_01.set_solution(Exercise)


task_02 = CodeTask(index=2, assignment_text=task_02_question)

task_02.set_solution(BaseTask, CodeTask, EssayTask)


task_03 = EssayTask(index=3, assignment_text=task_03_question)

task_03.set_solution(task_03_answer)


exercise = Exercise(index=4, title="Objects and Classes")
exercise.add_task(task_01)
exercise.add_task(task_02)
exercise.add_task(task_03)


# Validation
for i, task in enumerate(exercise, start=1):
    assert i == task.index, "tasks must be ordered"
    assert task.has_solution(), "tasks must have a solution"

executable_path = pathlib.Path(sys.executable)
document_base = pathlib.Path(os.getcwd())

assert executable_path.is_relative_to(document_base), (
    'you must use a local virtual environment within the working directory'
)


# Export
exercise.write("04 Exercises Objects and Classes Solution.md")
# when everything runs as expected, submit the _generated_ file
```

# Exercises: 03 Virtual Environments

## Notes

Complete and run this session locally on your own computer.

## Task 01

- Windows users: If you don't already have / use a terminal emulator, install Git Bash (or any tool you prefer).

- In the shell, navigate to a suitable directory and create a project directory for this exercise session. Use this to familiarise with some basic POSIX commands:

  - `cd`: change directory
  - `ls`: list directory content
  - `pwd`: print working directory
  - `mkdir`: create a directory
  - `man`: show manual

> Note: The command line can seem a little dated, but it is a very efficient tool for interacting with your computer. See this course as an opportunity to become comfortable using it.

> Note: If you prefer using cmd.exe or powershell, feel free to do so. They should allow you to do everything required in this lecture. But be aware that some command names differ, so it's up to you to adapt these from here on.

## Task 02

- Install `uv`.
- In your exercise directory, initialise a Python project within a directory `project-uv`.
- Navigate into the project directory.
- Use uv to install `jupyter` in the local environment.
- Use uv to start `jupyter lab` in the local environment.
- Create a notebook and copy all code and instructions from this document into your notebook.
- In a markdown cell below, list what shell commands you used.
- Print `sys.executable` to ensure that you are running the newly created venv.
- Print `os.listdir()`. For each file, describe what it does.

> Note: I recommend installing your software through a packet manager like [winget](https://docs.astral.sh/uv/getting-started/installation/#winget) or [homebrew](https://docs.astral.sh/uv/getting-started/installation/#homebrew).

## Task 03

- Back in the terminal, create a sibling directory `project-pip`.
- Create a virtual environment using Python's `venv` module and use `pip` to install `jupyter`.
- start Jupyter lab, and verify that you are indeed within your project-pip venv.

## Task 04

To share a project setup, it is enough to share the .toml-file. With a pip-managed venv however, you need to first explicitly create a requirements-file.

- In project-pip, run `pip freeze > requirements.txt`.
- run the two cells below (remember: this notebook is still running in the uv-project)
- In a markdown-cell below:
  - Describe what `!cat` does. What is the difference to the second command `with open…`.
  - Explain the content of the two files, why are they so different?

```python
!cat pyproject.toml
```

```python
with open('../project-pip/requirements.txt') as file:
    print(file.read())
```

## Task 05

- Use `sys` to find out what version of Python you are running.
- Close Jupyter, downgrade the Python version of the uv-project by 0.1 (e.g. 3.14 to 3.12) and restart Juypter lab.
- What's the difference between the file `.python-version` and `requires-python` in `pyproject.toml`?
- How would you change the Python version in project-pip?

## Task 06

- Save and close this notebook and stop Jupyter.
- Install VSCodium, or any other IDE that supports Jupyter notebooks.
- Open the notebook you created in the IDE. It should automatically ask you to install all required extensions.
- Run the notebook, ensure that `sys.executable` again points to the correct virtual environment.

> Note 1: Typically, IDEs will recognise the local venv if its in a `.venv` directory. If not, sometimes you need to select it manually. On VSCodium, this would be <kbd>ctrl</kbd>+<kbd>shift</kbd>+<kbd>P</kbd> › Python: Select Interpreter › Enter interpreter path…

> Note 2: On Windows, the `!cat…` commands likely fails as `!` runs the system's default shell. If this is the case, replace the line with the corresponding Python command. To quickly run shell commands, you best just use the integrated terminal of your IDE, which you typically can set to Git Bash.

## Task 07

Create a standalone script named `print_address.py` that uses [Faker](https://pypi.org/project/Faker/) to print a random fictional address.

Make the script directly executable so that it can be run outside a virtual environment with:

```bash
./print_address.py
```

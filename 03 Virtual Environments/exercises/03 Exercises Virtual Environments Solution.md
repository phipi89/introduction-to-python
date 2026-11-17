# Solution: Exercises Virtual Environments

## Task 02

Below are the steps required in the shell (install uv as you do any software on your computer; I recommend using a packet manager, but that's up to you):

```bash
# Install uv; see https://docs.astral.sh/uv/getting-started/installation/
# you might need to restart the shell for `uv` to be available

cd ~/Documents/BME/2026/ItP/exercises/03/  # or wherever your exercises are located
uv init project-uv
cd project-uv
uv add jupyter
uv run jupyter lab
```

Then in a notebook cell:

```python
import sys
import os

print(sys.executable)
# should be …/project-uv/.venv/bin/python

print(os.listdir())
```

This should list the following files:

- `src`: source directory for code
- `pyproject.toml`: defines the project and its direct dependencies
- `uv.lock`: records the exact resolved versions of the project's dependencies
- `.python-version`: allows you to pin a specific Python version
- `Ex03.ipynb`: the exercise notebook you created
- `.ipynb_checkpoints`: automatically generated Jupyter notebook checkpoints
- `README.md`: starting point for the project description
- `.venv`: virtual Python environment
- `.git`: Git version-control data; important but not part of this course
- `.gitignore`: belongs to git

## Task 03

Steps in th shell:

```bash
# Technically, you need to install Python first,
# but uv likely did that for you

cd ..  # assume you continue from Task 02
mkdir project-pip
cd project-pip
python -m venv .venv  # use python3 on some systems
source .venv/bin/activate
python -m pip install jupyter
jupyter lab
```

## Task 04

`cat` is a shell command to print the contents of a file. The leading `!` is a shorthand for running shell commands from within a Jupyter notebook. Therefore, the corresponding cell runs a shell command rather than Python. The `with open(…)` cell also prints the contents of the file, but does so using Python.

The output of `pip freeze` should look something like this:

```text
anyio==4.15.1
appnope==1.0.0
argon2-cffi==25.1.0
…
< 90 more libraries >
…
webencodings==0.6.1
websocket-client==1.9.2
widgetsnbextension==4.0.1
```

The reason for the difference is that `jupyter` itself depends on dozens of other libraries. `pip freeze` does not distinguish between packages installed directly by the user and packages installed as dependencies of other packages. The `pyproject.toml` file, however, makes this distinction and therefore lists only `jupyter` as a direct dependency.

## Task 05

```python
print(sys.version)
# '3.14.3 (main, Mar 10 2026, 18:02:52) [Clang 21.1.4 ]'
```

To downgrade Python, change the version specified in `.python-version`, for example from `3.14` to `3.13`. You can do this manually in JupyterLab or with any other text editor. Alternatively, you can run:

```bash
uv python pin 3.13
```

This command edits the `.python-version` file for you.

To restart JupyterLab:

```bash
# Press Ctrl+C twice to stop the JupyterLab server
uv run jupyter lab
```

You may also need to change the version range specified by `requires-python` in `pyproject.toml`. The pinned Python version must be compatible with this range.

## Task 06

Full file content of `print_address.py`:

```python
#!/usr/bin/env -S uv run

# /// script
# dependencies = [
#     "faker",
# ]
# ///

from faker import Faker

fake = Faker("de_CH")

print(fake.name())
print(fake.address())
```

On Unix systems, you need to make the file executable before running it directly. You can do this with:

```bash
chmod +x print_address.py
```

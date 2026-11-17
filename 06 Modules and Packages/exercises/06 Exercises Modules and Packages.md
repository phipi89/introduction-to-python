# 06 Exercises: Modules and Packages

## Task 01

Create all necessary files and directories for a package `toolbelt`, with submodules `iterator`, `logging`, `misc`, and `utils`.

## Task 02

Below are two code snippets to explore.

1. Decorators are a handy tool in Python. We have not seen them in the lecture, but the basic concept is straight forward. Study the example below and try decorating functions, classes and methods. What do decorators do?

```python
def decorator(func):
    def wrapper(*args, **kwargs):
        print("Before execution")
        result = func(*args, **kwargs)
        print("After execution")
        return result

    return wrapper


@decorator
def run():
    print("Function execution")


run()
```

2. Analise the code below. Based on this, write a function `get_cell_source` that returns the source code of the currently running cell. Save it to `toolbelt.utils`.

```python
from IPython import get_ipython

hist = get_ipython().history_manager
hist.get_tail?
```

## Task 03

The code below uses `curl` to send a request to a LLM. Write an analoguous Python function `request_LLM(content: str)` to `toolbelt.utils`, that _posts_ a request and returns the generated answer (use Python's `requests` and `json` libraries).

```bash
curl https://oai.endpoints.kepler.ai.cloud.ovh.net/v1/chat/completions \
  --header "Content-Type: application/json" \
  --data '{
    "model": "gpt-oss-20b",
    "messages": [
      {
        "role": "user",
        "content": "Please count to 10\n"
      }
    ]
  }'
```

## Task 04

> «There are 2 hard problems in computer science: cache invalidation, naming things, and off-by-1 errors.»

At least naming things should have become easy with LLMs! Write a decorator `suggest_name`, that

- Retrieves the current cell’s source using your helper from Task 02 and 03,
- Uses an LLM to suggest a better name,
- Prints the suggestion, then continues the regular program.

You can assume that this is only used in notebooks, and that the decorated object is defined in the currently running cell. The useage should follow this pattern:

```python
from toolbelt.utils import suggest_name


@suggest_name
class TempName:
    # imagine this is a large class that defines
    # some functionality, but we have no idea
    # how to name it.
    # GenAI should propose a name based on the
    # source code.

obj = TempName()       # prints suggestion and continues
```

## Task 04

Off-by-one errors on the other hand are inevitable, so let's make them official.

In `toolbelt.iterators` implement `range(start, stop, step)`, that behaves like the built-in `range`, but adds a random offset. Bonus points for adding fun, unforeseen behaviour.

## Task 05

There are powerful libraries for essentially everything in Python. The hard part is often just remembering how to set them up. Modules can be helpful to set up preconfigured versions of existing tools.

In `toolbelt.logging`, write code to set up logging to your liking through `basicConfig` (configure level, format and datefmt).

Intended usage:

```python
from toolbelt.logging import logging  # sets up your config

logging.info("Application started")
logging.warning("Something needs attention")
logging.debug("Additional details")
```

## Task 06

Save the code below to `misc`, and make sure the test runs:

```python
# toolbelt/misc.py
 
import toolbelt as tb
from toolbelt.log import logger


@suggest_name
def test_package():
    logger.info("This should use our custom logging setup.")

    logger.info("Testing our custom iterator.")
    for i in tb.iterators.range(1, 5):
        print(tb.iterators.range(1, 5))

    source = tb.utils.get_cell_source()
    line_count = len(source.split("\n"))
    logger.info(f"this cell has {line_count} lines")

    content = "What is the answer to the ultimate question of life, the universe, and everything?"
    response = tb.utils.request_LLM(content)
    logger.info(f"Answer is {response}")

# enf of misc.py
```

```python
# test (to be run in notebook)


import toolbelt as tb

tb.misc.test_package()
```

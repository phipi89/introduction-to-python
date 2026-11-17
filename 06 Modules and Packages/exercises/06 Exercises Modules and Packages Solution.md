# 06 Exercises: Modules and Packages Solution

## Task 01

```python
!mkdir toolbelt
!touch toolbelt/iterator.py toolbelt/log.py toolbelt/misc.py toolbelt/utils.py
```

## Task 02

decorators allow to modify or extend the behaviour of existing functions. For part 2:

```python
# toolbelt.utils.py (part 1)

from IPython import get_ipython


def get_cell_source():
    hist = get_ipython().history_manager
    session, line, code = hist.get_tail(n=1, include_latest=True)
    return code
```

Before testing your module works, be sure to set up autoreload:

```python
%load_ext autoreload
%autoreload 3
```

```python
# toolbelt.utils.py (part 2)

import json
import requests


def request_LLM(content):
    url = "https://oai.endpoints.kepler.ai.cloud.ovh.net/v1/chat/completions"
    header = {"Content-Type": "application/json"}
    data = {"model": "gpt-oss-20b", "messages": [{"role": "user", "content": content}]}

    r = requests.post(url, headers=header, data=json.dumps(data))
    content = json.loads(r.content)
    suggestion = content["choices"][0]["message"]["content"]

    return suggestion
```

## Task 03

```python
# toolbelt.utils.py (part 3)

def suggest_name(func):
    def wrapper(*args, **kwargs):
        # first, suggest a name

        source = get_cell_source()
        content = (
            "You are an expert softeware engineer."
            "Below is some source code that includes a fuction or class "
            "decorated with `@suggest_name`. Please read the code carfully, "
            "understand its function and come up with a clear, concise, "
            "pythonic name for it."
            ""
            "Please respond the suggested name only, not any other information."
            ""
        ) + source
        suggestion = request_name_from_source(source)
        print('in s')
        print(f"\nSUGGESTED NAME FOR THE UNNAMED OBJECT: {suggestion}\n\n")

        # run the function normally
        result = func(*args, **kwargs)
        return result

    return wrapper
```

## Task 04

```python
# toolbelt/iterator.py

import random


builtin_range = range


class range:
    def __init__(self, start, stop, step):
        self.start = start
        self.stop = stop
        self.step = step
        
        self._offset = random.random()
        if random.random() > 0.42:
            self.stop += 1
        self._current = start + self._offset

    def __iter__(self):
        return self

    def __next__(self):
        if self._current < self.stop:
            value = self._current
            self._current += 1
            return value

        raise StopIteration
```

## Task 05

```python
import toolbelt as tb

tb.misc.test_package()
```

The output should look something like this:

```text
SUGGESTED NAME FOR THE UNNAMED OBJECT: run_tests


10:30:40 W L07 logging.py       → test
10:30:49 I L07 misc.py          → This should use our custom logging setup.
10:30:49 I L09 misc.py          → Testing our custom iterator.
10:30:49 I L11 misc.py          → [1, 1.9934904594564058, 2.966626265264474, 3.9538872022376124, 4.977899632681459, 5.964525182822198]
10:30:49 I L11 misc.py          → [1, 1.9937526064836404, 2.939988082157508, 3.8655396260683044, 4.765041535161752]
10:30:49 I L11 misc.py          → [1, 2.0405068851304238, 3.0905420872672638, 4.164170564558562]
10:30:49 I L11 misc.py          → [1, 1.9616636745573923, 2.8913138399156626, 3.815079836044727, 4.703885511637701]
10:30:49 I L11 misc.py          → [1, 1.956891102719121, 2.917553010506823, 3.905139536845377, 4.916724089989415]
10:30:49 I L11 misc.py          → [1, 2.0249411905135686, 3.0373580388129504, 4.032968337163787, 4.992167949919786]
10:30:49 I L15 misc.py          → this cell has 3 lines
10:30:51 I L19 misc.py          → Answer is The answer, as famously given in *The Hitchhiker’s Guide to the Galaxy*, is **42**.
```

For the import to work, you need to import the submodules in `toolbelt.__init__.py`.

```python
# toolbelt.__init__.py

from toolbelt import utils, iterator
```

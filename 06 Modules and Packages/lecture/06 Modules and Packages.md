# 06: Modules and Packages

## TL;DR

- *Modules* are single .py files that group related functionality.
- *Packages* are directories that group modules (and possibly subpackages).
- In Juypter, always use *%autoreload 3*

## Abstracting the Abstraction

We're climbing one level up in abstraction: by grouping classes and functions into modules and packages, we can create a reusable library for our projects.

> Note: _Library_ isn't a formal Python term, it is just a general label for modules and packages.

## Module

A module is any Python file. Every object defined in it can be imported.

With the import statement, we don't provide a file path, but just a name. To locate its source code, Python searches for .py files with that name in all directories defined in your environment's _PATH_ variable. The current working directory is always added to path by Python, so the simplest way to import a module is to have the file just next to your script file.

Below, we import `tools`, which works because we have a `tools.py` file in our working directory. Importing a module gives you a namespace object. You access its contents via `module_name.object_name`. `tools.py` contains a `Patient` class, so we can access it as `tools.Patient`:

```python
# --------
# tools.py
from pydantic import BaseModel


class Patient(BaseModel):
    stroke_volume: float
    heart_rate: float


# ------------
# this_file.py

import tools


p = tools.Patient(stroke_volume=0.072, heart_rate=82)
```

## Package

For more complex setups, we might want to structure this again into a hierarchical structure (I promise, it's the last!), and this can be done with a package. A package is a collection of Python files (i.e., modules) within a directory.

As an example, let's create a `biomed` package, that contains three modules: `image`, `pyhsiology` and `signal`.

Packages could contain packages again, so you can nest these structures arbitrarily deep, but for this example, we keep it simple.

```bash
.
├── this_file.py
├── biomed              # package
│   ├── __init__.py     # optional; runs on `import biomed`
│   ├── image.py        
│   ├── physiology.py
│   └── signal.py       
└── tools.py            # unrelated module
```

## Importing a Package ≠ Importing its Submodules

`import biomed` does not automatically import `biomed.image`, `biomed.signal`, etc. If you want submodules available using `import biomed`, import them in `biomed/__init__.py`. This initialisation file is run upon import of the package (as its name already suggests, it's the same concept as the init dunder method that is run when creating a class instance):

```python
# ------------------
# biomed/__init__.py

from biomed import image, physiology, signal


# ------------------
# script.py

import biomed


img = biomed.image.black(shape=(224, 224))
#            ↳ submodule image is imported by __init__.py
```

## Internal Imports

Modules inside a package can import each other as *package members*. Within packages, imports are more strict, Python won't search your full path. If `image.py` for example requires a function from `signal.py`, we need to use the full structure (`import biomed.signal`, not `import signal`, even though both files are in the same directory). Alternatively, relative Imports inside packages can must be explicitely marked with a leading dot: `from .signal import clip`.

```python
# ----------------
# biomed/signal.py

def clip(array, min=0, max=1):
    array[array < min] = min
    array[array > max] = max
    return array


# ---------------
# biomed/image.py

from biomed.signal import clip       # NOT `from signal import clip`
                                     # because we're in a package

def preprocess(img):
    img /= 255
    img = clip(img)
    return img
```

## `if __name__ == '__main__'`

When a module is imported, all code within the file is executed. Therefore, inside modules, top-level code should be limited to definitions. `cleanup.py` below gives an example of why this is important.

```python
def deletable_files(base='.'):
    found = set()
    for root, dirs, files in os.walk(base):
        for file in files:
            if file.endswith(('.tmp', '.bak', '.log', '.DS_Store', '__pycache__')):
                path = os.path.join(root, file)
                found.add(path)
    return found


for file in deletable_files():
    print('Deleting:', file)
    os.remove(file)
```

This file cleans up temporary files and similar leftovers. Suppose we want to reuse the helper function deletable_files() in another program. We can do this with `from cleanup import deletable_files`. However, importing the module runs for loop, thus immediately deleting files.

To avoid this, we can check how the file is being executed. Python defines a special built-in variable `__name__` for every module:

- _If the file is run as a script,_ (e.g., python cleanup.py), then `__name__` _is set to_ `'__main__'`.
- _If the file is imported as a module,_ (e.g., import cleanup), then `__name__` _is set to the module's name_.

We can use this to protect code that should only run when the file is executed directly:

```python
def deletable_files(base='.'):
    found = set()
    for root, dirs, files in os.walk(base):
        for file in files:
            if file.endswith(('.tmp', '.bak', '.log', '.DS_Store', '__pycache__')):
                path = os.path.join(root, file)
                found.add(path)
    return found


if __name__ == '__main__':
    
    # code that only runs when called as a script
    
    for file in deletable_files():
        print('Deleting:', file)
        os.remove(file)
```

In short, wrapping script-only actions inside `if __name__ == '__main__':` lets you safely use the same file both as a standalone program and as a reusable module.

## Autoreload

When working on your own modules interactively in a notebook, there is an annoying problem: Once a module has been imported, changes to its source file are not picked up. Imports are cached for efficiency, so even re-importing a module does not reload it.

To make this workflow smoother, Jupyter offers the autoreload extension, which automatically reloads modules when they change:

```python
%load_ext autoreload
%autoreload 3
```

With that setup, changes to imported modules are applied automatically. Edits to functions or class methods take effect immediately, even for existing class instances. This makes autoreload a very convenient tool for interactive development.

## My Workflow Recommendation

- _When starting a new Python project,_ I recommend to _start in a Jupyter notebook._ Build things step by step, line by line.
- _As patterns or reusable ideas emerge, group them into functions and classes._ Then continue with the next subtask.
- _Once those_ functions or classes _start to feel stable, move them into a module._ They don't need to be polished. With autoreload, you can keep developing interactively, edit and extend your module in the background while testing it live in the notebook.

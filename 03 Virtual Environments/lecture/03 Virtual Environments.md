# 03: Virtual Environments

## TL;DR

```bash
# give each project its own environment and explicitly track its dependencies

uv init <project-name>
uv add <library>
uv run python
```

## The Competition

The strength of Python lies in its vast ecosystem of libraries. [PyPI](https://pypi.org/) hosts nearly 700'000 projects, developed independently by individuals and organisations. This richness cannot be packaged into a single, ready-made application.

By contrast, the appeal of managed Software like Matlab is that it comes in a self-contained application where one double click launches an IDE (integrated development environment) with the entire software stack ready to use.

With Python, you are free to choose IDE, Python version, and library management tool. This flexibility is powerful but can feel overwhelming at first. In this lecture we will see how to set up Python properly.

## The Most Probable Solution

Imagine you are new to Python and want to use SciPy for some data analysis. You likely search online or ask a chatbot, _"How to install scipy:"_

![Library Installation](media/03%20installation-steps.png "How to install SciPy!?")

The likely answer is to type `pip install scipy` into your command line. This does install SciPy, but it is a bad answer:

- it _installs_ the library _into your system Python_. Using one installation for multiple projects quickly leads to conflicts.
- `pip` _does not well resolve dependency conflicts_. If you later add a library that requires a newer SciPy, you'll need to manually upgrade. With more libraries, this becomes unmanageable.
- pip _might not point to the Python version you expect_. On some systems, pip installs packages for Python2.X.

## Virtual Environments

Python itself is in active development. Python 3.14 was released last October, with major versions (e.g., 3.14, 3.15, …) arriving once a year. Each major version receives bugfixes for two years and security updates for another three years.

Python *libraries* are developed independently by different individuals and organizations. Each maintainer decides which Python versions their library supports. This creates a compatibility issue: not all libraries are compatible with each other, and not all work with every Python version.

Example:
Version 2.0 of the numerical computing library NumPy was released in 2024 and requires at least Python 3.9. Updating NumPy to 2.x can break code in older projects that rely on NumPy's 1.x syntax.

To avoid these Problems, __each project should use its own isolated Python installation__ with its own libraries. That is what *virtual environments* provide.

A virtual environment may sound complex, but it is really just a folder holding its own local copy of Python. Here is a typical *venv* layout (`->` marks symbolic links: the Python executable isn't copied to save disk space):

```bash
.venv
├── bin                        # everything you run
│   ├── activate
│   ├── activate.csh | .fish | .ps1
│   ├── pip
│   ├── python -> python3.14
│   └── python3.14 -> /opt/homebrew/opt/python@3.14/bin/python3.14
├── include
│   └── python3.14
├── lib                        # third-party packages
│   └── python3.14
│       └── site-packages
│           ├── numpy
│           ├── pip
│           ├── scipy
│           └── …
└── pyvenv.cfg
```

## The Old-fashioned Way

Python ships with a built-in module `venv`, that lets you create virtual environments without any external tools:

```bash
python -m venv .venv                # create a virtual environment
source .venv/bin/activate           # activate the environment. `bin`→`Scripts` on Windows
pip install scipy jupyter           # install a library
jupyter lab
```

The first command creates a directory `.venv`, containing (among other tools and scripts) a Python executable at `.venv/bin/python`. (The `-m` flag tells Python to run the module _venv_, not search for a script file with that name).

Activating the environment with `source` makes commands like `python` and `pip` refer to the executables inside `.venv`.

The built-in way to install libraries is `pip`. Here, we add the most recent version of SciPy and Jupyter to the environment. Installation here means, that the files of a library are just copied into `./venv/lib/`.

Until a few years ago, venv and pip were the de facto standard setup, which is why you still see it in a lot of online tutorials. Today, however, there are better tools, and you rarely ever need to rely on venv and pip.

### Advantages and Drawbacks

- built-in: no other software needed
- all projects hosted on PyPI are available
- bad dependency resolution
- no tracking of the environment. If you delete the venv directory, the installation is lost

## Conda

Conda approaches the dependency problem by releasing curated collections of Python and packages that are compatible. It is popular in data science and machine learning. A basic setup looks like this:

```bash
conda create --name playground       # ~ python -m venv .venv
conda activate playground            # ~ source .venv/bin/activate
conda install scipy jupyter          # ~ pip install scipy
jupyter lab
```

### The conda ecosystem

There are several tools in the conda ecosystem:

- conda is a package manager
- miniconda is a command line interface to run conda
- anaconda is a distribution that contains conda and many packages for data science
- anaconda navigator is a graphical user interface that comes with anaconda

_Miniconda_ is sufficient to run the commands shown above. Conda was developed by US company Anaconda, Inc. They also release the Anaconda Navigator, which comes with the IDE Spyer. Together, they are the closest equivalent to Matlab: a large, integrated environment focused on scientific computing.

### Advantages and Drawbacks

- handles compatibility
- popular in data science fields
- limited package selection compared to PyPI
- slow environment creation and package installation (tens of seconds for a typical installation)
- managing many environments can become confusing

## UV

The cool new kid on the block is `uv`. If you are not already in a project managed otherwise, I recommend using _uv_ to manage any Python project.

```bash
uv init playground                   # ~ conda create --name playground
cd playground
uv add scipy jupyter                 # ~ conda/pip install scipy
uv run jupyter lab
```

Unlike conda, uv does not rely on curated lists of compatible versions. Instead, it determines a set of package versions that work together. It is also highly performant. Tasks that used to take minutes typically complete in just a few seconds.

Uv enforces a project structure within a directory. `init` creates the directory and sets up some boilerplate. When you `uv add` dependencies, their version constraints are recorded into a `pyproject.toml` file.

Uv creates the .venv dynamically when you fist run a Python command. The exact resolved versions are written into `uv.lock` (`*.toml` specifies which versions are allowed, and `*.lock` which were installed).

Files created by `uv init`:

```bash
playground
├── .git
│   ├── config
│   └ ┈
├── .gitignore
├── .python-version
├── uv.lock                 # tracks exactly installed dependencies
├── main.py
├── pyproject.toml          # tracks allowed dependency versions
└── README.md
```

uv initializes Git and a README.md for convenience. If you don't want them, use `uv init --bare` to only create the `*.toml` file.
`.python-version` defines which exact version of Python to use (can be changed with `uv python pin 3.X`).

`pyproject.toml` tracks metadata and defines _ranges_ of allowed versions for all libraries (it automatically sets some lower bounds to prevent installing old libraries). Below is how it looks after our installation:

```bash
# pyproject.toml

[project]
name = "playground"
version = "0.1.0"
requires-python = ">=3.7"
dependencies = [
    "jupyter>=1.1.1",
    "scipy>=1.7.3",
]
```

In summary:

- all projects hosted on PyPI are available
- simple concept: project = folder
- explicit environment tracking in pyproject.toml
- very performant (sub seconds to few seconds for typical installations)
- many more advanced tools

## Self-contained Scripts

Not every Python file needs to become a full project. If you want to run a Python file outside of a project, uv also provides a `--no-project` flag:

```python
uv run --no-project --with jupyter,scipy <file.py>
```

For small standalone scripts, Python defines a standard called *inline script metadata*, which allows dependencies in the same form as the `pyproject.toml`to be written directly into the Python file. We can combine that with a [shebang](<https://en.wikipedia.org/wiki/Shebang_(Unix)>), that instructs the system to run the script with uv. Together, that creates a self-contained script file:

```python
#!/usr/bin/env -S uv run

# /// script
# dependencies = [
#     "scipy",
# ]
# ///

import scipy.constants

print(scipy.constants.physical_constants['Newtonian constant of gravitation over h-bar c'])
```

The script can then simply be executed using `./filename.py`. Your system will run uv, and
uv will read the dependency metadata and run the script in a temporary virtual environment.

## Wrap-Up

In summary, each project should always have its own local virtual environment. With uv, this is straightforward. Using `uv add` (instead of `pip install`) guarantees that libraries are compatible and explicitly tracked.

To make this process smoother, you can define a shell shortcut (e.g., in ~.bashrc or ~.zshrsc). Below is my setup that creates a new project, installs my typically used libraries, activates the environment and starts Juypter lab:

```bash
pynit() {
    uv init --bare --no-workspace "$1"
    cd "$1"
    uv add scipy matplotlib tqdm
    uv add jupyter jupyterlab-lsp python-lsp-server
    source .venv/bin/activate
    jupyter lab
}
```

> Note: Python evolves constantly. Currently, uv is the best tool to manage virtual environments. This functionality will likely be integrated into pip in the future. I am not ( / lets not be) dogmatic about its use and will be very happy to drop it once pip is improved.

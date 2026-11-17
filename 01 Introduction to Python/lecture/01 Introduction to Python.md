# 01: Introduction to Python

## TL;DR

- Python is a powerful tool to instruct a computer to execute tasks.
- We'll have a realistic, up-to-date look at coding with LLMs.
- Weekly voluntary exercises starting next week.
- final oral exam on 15.12.2026.

## Why Python?

In the 1980s, personal computers like the Commodore 64 brought programming into living rooms. For the first time, curious non-professionals could instruct a computer to do whatever they imagined. This course follows that same spirit: will explore how non-software developers can use computers to solve problems.

Early home-computing enthusiasts would be amazed by the speed and capacity of today’s hardware, but the real revolution may be in software: many common programming problems have already been solved, so modern programming is often about combining existing tools and libraries in new ways. For Python, the Python Package Index (PyPI) provides access to a vast, open ecosystem of such building blocks that anyone can use and contribute to.

Over the past decade, Python has become one of the most popular programming language. It has grown into the default tool in many fields, notably in data science, machine learning and scientific computing.

### High- and Low-Level Languages

Below is a code example for a simple Python program that converts degrees Fahrenheit to Celsius.

```python
fahrenheit = 9 / 11
celsius = (fahrenheit - 32) / 1.8

print(celsius)
# -17.323232323232325
```

Notice what we don't do: No initialisations, no specification of variable types, and no memory management. In contrast, lower-level languages (e.g., C, C++, Rust) typically require close attention to these aspects. These languages are standard in many industries where performance and fine-grained control matter, such as robotics, embedded systems, and resource-constrained environments. Python has a different focus: Its trade-off is to sacrifice some execution speed in order to maximize development speed. Its strengths include:

- _readability_ and ease of use
- _rapid prototyping and scripting_
- _extensible_ with low-level languages whenever necessary

Python is especially a valuable tool for non-specialist programmers and for projects where productivity matters more than raw performance, but it's capable enough to scale to highly performant applications.

### Python

Let's look at a richer example. Say we're interested in understanding how large language models improved in programming over time. We find a [resource](https://evals.report/benchmarks/swe-bench-pro) online, but we want to see this tabular data visualised:

```python
import pandas as pd
import matplotlib.pyplot as plt


# parse data
df = pd.read_html(
    'https://evals.report/benchmarks/swe-bench-pro',
    storage_options={'User-Agent': 'Mozilla/5.0'},
)[0]

# setup data frame
df['Date'] = pd.to_datetime(df['Date'])
df['Score'] = df['Score↓'].str.rstrip('%').astype(float)
df = df.sort_values('Date')
df['Best so far'] = df['Score'].cummax()

# visualisation
plt.scatter(df['Date'], df['Score'], alpha=0.4, color='black')
plt.step(df['Date'], df['Best so far'], where='post', color='red')

plt.ylim([0, 100])
plt.xlabel('Release date')
plt.ylabel('SWE-bench Pro (%)')
plt.title('LLM software engineering performance')
plt.show()
```

![LLM software engineering performance](media/01%20swe_performance.png "Time evolution of LLM software engineering performance")

In these few lines of code, we parse data from a website, sort it, perform calculations and visualise it. This is one of Python’s core strengths: its community has built an immense set of libraries that do much of the complicated work. What is left for us is to assemble these existing building blocks.

## Course

The official goal of this course is for you to __learn to use Python__. My unofficial "secret" goal is to __get you hooked__ on the addictiveness of programming. I believe this is the most effective and most enjoyable way to learn programming.
The course has __12 voluntary exercises__. They allow you to internalise the concepts we visit during the lectures. The course awards 2 ECTS, so you should expect to invest about 3 hours per exercise. For those who are interested, I will offer __voluntary tutorials__ after each lecture, where we can discuss open questions.
Finally, you will be evaluated in an __oral exam__ at the end of the semester.

### Lecture

This course aims to prepare you for using Python for real world tasks. Python is a high-level language and abstracts away a lot of underlying setup (for example, you don't need to declare whether a variable holds an integer or a floating-point number, and Python handles arithmetic between them.)
This course follows that philosophy: We will learn the fundamentals to use the language appropriately, and will explore tools for using Python in data processing, visualisation and generally "to get things done". We won't go into computer science rabbit holes; we won't learn about CPython, bytecode, endianness, integer representation or hardware-level details.

The course is structured into five topics:

1. _Syntax and core features_ of the language: Python's clean and simple design principles allow us to cover this within one lecture.
2. _Set up of project-specific virtual environments_: A messy use of Python installations is a large issue I regularly observe. We will learn how to set up project-specific environments to keep installations clean and reproducible.
3. _Programming fundamentals:_ Creating _classes,_ handling _exceptions and organising code_ into packages. These are the building blocks for well-organized code.
4. _Applications:_ Established libraries for _numerical and scientific data processing,_ modern _visualisation_ tools and user interfaces, _etc._
5. _Coding with LLMs_: How to employ them (safely), and what you can and can't expect from today's free and paid models.

The three initial points will take us about half of the semester, and with that preparation done, we'll learn the exciting stuff in the second half. In detail, the 14 lectures are:

1. Introduction
2. Syntax
3. Virtual Environments
4. Objects and Classes
5. Exceptions
6. Modules and Packages
7. Numerical Computing
8. Data Visualisation
9. Scientific Tools
10. Coding with LLMs
11. Coding with LLMs
12. Automation
13. User Interfaces
14. Speed Up

This lecture comes with its own narrative script, which I hand out as a Markdown file.

> Note: Markdown is a very simple markup language, with the goal of being human readable without any processing. It is standard in many places, for example as README files on GitHub, and typically also how large language models format text. You can open markdown file with any text editor. Personally, I recommend checking out [Obsidian](https://obsidian.md/). If you want a PDF or any other format, `pandoc` can convert markdown files.

I also hand out the slides. These are automatically generated from the lecture notes. They follow exactly the same structure, just without the bulk of the verbose text.

## Exam

The course will be graded in a __15-minute oral exam__ on __15.12.2026__. You will work __on your own device__ (with an alternative device available if needed).
The course is about using Python in practice, therefore the exam may include __writing code and structural / organisational tasks__ around that, such as setting up Python environments or working with notebooks.

## Large Language Models

We've seen in the example above how LLM-based coding solutions have improved over the last year. For example, even free models are able to solve the provided exercises. So…

### Should you still learn Python?

Given this, should you even bother learning Python? I’d argue yes, for a couple of reasons:

- _Design decisions:_ You _need to know what is possible_ in order to create the appropriate tools for the task.
- _Simplicity:_ If you know what a program should do, Python can be _the simplest language to express_ it.
- _Enjoyment_: Programming can be a lot of fun, and we should be careful not to let computers take over the enjoyable parts of our work.
- _Practicality:_ Some companies prohibit the use of coding AI for _security, compliance,_ or _intellectual property_ reasons.
- _Responsibility:_ LLM-based coding AIs come with significant _environmental costs, ethical concerns,_ and _high financial expenses_.
- _Hype_: Chill and let's see where this leads.

We’ll take a closer look at these issues, and learn where using these tools is appropriate, in Lecture 10 and 11.

## Running Code

Next week we will dive straight into the syntax of Python; I want you to start coding quickly. But first, how do we actually run Python code?

Python is a program (an interpreter) that reads your source code and executes the instructions line by line.

There are three common ways to run Python:

- by _executing a script file_ containing your code
- in a _REPL (Read-Eval-Print-Loop)_, an interactive prompt
- in a _notebook_, a modern take on the REPL that lets you mix code text and visualisations.

### Source Files

The standard way to run code is to save it into a file with the extension `.py`, and tell `python` to execute it:

```bash
python plot_benchmark.py
```

Of course, you need Python installed first. To do this properly, it is best practice to create a dedicated virtual environment for each project. We will learn how to set this up in Lecture 3.

### Interactive Modes

If we run Python without specifying a file, it launches into an interactive shell (the Read-Eval-Print-Loop, REPL). Here, you can type and run code line by line.

```bash
python
```

```python
Python 3.14.7 (main, Aug  5 2026, 10:29:49) [Clang 21.0.0 (clang-2100.1.1.101)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> earth_radius = 6_378_137
>>> pi = 3
>>> 2 * earth_radius * pi / 1000
38268.822
```

This can be useful for quick experiments but is not very user-friendly. So, over the last decade, Notebooks have become popular. They combine aspects of the REPL and source files. A notebook is made up of a sequence of editable cells, where each cell can contain either markdown or Python code. Importantly, objects persist across all cells. This makes notebooks a great tool for prototyping code and for data visualization. In contrast to the two previous modes, notebooks are not a core capability of Python, but are implemented as a Python library. The standard notebook-based tool is _Jupyter_. You can run it with:

```bash
jupyter lab
```

Notebooks are saved with the `.ipynb` extension, and many integrated development environments (e.g. VSCodium or PyCharm) support them directly. They can also be run in a web browser: JupyterLite runs notebooks entirely in the browser (https://jupyter.org/try-jupyter/lab/), while platforms such as [Google Colab](https://colab.research.google.com) run them in a hosted environment.

### Note on the Command Line

The command line will be a central tool for using Python. To use it:

- _macOS / Linux:_ You're all set, a _terminal_ app is preinstalled.
- _Windows:_ The simplest option is to install _Git Bash_.

If you use Visual Studio Code (or better VSCodium) on Windows, you can select Git Bash in the integrated terminal, so you don't need to work in a separate Git Bash application.

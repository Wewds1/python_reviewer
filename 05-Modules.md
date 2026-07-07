# Lesson 5: Modules

## 1. Learning objectives

By the end of this lesson you should be able to:

- Import standard library modules and use aliases sensibly
- Explain the difference between a module and a package
- Create your own module and import it from another file
- Set up and use a virtual environment, and explain why you'd never skip this step on a real project
- Install packages with pip and manage them through a requirements.txt file

## 2. Prerequisites

Lessons 1 through 4. Modules are where you start organizing everything you've learned across multiple files instead of one script.

## 3. Introduction

Every real Python project eventually outgrows a single file. Modules and packages are how Python lets you split code across files while still being able to use it all together, and pip and virtual environments are how you pull in code other people have already written instead of reinventing it. This lesson is more about tooling and project structure than new language syntax, but it's exactly the stuff that separates someone who's done a few tutorials from someone who's worked on an actual codebase.

## 4. Theory

A module is just a `.py` file. That's it. The moment you write `import math`, you're importing a module, a file called `math` (implemented in C for the standard library, but conceptually the same idea) that has functions and constants defined in it. A package is a directory of modules with an `__init__.py` file (which can be empty) that tells Python "treat this folder as a package you can import from."

```python
import math
print(math.sqrt(16))  # 4.0

from math import sqrt
print(sqrt(16))  # 4.0, no need to prefix with math.

import math as m
print(m.sqrt(16))  # aliasing, common for long or frequently-used module names
```

## 5. Why this concept exists

Without modules, every project would either be one enormous file, or you'd have to copy-paste shared code between files, which is exactly the problem functions solved at a smaller scale. Modules extend that same idea, don't repeat yourself, to the level of entire files and libraries. Packages, and package managers like pip, exist because most problems you'll face have already been solved by someone else, and reinventing a well-tested JSON parser or HTTP client from scratch would be a poor use of anyone's time.

## 6. How Python implements it internally

When you write `import math`, Python searches a list of directories (found in `sys.path`) for a file or package matching that name, loads it, executes the module's top-level code exactly once, and caches the resulting module object in `sys.modules`. Every subsequent `import math` anywhere else in the program just reuses that cached object instead of re-running the file. This is why you'll sometimes see people put debugging `print()` statements at the top level of a module to check whether it's actually being loaded, and why it only prints once even if ten other files import it.

## 7. Real-world analogy

A module is a toolbox you bought instead of building yourself. You don't need to know how the manufacturer forged the wrench, you just need to know it's called `wrench` and it fits the bolt. `import module_name` is walking into the garage and grabbing that specific toolbox off the shelf. `from module_name import specific_tool` is reaching into the box and pulling out just the one tool you need, so you don't have to keep saying "toolbox dot" every time you use it. A virtual environment is having a separate, clearly labeled toolbox for each project, so the oddball metric wrench you bought for one job doesn't end up loose in the same box as the imperial one another project needs.

## 8. Enterprise use cases

Real projects are organized into packages by responsibility, a `validators` package, a `reports` package, a `data_access` package, precisely so multiple people can work on different parts without stepping on each other. Virtual environments matter enormously the moment you have more than one project on your machine, or more than one person on a team; without them, installing a newer version of a library for one project can silently break a different project that needed the old version. A `requirements.txt` file is how a team, or a deployment pipeline, knows exactly which packages and versions a project needs to run, which is non-negotiable for anything going to production.

## 9. Syntax

**Import styles:**

```python
import os
import sys
from datetime import datetime
from collections import Counter, defaultdict
import numpy as np  # common convention for well-known aliases
```

**Creating and importing your own module:**

```python
# file: helpers.py
def format_currency(amount):
    return f"${amount:,.2f}"

# file: main.py
import helpers
print(helpers.format_currency(1500))  # $1,500.00

# or:
from helpers import format_currency
print(format_currency(1500))
```

**Package structure:**

```
my_project/
├── main.py
└── utils/
    ├── __init__.py
    ├── validators.py
    └── formatters.py
```

```python
# from main.py:
from utils.formatters import format_currency
from utils.validators import is_valid_email
```

**Virtual environments and pip, from the terminal:**

```bash
python -m venv venv           # create a virtual environment named "venv"
source venv/bin/activate      # activate it (macOS/Linux)
venv\Scripts\activate         # activate it (Windows)

pip install requests          # install a package into the active environment
pip freeze > requirements.txt # save exact installed versions

pip install -r requirements.txt  # install everything listed, e.g. on a new machine
```

## 10. Step-by-step examples

**Easy — using a standard library module:**

```python
import random
print(random.randint(1, 10))
```

**Medium — writing and importing your own module:**

```python
# file: math_helpers.py
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

# file: main.py
from math_helpers import is_prime
print(is_prime(17))  # True
```

**Hard — a small package with a working `__init__.py`:**

```python
# file: shop/__init__.py
from .pricing import apply_discount
from .inventory import check_stock

# file: shop/pricing.py
def apply_discount(price, percent):
    return price * (1 - percent / 100)

# file: shop/inventory.py
def check_stock(item, stock_levels):
    return stock_levels.get(item, 0) > 0

# file: main.py
from shop import apply_discount, check_stock
print(apply_discount(100, 20))
```

The `__init__.py` here re-exports functions from the submodules, so `main.py` can import directly from `shop` instead of needing to know the internal file layout. That pattern, a clean public interface hiding the internal structure, is worth remembering; it's exactly how well-designed packages are put together.

## 11. Common mistakes

**Forgetting to activate the virtual environment** before installing packages, which installs them globally instead, defeating the entire purpose.

**Circular imports:** module A imports from module B, and module B imports from module A. Python will raise an `ImportError` or produce confusing partially-initialized modules. The fix is almost always restructuring, pulling shared code into a third module both can depend on, rather than having two modules depend on each other directly.

**Naming your own file the same as a standard library module,** for example `datetime.py` in your project root. Python's import system will find your file first and shadow the real `datetime` module, causing baffling errors elsewhere in code that expected the real one.

**Installing packages without a `requirements.txt`,** which works fine until someone else tries to run the project and has no idea what to install, or worse, until you reinstall your own machine and can't remember either.

## 12. Debugging tips

If `import some_package` fails with `ModuleNotFoundError`, check first whether your virtual environment is actually activated (this is the single most common cause). If two modules seem to be importing each other and something is behaving strangely, suspect a circular import before anything else. `pip list` shows you everything currently installed in the active environment, which is the fastest way to check whether a package actually got installed where you think it did.

## 13. Best practices

Always use a virtual environment per project, no exceptions, even for small scripts; the habit is worth more than the individual case. Keep `requirements.txt` up to date whenever you add a dependency. Group your standard library imports, third-party imports, and local imports into three separate blocks at the top of a file, in that order, which is the PEP 8 convention and makes it immediately obvious what's built-in versus something you'll need to install. Give modules short, lowercase, descriptive names, and avoid shadowing standard library names.

## 14. Performance considerations

Importing a module executes its top-level code exactly once and caches the result, so importing the same module in ten different files costs you one load, not ten. Import statements at the top of a file have negligible ongoing cost after that first load; the only time import overhead is worth thinking about is when importing extremely heavy libraries inside a function that gets called in a tight loop, where you'd want the import to happen once outside the loop instead.

## 15. Code style (PEP 8)

Imports go at the top of the file, one import per line for `import x` style statements. Group them: standard library first, then third-party packages, then your own local modules, with a blank line between each group. Avoid wildcard imports (`from module import *`); they make it unclear where a given name actually came from, which is exactly the kind of ambiguity that slows down a code review.

## 16. Interview questions with model answers

**Q: What's the difference between a module and a package?**

A module is a single `.py` file. A package is a directory of modules that includes an `__init__.py` file, which lets Python treat the whole directory as something importable. The interviewer is checking that you know this isn't just terminology, a package can bundle many modules together and expose a clean interface through its `__init__.py`.

**Q: Why use a virtual environment instead of installing packages globally?**

Different projects often need different, sometimes conflicting, versions of the same package. A virtual environment isolates each project's dependencies so installing something for one project can't silently break another. It also makes a project reproducible: anyone can create a fresh environment and install the exact versions listed in `requirements.txt`.

**Q: What causes a circular import, and how would you fix one?**

It happens when two modules import from each other, directly or through a chain. Python can end up with a module that's only partially initialized at the point the other one tries to use it. The fix is usually to move the shared logic both modules need into a separate third module that each of them can import from independently, rather than having them depend on each other.

## 17. Knowledge check

1. What file marks a directory as a Python package?
2. What does `pip freeze` do, and why would you redirect its output into a file?
3. What's the practical difference between `import math` and `from math import sqrt`?
4. Why is `from module import *` discouraged?

## 18. Hands-on exercises

**Easy**

1. Import the `random` module and use it to print a random integer between 1 and 100.
2. Create a file `greetings.py` with a function `say_hello(name)`, then import and call it from a separate `main.py`.
3. Use `from datetime import date` to print today's date.

**Medium**

4. Create a small package `text_tools/` with two modules, `cleaners.py` (a function that strips whitespace and lowercases text) and `counters.py` (a function that counts words in a string), and import both from a `main.py` at the project root.
5. Set up a virtual environment, install the `requests` package into it, and generate a `requirements.txt` from it.
6. Deliberately create a circular import between two small modules, observe the error, and then fix it by extracting the shared function into a third module.

**Hard**

7. Build a package with an `__init__.py` that re-exports selected functions from two internal submodules, so that code importing the package doesn't need to know the internal file structure, following the `shop` example from this lesson.
8. Write a short script that imports a standard library module inside a function rather than at the top of the file, and explain in a comment why this is sometimes done deliberately (hint: think about optional dependencies and startup time) even though it goes against the usual PEP 8 guidance.

## 19. Stretch challenge

Take the capstone-style mini project you'll build later in this module and, before writing any of its logic, design its folder structure as a package with at least three submodules split by responsibility (for example, `data.py`, `validation.py`, `reporting.py`). Write the `__init__.py` so that `main.py` only ever needs one or two import lines to access everything it needs. Getting this structure right before writing the logic is a genuinely useful habit to build now, while the stakes are low.

## 20. Summary

A module is a file, a package is a folder of modules with an `__init__.py`, and both exist so code can be organized and reused instead of duplicated. Virtual environments and pip are the tooling that make this practical across real projects and real teams: isolated dependencies per project, and a `requirements.txt` that lets anyone reproduce your setup exactly. None of this is exciting, but skipping it is exactly how "works on my machine" problems happen, and avoiding those is most of what makes a codebase enterprise-ready rather than just a personal script.

## 21. Additional resources

- [Python official docs: Modules](https://docs.python.org/3/tutorial/modules.html)
- [Python official docs: venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html)
- [pip documentation: Requirements Files](https://pip.pypa.io/en/stable/user_guide/#requirements-files)

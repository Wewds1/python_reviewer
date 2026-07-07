# Lesson 4: Functions

## 1. Learning objectives

By the end of this lesson you should be able to:

- Write functions with positional, keyword, and default arguments, and explain the difference between all three
- Use `*args` and `**kwargs` correctly, and know when reaching for them is appropriate versus overkill
- Explain local versus global scope and the LEGB rule that governs how Python resolves names
- Write clean lambda functions for the narrow cases they're actually good for
- Write proper docstrings and basic type hints that make a function self-documenting

## 2. Prerequisites

Lessons 1 through 3. Functions are where variables, data types, and control flow all get packaged into something reusable, so you need all three.

## 3. Introduction

A function is how you stop copy-pasting the same six lines of code every time you need to do a thing. That sounds almost too simple to dedicate a whole lesson to, but function design, what arguments to accept, what to return, how much a single function should be responsible for, is one of the biggest differences between code that's pleasant to work in and code that makes you want to quit. This lesson covers the mechanics and the judgment calls together.

## 4. Theory

A function bundles a block of code under a name, optionally takes input (parameters), and optionally hands back output (a return value). Once defined, you can call it as many times as you want without rewriting the body.

```python
def calculate_discount(price, percent):
    return price * (percent / 100)
```

Here, `price` and `percent` are parameters; when you call `calculate_discount(100, 20)`, `100` and `20` are the arguments. That distinction, parameter is the name in the definition, argument is the value at the call site, comes up in interviews more than you'd expect.

## 5. Why this concept exists

Without functions, any change to shared logic means hunting down and fixing every copy-pasted instance of it, and missing one is how bugs get shipped to production. Functions give you one place to fix a mistake or improve an algorithm, and everywhere that calls it benefits immediately. They're also how you make code testable: you can call a function with known inputs and check the output, which is nearly impossible to do cleanly with a long unbroken script.

## 6. How Python implements it internally

When Python hits a `def` statement, it doesn't run the function body. It creates a function object and binds it to the given name, the same name-to-object binding covered in Lesson 1. The body only executes when the function is actually called, at which point Python creates a new local namespace, or scope, for that call, populates it with the arguments, runs the body against that namespace, and discards it when the function returns (unless something outside kept a reference to something created inside, like a closure, which is beyond this lesson).

This is also why default argument values are evaluated exactly once, at definition time, not on every call, which is precisely the mechanism behind the mutable-default-argument bug from Lesson 2.

## 7. Real-world analogy

A function is a recipe card, not a specific meal. The recipe says "take flour, sugar, and eggs, do these steps, get a cake." You can run that recipe a hundred times with slightly different ingredient amounts (arguments) and get a hundred cakes, without rewriting the recipe each time. A recipe with a fixed default ingredient list, "serves 4 unless you say otherwise," is a default argument. A recipe that accepts "and whatever else you want to throw in" is `**kwargs`.

## 8. Enterprise use cases

Nearly every reusable piece of business logic in a real codebase, calculating tax, validating an email format, formatting a currency value for a report, lives in a function specifically so it's defined once and tested once. Functions with clear, typed signatures and docstrings are also what make a codebase navigable for a new hire; being able to read a function's name, parameters, and docstring and understand what it does without reading the implementation is the entire point of good function design, and it's exactly what a code reviewer at a firm like PwC is checking for.

## 9. Syntax

**Basic definition and default arguments:**

```python
def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

greet("Alex")                  # "Hello, Alex!"
greet("Alex", "Hi")             # positional
greet("Alex", greeting="Hi")    # keyword — same result, more explicit
```

**Positional vs. keyword arguments:**

```python
def book_flight(origin, destination, seat="economy"):
    return f"{origin} to {destination}, {seat}"

book_flight("NYC", "LON")                     # positional
book_flight(origin="NYC", destination="LON")  # keyword
book_flight("NYC", destination="LON")         # mixed, positional first
```

**\*args and \*\*kwargs:**

```python
def total(*numbers):          # collects any number of positional args into a tuple
    return sum(numbers)

total(1, 2, 3)      # 6
total(4, 5, 6, 7)   # 22

def build_profile(**details):  # collects keyword args into a dict
    return details

build_profile(name="Sam", role="engineer")
# {'name': 'Sam', 'role': 'engineer'}
```

**Scope:**

```python
count = 0  # global

def increment():
    global count  # without this line, the function would create a new local variable instead
    count += 1

increment()
print(count)  # 1
```

**Lambda functions:**

```python
square = lambda x: x * x
square(5)  # 25

# more realistic use: as a sort key
people = [("Sam", 34), ("Alex", 28)]
people.sort(key=lambda person: person[1])
```

**Docstrings and type hints:**

```python
def calculate_discount(price: float, percent: float) -> float:
    """Return the discount amount for a given price and percentage."""
    return price * (percent / 100)
```

## 10. Step-by-step examples

**Easy — a function with a default argument:**

```python
def power(base, exponent=2):
    return base ** exponent

print(power(5))     # 25, uses the default exponent
print(power(5, 3))  # 125
```

**Medium — \*args used to build a flexible sum function:**

```python
def total_cost(*prices):
    return sum(prices)

print(total_cost(9.99, 4.50, 12.00))
```

**Hard — LEGB in action, showing how Python resolves a name across scopes:**

```python
x = "global"

def outer():
    x = "enclosing"

    def inner():
        x = "local"
        print(x)  # local

    inner()
    print(x)  # enclosing

outer()
print(x)  # global
```

LEGB stands for Local, Enclosing, Global, Built-in, the order Python checks when it looks up a name. Each `print(x)` above finds a different `x` because each one is checked from a different scope, and Python always looks in the nearest enclosing scope first before working outward.

## 11. Common mistakes

**Forgetting that a function without `global` creates a new local variable instead of modifying the outer one:**

```python
count = 0

def increment():
    count += 1  # UnboundLocalError — Python sees the assignment and treats count as local

increment()
```

Python decides a variable is local to a function if it's assigned anywhere in that function's body, even before the line that does the assigning runs. That's why the fix isn't just moving code around, it's explicitly declaring `global count`.

**Confusing `*args` with actually needing a list parameter.** If a function will only ever be called with one collection of items, just accept a list. `*args` is for genuinely variable numbers of separate arguments, not a substitute for a normal parameter.

**Overusing lambda for anything with real logic.** A lambda should be small enough to read in one glance. If you're nesting conditionals inside a lambda, write a normal named function instead; it'll be easier to test and to read six months from now.

## 12. Debugging tips

`UnboundLocalError` almost always means you're assigning to a variable inside a function that Python thinks should be local, when you meant to modify a variable from an outer scope, missing `global` or `nonlocal`. If a function isn't returning what you expect, check whether it has a `return` statement at all; a function with no `return` implicitly returns `None`, which is an extremely common source of "why is my variable None" bugs.

## 13. Best practices

Keep functions small and focused on one task; if you're struggling to name a function without using "and," it's probably doing two things and should be split. Use default arguments for genuinely optional parameters, never for mutable objects. Prefer explicit named parameters over `*args`/`**kwargs` unless you specifically need the flexibility, explicit signatures are easier to read and to get autocomplete for. Add a docstring to every function whose purpose isn't obvious from its name alone.

## 14. Performance considerations

Function calls in Python have real overhead compared to inline code, since each call sets up a new local scope. This essentially never matters at the scale of scripts in this module; it only becomes relevant in tight, high-frequency loops in performance-critical code, at which point inlining or using built-in functions (which are implemented in C) can matter. Don't let this concern override function design, readability wins by a wide margin at this stage.

## 15. Code style (PEP 8)

Two blank lines before and after a top-level function definition. Function names in `snake_case`. Keep the signature on one line if it reasonably fits; if a function has many parameters, break them across multiple lines, one per line, with consistent indentation. Type hints go directly in the signature (`def f(x: int) -> str:`), not in a comment.

## 16. Interview questions with model answers

**Q: What's the difference between `*args` and `**kwargs`?**

`*args` collects extra positional arguments into a tuple. `**kwargs` collects extra keyword arguments into a dictionary. Both let a function accept a variable number of arguments, but they handle positional versus named arguments differently, and you can use both in the same signature (`def f(*args, **kwargs)`), with `*args` always coming first.

**Q: Explain the LEGB rule.**

It's the order Python searches when resolving a variable name: Local scope first, then any Enclosing function scope, then the module's Global scope, then Python's Built-in names last. The interviewer wants to see that you understand scope resolution isn't just "local versus global," there can be layers in between with nested functions.

**Q: Why does this raise an error, and how do you fix it?**

```python
counter = 0

def bump():
    counter += 1
    return counter
```

Ideal answer: Python treats `counter` as a local variable inside `bump` because it's assigned within the function body, so the line `counter += 1` tries to read a local variable before it's been assigned anything, causing `UnboundLocalError`. The fix is adding `global counter` inside the function, or better, restructuring the code to avoid mutating global state from inside a function at all, which is generally the more senior answer.

## 17. Knowledge check

1. What's the difference between a parameter and an argument?
2. What does a function return if it has no explicit `return` statement?
3. Why does `def f(x, values=[]):` cause bugs across repeated calls?
4. In what order does Python search for a name under the LEGB rule?

## 18. Hands-on exercises

**Easy**

1. Write a function `is_even(n)` that returns `True` or `False`.
2. Write a function `greet(name, title="Mx.")` with a default argument, and call it both with and without providing the title.
3. Write a one-line lambda that doubles a number, and use it in a call to `map()` over a list of five numbers.

**Medium**

4. Write a function `summarize(*scores)` that accepts any number of scores and returns their average.
5. Write a function `build_record(**fields)` that accepts arbitrary keyword arguments and returns them as a formatted string, one `key: value` pair per line.
6. Write a function that demonstrates `UnboundLocalError` on purpose, with a comment explaining why it happens, then fix it using `global`.

**Hard**

7. Write a function `apply_discount(price, percent=10, *, rounded=True)` that uses a keyword-only argument (the `*` forces `rounded` to be passed by name) and returns the discounted price, rounded to two decimals when `rounded` is `True`.
8. Write three nested functions (`outer`, `middle`, `inner`) each defining a variable named `value`, and print `value` from within `inner` after printing it from each of the other two, to demonstrate the LEGB rule concretely.

## 19. Stretch challenge

Write a function `memoize(func)` that takes another function as an argument and returns a new function which caches results in a dictionary, keyed by the arguments passed in, so repeated calls with the same arguments skip recomputation and return the cached result instead. Test it against a deliberately slow function (one with a `time.sleep()` call inside) and confirm the second call with the same argument returns instantly. This is your first real taste of a decorator, even though we haven't named that topic yet, and it's worth sitting with.

## 20. Summary

Functions are how you turn "code that runs once" into "code you can trust and reuse." The mechanics, positional versus keyword arguments, defaults, `*args`, `**kwargs`, are all in service of one goal: a clear, predictable contract between the function and whoever calls it. Scope determines what a function can see and change, and the LEGB rule is the exact order Python checks. Keep functions small, name them well, and don't let a lambda grow past what fits comfortably on one line.

## 21. Additional resources

- [Python official docs: Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)
- [PEP 3107 / PEP 484 — Function Annotations and Type Hints](https://peps.python.org/pep-0484/)
- [Real Python: Python Scope & the LEGB Rule](https://realpython.com/python-scope-legb-rule/)

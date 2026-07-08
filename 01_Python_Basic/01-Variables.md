# Lesson 1: Variables

## 1. Learning Objectives

By the end of this lesson you should be able to:

- Create variables in Python and explain what actually happens in memory when you do
- Follow Python naming conventions without having to think about them
- Explain dynamic typing, and why Python doesn't make you declare a type up front
- Tell the difference between a variable, a constant, and an object reference
- Spot the classic beginner mistakes around variable scope and mutable defaults before they bite you in a code review

## 2. Prerequisites

None. This is the first real lesson. You should have Python installed and a terminal or VS Code open, ready to run code.

## 3. Introduction

Every program needs somewhere to put data while it's working on it. That's all a variable is: a name that points at a value. It sounds trivial, and typing `x = 5` is trivial. What's not trivial, and what separates someone who can write Python from someone who understands Python, is knowing what that line of code actually does under the hood, and why Python's approach to it is different from languages like Java or C.

## 4. Theory

In Python, a variable is a label attached to an object, not a labeled box that holds a value. This is the single most important mental model shift for anyone coming from a language like Java or C.

```python
x = 5
```

This doesn't create a box called `x` and put `5` inside it. It creates an integer object `5` somewhere in memory, and then makes the name `x` point at it. If you write `y = x`, you don't get a copy of `5`. You get a second name pointing at the exact same object.

You can prove this to yourself:

```python
x = 5
y = x
print(id(x) == id(y))  # True — same object in memory
```

`id()` returns the memory address of an object (CPython specific, but reliable enough to demonstrate the point). Two names, one object.

## 5. Why this concept exists

Languages like C make you declare a type before you use a variable (`int x;`) because the compiler needs to know exactly how many bytes to reserve. Python skips that step on purpose. The tradeoff is real: you lose some safety net (a typo that creates a new variable instead of erroring out), but you gain speed of writing and reading code, especially for the kind of glue-code, data-wrangling work that makes up a lot of real consulting work. Python decided that for most day-to-day programming, the compiler catching your type mistakes matters less than you being able to write three lines instead of six.

## 6. How Python implements it internally

Under the hood, CPython keeps a dictionary-like structure called a namespace that maps names to objects. When you run `x = 5` at the top level of a script, CPython adds an entry to the module's namespace: the string `"x"` maps to a reference to the integer object `5`.

Small integers (roughly -5 to 256) and short strings are actually cached and reused by CPython as an optimization, which is why `id()` comparisons on small numbers can look surprising if you don't know this is happening. Don't rely on this behavior in real code. It's an implementation detail of CPython, not a guarantee of the language.

## 7. Real-world analogy

Think of it like sticky notes on a filing cabinet, not folders inside it. The filing cabinet drawer holds the actual document (the object, `5`). A sticky note labeled "x" gets stuck to that drawer. If you write `y = x`, you're not making a photocopy of the document, you're sticking a second note, labeled "y", onto the exact same drawer. Move the drawer (change the object), and both notes still point to wherever it ends up. Peel off the "x" note and stick it on a different drawer (`x = 10`), and "y" still points at the original one.

## 8. Enterprise use cases

In practice, variable naming is where code review time actually goes. A function with parameters named `d`, `l1`, `tmp2` will get flagged in any serious PwC or enterprise code review, not because it's wrong, but because six months from now nobody, including the original author, will remember what `tmp2` was for. Naming things well is a genuinely underrated skill and it's one of the fastest ways to look like you know what you're doing.

Constants (things like `MAX_RETRY_ATTEMPTS = 5` or `DEFAULT_TIMEOUT_SECONDS = 30`) show up constantly in configuration files, retry logic for API calls, and validation rules for client data. Getting into the habit of naming these clearly instead of scattering magic numbers through your code is a habit interviewers actively look for.

## 9. Syntax

Basic assignment:

```python
age = 28
name = "Priya"
is_active = True
```

Multiple assignment on one line:

```python
x, y, z = 1, 2, 3
```

Chained assignment (careful with this one, see Common Mistakes):

```python
a = b = c = 0
```

Naming rules Python actually enforces:

- Must start with a letter or underscore, not a digit
- Can contain letters, digits, and underscores after that
- Case-sensitive: `total` and `Total` are different names
- Cannot be a reserved keyword (`class`, `if`, `for`, and so on)

Naming conventions the community enforces (PEP 8, not the interpreter):

- `snake_case` for variables and functions: `total_price`
- `UPPER_SNAKE_CASE` for constants: `MAX_USERS`
- `PascalCase` reserved for class names: `CustomerRecord`

## 10. Step-by-step examples

**Easy — basic assignment and printing:**

```python
first_name = "Alex"
last_name = "Kim"
print(first_name, last_name)
```

**Medium — multiple assignment used to swap values (a genuinely useful Python trick):**

```python
a = 5
b = 10
a, b = b, a
print(a, b)  # 10 5
```

Most languages need a temporary variable to swap two values. Python's tuple unpacking does it in one line, which is a small thing that tends to impress people who don't know Python well and comes up constantly in real code.

**Hard — demonstrating that reassignment doesn't mutate the original object:**

```python
x = [1, 2, 3]
y = x
y.append(4)
print(x)  # [1, 2, 3, 4] — because x and y point to the same list

y = [9, 9, 9]  # now y points somewhere new
print(x)  # still [1, 2, 3, 4] — x was never touched
```

That last example is the whole "variables are labels, not boxes" idea in four lines. Sit with it until it feels obvious, because it's the source of a huge fraction of bugs beginners hit later with lists and dictionaries.

## 11. Common mistakes

**Chained assignment with mutable objects.** This one catches people constantly:

```python
a = b = []
a.append(1)
print(b)  # [1] — surprise! a and b are the same list object
```

If you meant two separate empty lists, you needed `a = []` and `b = []` on separate lines.

**Using a variable before assigning it.** Python won't let you, but the error message trips people up the first time:

```python
print(total)  # NameError: name 'total' is not defined
total = 0
```

**Shadowing built-in names.** Python will let you do this, which is exactly the problem:

```python
list = [1, 2, 3]  # now the built-in list() function is gone in this scope
```

This runs fine and then breaks something completely unrelated fifty lines later when you try to call `list(range(10))`.

## 12. Debugging tips

If a variable has a value you didn't expect, check whether something else has a reference to the same object and mutated it. The `id()` function is your friend here; if two names return the same id, they're the same object, and mutating through one affects the other.

`NameError` almost always means either a typo in the variable name, or you're trying to use a variable outside the scope where it was defined (loops and function bodies are the usual suspects, more on this in the Functions lesson).

## 13. Best practices

Name things for what they represent, not for their type. `user_list` is worse than `users`, because if you later switch from a list to a set, the name is now lying to you. Favor clarity over brevity: `subtotal_after_discount` beats `s` every time, even though it's more typing. Avoid single-letter names outside of very short-lived loop counters (`i`, `j` in a tight loop is fine; `i` as a variable that lives for fifty lines is not).

## 14. Performance considerations

Variable assignment itself is essentially free, a pointer update. Where performance actually matters is what you're assigning: reassigning a name to a new large object (a big list, say) doesn't free the old object until nothing else references it, which is a detail worth knowing when you're dealing with memory-sensitive code, but rarely matters for the kind of scripts this module covers.

## 15. Code style (PEP 8)

- Use `snake_case`, always
- One assignment per line unless you're doing genuine tuple unpacking (`x, y = 1, 2`) — avoid chained assignment for anything mutable
- Add a blank line to visually separate a block of related variable declarations from the code that uses them
- No spaces around `=` inside function call keyword arguments (`func(x=5)`), but spaces around `=` for normal assignment (`x = 5`)

## 16. Interview questions with model answers

**Q: What's the difference between a variable in Python and a variable in Java?**

A good answer covers that Java variables have a declared, fixed type and the compiler enforces it, while Python variables are just names bound to objects, and the same name can be rebound to a completely different type of object at any point. The interviewer is checking whether you understand dynamic typing isn't "no types," it's "types belong to objects, not to names."

**Q: What does this print, and why?**

```python
a = [1, 2]
b = a
a = [3, 4]
print(b)
```

Ideal answer: `[1, 2]`. The second line makes `b` point at the same list as `a`. The third line doesn't change that list, it rebinds the name `a` to point at a brand new list. `b` never moved, so it still points at the original.

**Q: Why does `a = b = []` cause bugs that `a = []` followed by `b = []` doesn't?**

The interviewer wants to hear that chained assignment binds every name to the same single object, so mutating through one name shows up through the other, which is almost never what someone intended when they write it.

## 17. Knowledge check

1. True or false: `x = 5; y = x` copies the value `5` into a new memory location for `y`.
2. What will `a = b = {}` followed by `a["key"] = "value"` do to `b`?
3. Which of these is a valid Python variable name: `2total`, `_total`, `total-price`?
4. Why is `list = [1, 2, 3]` a bad idea even though Python allows it?

(Answers are in the instructor notes, but genuinely try these before checking.)

## 18. Hands-on exercises

**Easy**

1. Create three variables holding your name, age, and whether you're currently employed. Print all three on one line.
2. Swap the values of two variables in a single line of code.
3. Create a constant `TAX_RATE` set to `0.08` and use it to calculate tax on a `price` of `49.99`.

**Medium**

4. Given `a = [1, 2, 3]` and `b = a`, write code that modifies `b` in a way that also changes `a`, then write code that modifies `b` in a way that does not.
5. Write a short script using multiple assignment to initialize three counters (`errors`, `warnings`, `passed`) to zero on one line.
6. Explain, in a comment above the code, what `id()` would return for two variables both assigned the literal integer `100`, and why.

**Hard**

7. Write a function-free script that demonstrates the chained-assignment mutable-object bug from the Common Mistakes section, then fix it.
8. Given a dictionary `config = {"retries": 3}`, create a second name `backup_config` pointing at the same object, modify `backup_config`, and print `config` to show the change is reflected. Then do it again, this time using `dict(config)` to make an actual independent copy, and show that modifying the copy no longer affects the original.

## 19. Stretch challenge

Without running any code, predict the output of the following, then run it to check yourself:

```python
x = 10
y = x
x += 5
print(x, y)

a = [10]
b = a
a += [5]
print(a, b)
```

The two blocks look almost identical, but `+=` on an integer and `+=` on a list behave completely differently under the hood. Figuring out why, before you run it, is the actual point of this exercise.

## 20. Summary

A variable is a name bound to an object, not a container holding a value. That distinction explains almost every "weird" behavior you'll run into with mutable objects like lists and dictionaries later in this module. Get comfortable with `id()` as a debugging tool, follow PEP 8 naming conventions by default, and watch out for chained assignment on anything mutable. Everything from here forward builds on this mental model, so if any part of this still feels shaky, this is the lesson worth rereading before moving on.

## 21. Additional resources

- [PEP 8 — Style Guide for Python Code](https://peps.python.org/pep-0008/)
- [Python official docs: Naming and Binding](https://docs.python.org/3/reference/executionmodel.html#naming-and-binding)
- Python's `id()` and `is` operator docs, for anyone who wants to go deeper on object identity before the Data Types lesson

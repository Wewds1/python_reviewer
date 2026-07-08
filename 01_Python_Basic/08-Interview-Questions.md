# Interview Preparation Guide — Module 1

## How to use this file

This isn't a new set of topics. It's every concept from Lessons 1 through 7, pulled together the way an actual interview would mix them, questions jumping between variables and exceptions and file handling in the same conversation, because that's how technical interviews actually go. Read through it once, then come back and cover the answers with your hand and see how you do out loud. Saying an answer out loud is a genuinely different skill from recognizing it on a page, and it's the one that actually gets tested.

Each question below is tagged by difficulty and topic. Model answers explain not just what to say, but what the interviewer is actually listening for when they ask it.

---

## Conceptual questions

**[Easy | Variables] What's the difference between `=` and `==` in Python?**

`=` assigns a value to a name. `==` compares two values for equality and returns a boolean. Mixing these up (`if x = 5:`) is a syntax error in Python, unlike some languages where it silently compiles and causes bugs, so this specific mistake is at least caught immediately here.

**[Easy | Data Types] Is Python statically or dynamically typed?**

Dynamically typed: a variable's type isn't declared and can change as different objects get assigned to it. Worth adding, if you want to sound like you've thought about it rather than memorized it, that Python is also strongly typed, meaning it won't silently coerce incompatible types for you (`"5" + 5` raises a `TypeError` rather than guessing what you meant). Dynamic and weak typing get conflated constantly, and separating them is a small thing that signals real understanding.

**[Medium | Data Types] Explain mutable versus immutable, and name two of each.**

Mutable objects can be changed in place after creation; immutable ones can't. Lists, dictionaries, and sets are mutable. Tuples, strings, and integers are immutable. The follow-up an interviewer often asks: why does it matter? Mutability affects whether an object can be a dictionary key, whether passing it into a function is safe from unexpected side effects, and whether two variables that reference "the same" object can end up seeing different data if one of them mutates it.

**[Medium | Control Flow] Why does Python use indentation instead of braces?**

It's a deliberate design choice to force readable code; since indentation is significant, badly formatted code simply won't run, rather than compiling and looking messy. The tradeoff is that whitespace bugs (mixing tabs and spaces) can cause confusing errors, which is why editors and linters flag inconsistent indentation.

**[Medium | Functions] What is a pure function, and why does it matter?**

A pure function's output depends only on its inputs, and it has no side effects, it doesn't modify anything outside itself or rely on anything outside itself changing. Pure functions are easier to test (same input always gives the same output) and easier to reason about, since you don't need to track any hidden state. Most real functions aren't purely pure, they log things, they touch a database, but understanding the concept helps you recognize when a function is doing more than its name suggests.

**[Hard | Modules] What's the difference between `import module` and `from module import thing`, in terms of what actually happens?**

Both load and execute the module exactly once and cache it in `sys.modules`. The difference is just what gets bound in your current namespace: `import module` binds the name `module` itself, so you access everything through `module.thing`. `from module import thing` binds `thing` directly, without needing the `module.` prefix. A good answer also mentions that this means `from module import thing` can shadow an existing name in your file if you're not careful, since `thing` now refers to something new.

**[Hard | Exception Handling] Why does Python's exception hierarchy matter when writing an `except` clause?**

Because `except SomeError:` catches `SomeError` and any of its subclasses, not just that exact type. This is why `except Exception:` catches nearly everything (almost every built-in exception inherits from `Exception`), and why writing narrow, specific `except` clauses, and ordering multiple `except` clauses from most specific to least, actually matters: Python checks them top to bottom and uses the first match.

---

## Practical coding questions

**[Easy] Write a function that returns whether a number is even.**

```python
def is_even(n):
    return n % 2 == 0
```

What they're checking: can you use the modulo operator correctly and return a boolean directly instead of writing `if n % 2 == 0: return True else: return False`, which works but signals you haven't quite internalized that comparisons already produce booleans.

**[Easy] Reverse a string without using `[::-1]`.**

```python
def reverse_string(s):
    result = ""
    for char in s:
        result = char + result
    return result
```

They might follow up asking for the time complexity here: building a string this way is O(n²) in the worst case because strings are immutable and each concatenation creates a new string. A better answer for large input uses `"".join(reversed(s))`, which is O(n).

**[Medium] Given a list of numbers, return a new list with duplicates removed, preserving original order.**

```python
def dedupe(numbers):
    seen = set()
    result = []
    for n in numbers:
        if n not in seen:
            seen.add(n)
            result.append(n)
    return result
```

The naive answer, `list(set(numbers))`, removes duplicates but doesn't preserve order, since sets are unordered. Pointing that out unprompted is exactly the kind of detail that separates a good answer from a passable one.

**[Medium] Write a function that counts word frequency in a string.**

```python
def word_frequency(text):
    counts = {}
    for word in text.lower().split():
        counts[word] = counts.get(word, 0) + 1
    return counts
```

A strong follow-up answer mentions `collections.Counter` as the standard-library shortcut for exactly this, while still being able to write it by hand, since interviewers often want to see you can do it without leaning on a library function you might not have memorized the name of under pressure.

**[Hard] Given a list of dictionaries representing transactions (each with `id`, `amount`, `category`), write a function that returns total spending per category.**

```python
def spending_by_category(transactions):
    totals = {}
    for txn in transactions:
        category = txn["category"]
        totals[category] = totals.get(category, 0) + txn["amount"]
    return totals
```

They may ask what happens if a transaction is missing the `category` key. The honest answer is that this raises `KeyError`, and a production version should either validate the input up front or use `txn.get("category", "uncategorized")` depending on whether a missing category is an error condition or an expected edge case.

---

## Debugging questions

**[Easy] What's wrong with this code?**

```python
def greet(name):
    print("Hello, " + name)

greet()
```

Missing required argument, calling `greet()` with no arguments when `name` has no default will raise `TypeError: greet() missing 1 required positional argument: 'name'`. 

**[Medium] What's wrong with this code, and what does it print?**

```python
def add_to_list(item, target=[]):
    target.append(item)
    return target

print(add_to_list(1))
print(add_to_list(2))
```

This is the mutable default argument bug from Lesson 2. It prints `[1]` then `[1, 2]`, not `[1]` then `[2]`, because the default list is created once and shared across every call that doesn't supply its own. The fix: default to `None` and create the list inside the function body.

**[Hard] Why does this raise an error, and how would you fix it?**

```python
total = 0

def add_amount(amount):
    total += amount

add_amount(50)
```

`UnboundLocalError`, because Python sees the assignment `total += amount` inside the function and treats `total` as a local variable for the entire function body, including the read that happens before the assignment. The quick fix is adding `global total` inside the function; the better fix, mentioned as the stronger answer, is avoiding mutable global state entirely by having the function return the new total and reassigning it at the call site.

---

## Scenario-based questions

**[Medium] You're processing a CSV of 50,000 client records, and about 200 of them have malformed data in one column. How do you handle this?**

A strong answer covers reading the file line by line rather than all at once, wrapping the per-row processing in a try/except that catches the specific expected failure (a `ValueError` from a bad numeric conversion, say), logging or collecting the bad rows separately rather than letting one bad row crash the whole batch, and producing a summary at the end: how many rows succeeded, how many failed, and why. The interviewer is checking whether you default to "let it crash" or "handle it gracefully and report clearly," and whether you know the difference between those two being a deliberate choice, not an accident.

**[Medium] A function you wrote returns different results on two different runs with the same input. What would you check first?**

Mutable default arguments are the first suspect if the function takes any collection as a parameter with a default value. After that: any reliance on global state that could have been modified by an earlier call, use of something like `random` or `datetime.now()` inside the function without realizing it, or, if dictionaries are involved, incorrectly assuming a specific iteration order in an older Python version (this is guaranteed as of 3.7, but it's worth knowing why the question used to matter at all).

**[Hard] You need to load a large JSON config file at the start of every script run, and the file occasionally doesn't exist or contains invalid JSON. Walk through how you'd handle that.**

The strong answer separates the two distinct failure modes rather than catching everything with one broad `except`: `FileNotFoundError` for a missing file, and `json.JSONDecodeError` for a file that exists but isn't valid JSON, each handled with a clear, specific message rather than a generic crash. Bonus points for mentioning a sensible fallback, either a hardcoded default config or refusing to start the program with a clear error, rather than continuing to run with a config object that might be silently `None`.

---

## Common mistakes candidates make

Reaching for `except Exception:` or a bare `except:` reflexively, instead of thinking about what can actually go wrong. Forgetting that Python function parameters with mutable defaults are shared across calls. Confusing `is` with `==` (`is` checks identity, whether two names point at the literal same object; `==` checks equality of value) and using them interchangeably without realizing they can give different answers. Writing an answer that's technically correct but never explains the "why," which in a live interview reads as having memorized syntax without understanding it.

## Evaluation criteria interviewers actually use

Correctness matters, but it's rarely the only thing being scored. Interviewers are also weighing whether you can explain your own code out loud without hand-waving, whether you consider edge cases unprompted (empty input, missing keys, wrong types) instead of only after being asked, whether your code reads clearly to someone else, and whether you can take a hint or a follow-up question and actually adjust your approach instead of defending a mistake. A slower, correct, well-explained answer generally beats a fast one you can't account for.

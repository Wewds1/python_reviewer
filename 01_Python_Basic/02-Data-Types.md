# Lesson 2: Data Types

## 1. Learning objectives

By the end of this lesson you should be able to:

- Explain every built-in type covered here well enough to teach it to someone else
- Say, without checking, whether a given type is mutable or immutable, and why that matters
- Pick the right container type for a given problem instead of defaulting to lists for everything
- Reason about the time complexity of common operations on each type
- Spot the type-related bugs that show up constantly in real code, before they ship

## 2. Prerequisites

Lesson 1: Variables. You need the "names point at objects" mental model before any of this will make sense.

## 3. Introduction

This is the longest lesson in the module, and it's long on purpose. Almost every bug I've seen in junior Python code traces back to a misunderstanding about one of these types: mutating something that shouldn't be mutated, using a list where a set would be a hundred times faster, or being surprised that a dictionary lookup doesn't work the way they expected. Get comfortable here and a lot of the rest of the module gets easier.

## 4. Theory

Python has a small set of built-in types, and everything else in the language is built out of them. They split cleanly into two groups:

**Immutable** (can't be changed after creation): `int`, `float`, `bool`, `complex`, `str`, `tuple`

**Mutable** (can be changed in place): `list`, `dict`, `set`

`None` is its own thing, a singleton representing the absence of a value.

That mutable/immutable split isn't a minor technical footnote. It decides whether you can use something as a dictionary key, whether passing it into a function is safe, and whether two variables pointing at "the same" value can drift apart unexpectedly.

### int

Whole numbers, arbitrary precision. Python doesn't have the 32-bit or 64-bit overflow problems that trip people up in C; `2 ** 1000` just works and gives you the exact answer, no wraparound.

```python
population = 8_000_000_000  # underscores as visual separators, ignored by Python
```

Common operations and their cost: addition, subtraction, and comparison are effectively O(1) for numbers of a reasonable size. Once you're dealing with genuinely huge numbers (thousands of digits), the cost grows, but that's not a concern for anything you'll write in this module.

### float

Floating-point numbers, following the IEEE 754 double-precision standard. The thing that catches everyone off guard:

```python
print(0.1 + 0.2)  # 0.30000000000000004
```

This isn't a Python bug. It's how binary floating-point representation works in every mainstream language. 0.1 can't be represented exactly in binary, the same way 1/3 can't be written exactly in decimal. If you need exact decimal arithmetic (money, for instance), use the `decimal` module instead of raw floats.

### bool

`True` and `False`. Worth knowing: `bool` is technically a subclass of `int` in Python. `True == 1` and `False == 0` both evaluate to `True`. This is occasionally useful (`sum([True, True, False])` gives you `2`) and occasionally a source of subtle bugs when someone doesn't realize a boolean got used in arithmetic by accident.

### complex

Numbers with a real and imaginary part: `3 + 4j`. Honestly, you will rarely touch this outside of scientific or signal-processing code. It's included here because it's a built-in type, not because you'll use it in a typical backend job.

### str

Text, and immutable. Every "modification" of a string actually builds a new one:

```python
name = "alex"
name = name.upper()  # this creates a new string, "ALEX"
```

Strings get a full lesson's worth of methods (`.split()`, `.join()`, `.strip()`, `.replace()`, slicing) which are covered in depth in the string-heavy exercises at the end of this lesson.

### list

An ordered, mutable sequence. The default "just put stuff in here" container in Python.

```python
tasks = ["review PR", "deploy", "write tests"]
tasks.append("update docs")
```

Appending to the end is O(1) on average. Inserting or deleting from the front or middle is O(n), because everything after that position has to shift. If you're constantly inserting at the front of a list, you probably want a `collections.deque` instead, though that's a stretch topic beyond this lesson.

### tuple

Ordered and immutable. People often describe it as "a list that can't change," which is true but undersells why it exists. Tuples signal intent: this is a fixed collection of things, not a growing sequence. Function return values that bundle multiple pieces of related data (`return name, age` returns a tuple) are the classic use case.

```python
point = (3, 7)
x, y = point  # unpacking
```

Because they're immutable, tuples can be used as dictionary keys. Lists can't.

### set

An unordered collection of unique items, built on a hash table internally, the same structure that powers dictionaries.

```python
seen_ids = {101, 102, 103}
print(104 in seen_ids)  # False, and this check is O(1) on average
```

That last line is the entire reason sets exist. Checking membership in a list is O(n): Python has to walk through every element. Checking membership in a set is O(1) on average, because it hashes the value and jumps straight to where it should be. If you find yourself writing `if x in my_list:` inside a loop, and `my_list` has more than a handful of items, that's usually a sign you want a set instead.

### dict

Key-value pairs, also backed by a hash table. As of Python 3.7, insertion order is preserved as a language guarantee, not just a CPython implementation detail.

```python
user = {"name": "Priya", "role": "backend engineer"}
print(user["role"])  # O(1) average lookup
```

Keys must be hashable, which is why they're almost always strings, numbers, or tuples, and never lists or dictionaries.

### None

Represents "no value here." It is a singleton: there is exactly one `None` object in the entire running program, which is why you check for it with `is None` rather than `== None`.

```python
result = find_user(user_id=999)
if result is None:
    print("user not found")
```

## 5. Why this concept exists

Different problems need different tradeoffs between order, uniqueness, mutability, and lookup speed. A language with only one container type would force you to build the others yourself out of that one, badly and slowly. Python gives you the common ones as built-ins, implemented in optimized C, so you get correctness and speed for free instead of having to hand-roll a hash table every time you need a fast lookup.

## 6. How Python implements it internally

`list` is implemented as a dynamic array, a contiguous block of memory that occasionally over-allocates and resizes when it runs out of room, which is why appending is usually O(1) but occasionally triggers a more expensive resize.

`dict` and `set` are both implemented as hash tables. When you look up a key, CPython computes a hash of it, uses that hash to jump almost directly to the right memory slot, and only then checks that the key actually matches (to handle rare hash collisions). That's the entire reason lookups are so fast, and also why only hashable (effectively, immutable) objects can be keys: if the key could change after being inserted, its hash would change too, and the table would have no way to find it again.

## 7. Real-world analogy

A list is a numbered coat check: item one, item two, item three, in order, and you can have five identical grey coats hanging there if you want. A set is a guest list at the door: nobody's name appears twice, and the bouncer checking "are you on the list" doesn't walk the whole line, they jump straight to where your name would be. A dictionary is that same guest list, except each name comes with a room assignment attached. A tuple is a printed and laminated itinerary: you can read it, but nobody's stapling extra pages onto it after the fact.

## 8. Enterprise use cases

Sets show up constantly in data reconciliation work: given two lists of client account IDs from two different systems, finding which ones are in one but not the other is a one-line set difference, and it's fast even at scale. Dictionaries are the natural shape for anything that came out of JSON, which is most API responses and configuration files you'll touch in a consulting job. Tuples get used for fixed-shape records, database rows returned from a query, coordinates, RGB values, where the position of each element has fixed meaning and nothing should be appended to it later.

## 9. Syntax

```python
# Numeric types
whole = 42
decimal = 3.14
complex_num = 2 + 3j
flag = True

# Sequences
text = "hello"
items = [1, 2, 3]
coords = (10, 20)

# Hashed collections
unique_ids = {1, 2, 3}
person = {"name": "Sam", "age": 30}

# Absence of value
missing = None
```

## 10. Step-by-step examples

**Easy — checking types and mutability:**

```python
x = [1, 2, 3]
y = (1, 2, 3)
print(type(x), type(y))
x.append(4)   # works, lists are mutable
# y.append(4) # would raise AttributeError, tuples have no .append
```

**Medium — using a set to find duplicates:**

```python
emails = ["a@x.com", "b@x.com", "a@x.com", "c@x.com"]
unique = set(emails)
print(len(emails) - len(unique))  # 1 duplicate found
```

**Hard — combining a dict and a set to deduplicate structured data by one field:**

```python
records = [
    {"id": 1, "name": "Alex"},
    {"id": 2, "name": "Jordan"},
    {"id": 1, "name": "Alex"},  # duplicate id
]

seen_ids = set()
deduped = []

for record in records:
    if record["id"] not in seen_ids:
        deduped.append(record)
        seen_ids.add(record["id"])

print(deduped)  # only the two unique records survive
```

This pattern, a set tracking what you've already processed, is one of the most useful small tools in everyday Python. It comes up in data cleaning constantly.

## 11. Common mistakes

**Mutable default arguments.** This is the single most infamous gotcha in the language:

```python
def add_item(item, basket=[]):  # DANGER
    basket.append(item)
    return basket

print(add_item("apple"))   # ['apple']
print(add_item("banana"))  # ['apple', 'banana'] — not what most people expect
```

The default list is created once, when the function is defined, not fresh on every call. The fix is to default to `None` and create the list inside the function:

```python
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket
```

**Comparing floats with `==`.** Because of the precision issue mentioned earlier, `0.1 + 0.2 == 0.3` is `False`. Use `math.isclose()` for float comparisons instead.

**Using a list when you meant a set.** Repeatedly checking `if x in my_list` in a loop over a large list is a performance mistake that's invisible until the data grows.

## 12. Debugging tips

If a function is silently returning stale or accumulating data across calls, check for a mutable default argument first. If a dictionary lookup is throwing `KeyError`, use `.get(key, default)` instead of `dict[key]` while you're debugging, so you can see the actual shape of the data without the program crashing mid-investigation.

## 13. Best practices

Default to a list unless you specifically need uniqueness (set), fixed structure (tuple), or key-based lookup (dict). Never use a mutable object as a default argument. Use `is None` / `is not None` for None checks, never `== None`. When a function returns multiple related values, prefer a tuple, or better, a `NamedTuple` or dataclass once you're past this module, over a plain list.

## 14. Performance considerations

| Operation | list | set | dict |
|---|---|---|---|
| Membership check (`in`) | O(n) | O(1) average | O(1) average (checks keys) |
| Insert at end | O(1) average | O(1) average | O(1) average |
| Insert at front | O(n) | n/a (unordered) | n/a |
| Lookup by index/key | O(1) for index | n/a | O(1) average for key |

That "average" caveat matters: worst-case dict and set operations can degrade to O(n) under pathological hash collisions, but in practice, with Python's built-in hashing, you won't hit that in normal use.

## 15. Code style (PEP 8)

Use the literal syntax (`[]`, `{}`, `()`) over the constructor calls (`list()`, `dict()`, `tuple()`) when creating empty or simple collections, since it's faster and more idiomatic. Use `{"key": "value"}` rather than `dict(key="value")` for dictionaries with more than one or two entries. Keep dictionary and list literals with many entries spread across multiple lines, one entry per line, when they get long enough to hurt readability on one line.

## 16. Interview questions with model answers

**Q: Why can't you use a list as a dictionary key?**

Dictionary keys must be hashable, and hashability generally requires immutability. If a list could be a key and then got mutated after insertion, its hash would change, and the dictionary would no longer be able to find it in the table, breaking the whole structure. Tuples work as keys precisely because they're immutable.

**Q: When would you choose a set over a list?**

Whenever you need to check membership repeatedly and don't care about order or duplicates. The interviewer wants to hear "O(1) average lookup versus O(n)" specifically, not just "sets are faster," because that shows you understand why, not just that it's true.

**Q: What's wrong with this function?**

```python
def append_to(element, target=[]):
    target.append(element)
    return target
```

The ideal answer names the mutable default argument bug specifically, explains that the default list is shared across every call that doesn't pass its own list, and gives the `None`-default fix.

## 17. Knowledge check

1. Which of these types are mutable: `str`, `list`, `tuple`, `dict`, `set`?
2. Why does `0.1 + 0.2 == 0.3` return `False`?
3. What's the time complexity of checking `x in my_set` versus `x in my_list`?
4. Why does `True + True` evaluate to `2`?

## 18. Hands-on exercises

**Easy**

1. Create a list of five numbers and a tuple of the same five numbers. Try to append to both and observe what happens.
2. Write a one-liner that returns `True` if a given value is `None`.
3. Create a dictionary representing a person (name, age, city) and print each value.

**Medium**

4. Given two lists of usernames, use sets to find which usernames appear in the first list but not the second.
5. Write a function with a mutable default argument bug, demonstrate the bug with two calls, then fix it.
6. Given a list of words, build a dictionary counting how many times each word appears, without using `collections.Counter`.

**Hard**

7. Given a list of dictionaries representing orders (each with an `order_id` and `amount`), write code that removes duplicate orders by `order_id`, keeping the first occurrence, using a set to track what's already been seen.
8. Explain, in comments, why `{[1, 2]: "a"}` raises a `TypeError`, and rewrite it using a tuple instead so it works.

## 19. Stretch challenge

Without running it, work out what this prints, then verify:

```python
a = (1, [2, 3])
a[1].append(4)
print(a)
```

A tuple is immutable, and yet this code runs without error and the tuple's contents visibly change. Explain, in your own words, why both of those things are true at once. This one trips up a lot of people who think "immutable" means "nothing inside it can ever change."

## 20. Summary

Every built-in type here is a different answer to the same question: what's the fastest, clearest way to store this particular shape of data? Immutability determines whether something can be a dictionary key and whether you need to worry about shared references. Hash-based structures (sets and dicts) trade a small amount of memory overhead for dramatically faster lookups than lists. The mutable default argument bug is the one mistake from this lesson that will follow you into every future lesson if you don't internalize the fix now.

## 21. Additional resources

- [Python official docs: Built-in Types](https://docs.python.org/3/library/stdtypes.html)
- [TimeComplexity — Python wiki](https://wiki.python.org/moin/TimeComplexity)
- [PEP 3141 — A Type Hierarchy for Numbers](https://peps.python.org/pep-3141/), for anyone curious how `bool`, `int`, `float`, and `complex` relate to each other

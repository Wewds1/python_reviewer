# Lesson 4: Tuples

## 1. Learning objectives

By the end of this lesson you should be able to:

- Explain what immutability means for a tuple and what it actually protects versus what it doesn't
- Use tuple packing and unpacking fluently, including extended unpacking with `*`
- Know when to choose a tuple over a list, and articulate the reason precisely
- Use `collections.namedtuple` for structured, self-documenting fixed records
- Explain why tuples can be dictionary keys and list elements cannot

## 2. Prerequisites

Lesson 3 (Lists). Tuples are best understood as the immutable counterpart to lists, so the list mental model needs to be solid first.

## 3. Introduction

Tuples are often taught as "like lists but immutable" and left at that, which undersells them significantly. Immutability isn't just a restriction; it's a communication: a tuple says "the number of elements and their positions have fixed meaning, and this collection should never change." That intent matters for code clarity, for performance (tuples are faster and lighter than lists), and for correctness (tuples can be used as dictionary keys, which makes them essential in a range of data structures that lists can't participate in at all).

## 4. Theory

A tuple is an ordered, immutable sequence of elements. Once created, neither the elements nor the length can change.

```python
point = (3, 7)
# point[0] = 99  # TypeError: 'tuple' object does not support item assignment
```

"Immutable" means the tuple's own references cannot change. The objects those references point to can still be mutable:

```python
t = ([1, 2], [3, 4])
t[0].append(99)      # This works — the list itself is mutable
print(t)              # ([1, 2, 99], [3, 4])
# But t[0] = [9, 9]  # This fails — you can't change which list t[0] points to
```

This distinction is important: tuple immutability means "these slots cannot be reassigned," not "nothing inside can ever change." The list inside `t[0]` can grow; what can't change is that `t[0]` points at that specific list.

## 5. Why this concept exists

Immutable data has two major advantages: it can be hashed (enabling dictionary keys and set elements), and it communicates intent clearly to anyone reading the code. A list signals "this collection may grow or change." A tuple signals "this is a fixed group of related values." The classic examples: coordinates `(x, y)`, database rows `(id, name, email)`, function return values bundling multiple results, RGB color values `(255, 128, 0)`. In all these cases, the fixed structure is part of the meaning.

## 6. Internal implementation

Internally, CPython represents a tuple as a simple C struct with a fixed-size array of `PyObject*` pointers. Because the length is fixed at creation and never changes, Python doesn't need to track an allocated capacity separate from the length, unlike lists. This makes tuples slightly smaller than equivalent lists:

```python
import sys

lst = [1, 2, 3, 4, 5]
tup = (1, 2, 3, 4, 5)

print(sys.getsizeof(lst))  # typically 120 bytes
print(sys.getsizeof(tup))  # typically 80 bytes
```

CPython also caches small tuples (length 0 to approximately 20) for reuse, making their creation faster than equivalent list creation. This is the "tuple is faster to create" optimization you'll hear mentioned.

## 7. Real-world analogy

A list is a whiteboard — you can write, erase, add, remove, and rearrange freely. A tuple is a printed certificate: the content is fixed at the moment of printing. You can read it, frame it, file it, and pass it around, but you can't change what it says. The permanence is a feature: anyone who receives a printed certificate knows exactly what it says and can trust it hasn't been modified in transit. That's precisely the property that makes tuples hashable and safe to use as dictionary keys.

## 8. Enterprise use cases

**Multi-value function returns:** Returning `(success, error_message)` or `(status_code, response_body)` as a tuple signals fixed structure at the call site and allows clean unpacking.

**Dictionary keys with compound structure:** A cache keyed by `(user_id, report_date)` or a lookup table keyed by `(region, product_category)` requires hashable keys, which tuples provide and lists don't.

**Database rows:** Results from database queries are typically returned as tuples (or namedtuples) in Python database libraries, because each column's position has fixed meaning and shouldn't change.

**Configuration records:** A tuple of `(host, port, timeout)` for a connection config communicates that these values are fixed and belong together.

## 9. Complexity analysis

| Operation | Complexity | Notes |
|---|---|---|
| `t[i]` (index access) | O(1) | Same as list |
| `x in t` | O(n) | Linear scan, same as list |
| `len(t)` | O(1) | Stored directly |
| `t + t2` | O(n + m) | Creates a new tuple |
| `t * k` | O(nk) | Creates a new tuple |
| `t[a:b]` (slicing) | O(b - a) | Creates a new tuple |
| Iteration | O(n) | Same as list |
| Creation | Faster than list | Fixed-size, no capacity management |

Tuples do not have `.append()`, `.insert()`, `.remove()`, or `.sort()` because they're immutable. If you need those operations, you need a list.

## 10. Step-by-step visual walkthrough

**Tuple packing and unpacking:**

```python
# Packing — multiple values assigned to a single tuple
coordinates = 3, 7, 0   # parentheses are optional for packing
print(type(coordinates)) # <class 'tuple'>
print(coordinates)        # (3, 7, 0)

# Unpacking — tuple's values distributed to individual names
x, y, z = coordinates
print(x, y, z)            # 3 7 0

# Extended unpacking with *
first, *rest = (1, 2, 3, 4, 5)
print(first)  # 1
print(rest)   # [2, 3, 4, 5]  — note: rest is a list, not a tuple

*head, last = (1, 2, 3, 4, 5)
print(head)   # [1, 2, 3, 4]
print(last)   # 5

# Swap using tuple packing/unpacking — no temp variable needed
a, b = 10, 20
a, b = b, a
print(a, b)   # 20 10
```

**Why swapping works without a temporary variable:**

```
Step 1: Python evaluates the right side: (b, a) → (20, 10) — creates a temporary tuple
Step 2: Python unpacks that tuple: a gets 20, b gets 10
Step 3: The temporary tuple is discarded
```

This is tuple packing and unpacking in action, happening in a single line transparently.

## 11. Syntax

**Creation:**
```python
empty = ()
single = (42,)        # comma required for single-element tuple
coords = (3, 7)
without_parens = 3, 7  # parentheses optional
nested = ((1, 2), (3, 4))
from_iter = tuple([1, 2, 3])
```

**Common operations:**
```python
t = (10, 20, 30, 40, 50)

print(t[0])        # 10
print(t[-1])       # 50
print(t[1:3])      # (20, 30)
print(len(t))      # 5
print(10 in t)     # True
print(t.count(20)) # 1
print(t.index(30)) # 2

# Tuples as dictionary keys
cache = {}
cache[(1, "report")] = {"data": [1, 2, 3]}
print(cache[(1, "report")])
```

**Named tuples:**
```python
from collections import namedtuple

# Define once, use like a class with attribute access
Point = namedtuple("Point", ["x", "y"])
Employee = namedtuple("Employee", ["name", "department", "salary"])

p = Point(3, 7)
print(p.x, p.y)      # 3 7 — attribute access, clearer than p[0], p[1]
print(p[0])           # 3 — still works as a tuple
print(p._asdict())    # OrderedDict([('x', 3), ('y', 7)])

emp = Employee("Alex", "Engineering", 75000)
print(emp.name)       # Alex
print(emp._replace(salary=80000))  # creates a new Employee with updated salary
```

Named tuples are still tuples (hashable, immutable, efficient), but fields are accessible by name rather than by position, making code self-documenting without the overhead of a full class.

## 12. Common mistakes

**Forgetting the trailing comma for a single-element tuple:**

```python
not_a_tuple = (42)    # this is just 42, an integer in parentheses
actual_tuple = (42,)  # the comma makes it a tuple
print(type(not_a_tuple))   # <class 'int'>
print(type(actual_tuple))  # <class 'tuple'>
```

This is one of the most common Python beginner mistakes and produces a `TypeError` when code assumes it has a tuple.

**Assuming tuple immutability protects nested mutable objects.** As shown in the theory section, `t = ([1, 2], [3, 4])` is a tuple whose inner lists are still fully mutable. The tuple's slots can't be reassigned; the objects in those slots can still change.

**Using a plain tuple when a namedtuple would be clearer.** `record[0]`, `record[1]`, `record[2]` is opaque; `record.name`, `record.department`, `record.salary` communicates intent to every future reader.

**Converting a list to a tuple "for performance" on every operation.** Tuple creation has overhead too. If you're repeatedly creating tuples from lists just to get a speed boost, profile first; the conversion cost may outweigh the savings.

## 13. Debugging tips

`TypeError: 'tuple' object does not support item assignment` means you tried to modify a tuple in place. If you need a mutable version, convert with `list(t)`, modify, then convert back with `tuple(lst)` if immutability matters. If a tuple has only one element and it's not behaving as a tuple (no length, wrong type), check whether the trailing comma is present.

## 14. Best practices

Use tuples for fixed-structure data where position has inherent meaning: coordinates, records, multi-value returns. Use namedtuples when you have three or more fields and tuple[0], tuple[1] would obscure what each field means. Use lists when the collection needs to grow, shrink, or change. Don't use a list "just to be safe" when a tuple is the honest representation of fixed data — the immutability is part of the contract you're communicating to the next reader.

## 15. Performance considerations

Tuple creation is faster than list creation (CPython caches empty tuples and some small ones). Iteration over a tuple is slightly faster than over a list due to simpler internal structure. Memory usage is lower. For large volumes of short-lived fixed-structure records (database result rows, geometry coordinates), tuples are meaningfully more efficient than equivalent lists. For anything where you need modification, the immutability makes tuples the wrong choice entirely regardless of their performance advantages.

## 16. Code style

Use parentheses consistently for tuples except in the most obvious cases like function return values and swap idioms where readability is clear without them. Always include the trailing comma for single-element tuples to make intent unambiguous. Prefer namedtuples over plain tuples for any structure with more than two or three elements where names would add clarity.

## 17. Interview questions with model answers

**Q: What's the difference between a list and a tuple?**

A list is mutable and ordered; a tuple is immutable and ordered. Lists are used for collections that may change; tuples are used for fixed-structure records where position has meaning. The practical consequence: tuples can be dictionary keys and set members (they're hashable), lists cannot. Tuples are also slightly smaller and faster to create.

**Q: If a tuple is immutable, why can I modify a list that's inside a tuple?**

Tuple immutability means the tuple's own references (its slots) cannot be reassigned. The object a slot points to is unaffected by this restriction. A tuple containing a list still points to that same list, and that list remains a fully mutable object. You can append to the list; you just can't replace the tuple's slot with a different list.

**Q: When would you use a namedtuple instead of a regular tuple or a class?**

A namedtuple is appropriate when you have a fixed, record-like structure with three or more fields, where field names would significantly clarify the code versus positional index access, but you don't need methods beyond basic attribute access and a few built-in helpers (`_asdict`, `_replace`). It's more self-documenting than a plain tuple, lighter than a full class, and still hashable and immutable.

## 18. Knowledge check

1. Why does `(42)` not create a tuple, but `(42,)` does?
2. Can a tuple containing a list be used as a dictionary key? Why or why not?
3. What does `first, *rest = (1, 2, 3, 4)` assign to `rest`?
4. Name two situations where a tuple is the better choice over a list.

## 19. Hands-on exercises

**Easy**

1. Create a single-element tuple containing the string `"hello"` and confirm its type.
2. Unpack the tuple `(10, 20, 30)` into three variables and print each.
3. Create a `namedtuple` called `Color` with fields `red`, `green`, `blue`, and instantiate it with the values for pure red.

**Medium**

4. Write a function that returns two values (a result and a status message) as a tuple, and demonstrate unpacking the result at the call site.
5. Use a tuple as a dictionary key to build a lookup table mapping `(country, city)` pairs to population values, and retrieve London's population.
6. Use extended unpacking to separate the first element, the last element, and all middle elements of `(1, 2, 3, 4, 5, 6, 7)` into three variables.

**Hard**

7. Build a `namedtuple` called `Transaction` with fields `id`, `amount`, `currency`, `timestamp`, then write a function that takes a list of `Transaction` namedtuples and returns the total amount in a given currency.
8. Demonstrate that a tuple containing a mutable list behaves correctly as a dictionary key (hashable) as long as you don't modify the inner list, but that modifying the inner list does NOT affect the dictionary lookup after the key is already inserted (explain why in a comment).

## 20. Stretch challenge

Implement a simple 2D point class using a namedtuple as the underlying storage, with additional methods for distance calculation and addition, by subclassing the namedtuple. This exercise demonstrates that namedtuples can be subclassed and extended with methods while keeping their tuple properties intact. Add `__add__` (returning a new Point), `distance_to(other)`, and `__str__`. Confirm that two points with the same coordinates compare as equal via `==` (since tuples implement `__eq__` by value) and that a point can be used as a dictionary key.

## 21. Summary

A tuple is an immutable, ordered sequence optimized for fixed-structure data. Its immutability makes it hashable, enabling use as dictionary keys and set members, which lists cannot be. Tuple immutability protects the slots themselves, not the mutable objects those slots might reference. Namedtuples extend the base tuple with named field access and self-documenting structure, making them ideal for record-like data. The choice between list and tuple is a design signal: list means "this may change," tuple means "this is fixed."

## 22. Additional resources

- [Python official docs: Tuples and Sequences](https://docs.python.org/3/tutorial/datastructures.html#tuples-and-sequences)
- [Python official docs: collections.namedtuple](https://docs.python.org/3/library/collections.html#collections.namedtuple)
- [PEP 3132 — Extended Iterable Unpacking](https://peps.python.org/pep-3132/)

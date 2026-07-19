# Lesson 8: Sets

## 1. Learning objectives

By the end of this lesson you should be able to:

- Explain how a set uses hashing internally and why that makes membership testing O(1)
- Use all set operations (union, intersection, difference, symmetric difference) both as methods and operators
- Recognize the specific problem patterns where a set is dramatically more efficient than a list
- Distinguish between `set` and `frozenset` and know when each is appropriate
- Apply sets to real data deduplication and comparison problems in backend systems

## 2. Prerequisites

Lesson 7 (Dictionaries and Hash Tables). A set is essentially a hash table that stores only keys, no values, so the internal model from Lesson 7 applies directly here.

## 3. Introduction

The set is Python's most underused built-in data structure. Most developers reach for a list by default, even in situations where they only care about membership testing or uniqueness. That habit carries a real cost: `if x in my_list` is O(n); `if x in my_set` is O(1) average. For a single check on a small collection, the difference is invisible. For 100,000 checks on a 50,000-element collection, the difference is the distinction between a feature that runs in a second and one that runs in an hour. This lesson makes set-shaped problems easy to recognize on sight.

## 4. Theory

A set is an unordered collection of unique, hashable elements. "Unordered" means there's no guaranteed sequence to iteration. "Unique" means duplicates are silently discarded. "Hashable" means only immutable objects can be set members — no lists, no dicts, no other sets.

```python
s = {1, 2, 3, 2, 1}
print(s)       # {1, 2, 3} — duplicates removed
print(type(s)) # <class 'set'>
```

Internally, a set is a hash table that stores only keys, with no associated values. Every operation that makes dictionaries fast for lookup applies equally to sets: adding an element, removing an element, and testing membership are all O(1) average, regardless of how many elements the set contains.

## 5. Why this concept exists

Two fundamental problems appear constantly in real data work:

**Uniqueness:** given a collection that may contain duplicates, produce a collection that doesn't. Converting to a set is a one-operation O(n) solution.

**Membership testing:** given a large collection, repeatedly check whether specific items belong to it. A list requires O(n) per check; a set requires O(1) per check after an O(n) build.

The mathematical set operations (union, intersection, difference) also appear naturally in data comparison problems: which customers exist in system A but not system B, which products appear in both the catalog and the inventory, which IDs were processed in both runs.

## 6. Internal implementation

A set in CPython is implemented as a hash table where each slot stores either:
- Empty (nothing here)
- A hash and a reference to the element
- A tombstone (element was deleted)

When you call `element in my_set`, Python:
1. Calls `hash(element)` → integer
2. Computes `hash % capacity` → bucket index
3. Checks that bucket: if the stored hash and element match, returns `True`
4. If there's a collision (different element in that slot), probes forward
5. If an empty slot is found before a match, returns `False`

This is identical to the dictionary lookup process, minus the value retrieval step. The same load factor management applies: Python resizes the internal array when it gets about 2/3 full, keeping collision rates low and operations fast.

## 7. Real-world analogy

A set is a bouncer with a guest list and a stamp. When you arrive, the bouncer checks the list (O(1) — it's indexed), stamps your hand if you're on it, and turns you away if you're not. Adding yourself to the list twice doesn't get you in twice — you're either on it or you're not. The bouncer doesn't care what order people arrived (unordered), and each person appears at most once (unique). The entire conversation — are you on the list? — takes the same amount of time whether the party has 10 guests or 10,000.

## 8. Enterprise use cases

**Data deduplication:** ETL pipelines processing client data extracts often receive records with duplicate IDs across multiple files. Converting ID lists to a set deduplicates in O(n) rather than the O(n²) of nested loop comparison.

**Reconciliation:** Comparing two lists of account IDs — one from System A, one from System B — to find accounts in one but not the other is a set difference operation. This is a real, daily operation in financial reconciliation systems.

**Permission checking:** Whether a user has a specific permission, when permissions are stored as a set of strings, is an O(1) membership check.

**Visited tracking in traversal:** Graph and web crawler algorithms track visited nodes in a set to avoid processing the same node twice.

**Tag systems:** Checking whether a document has any of a given list of tags is a set intersection check, O(min(len(doc_tags), len(query_tags))) rather than O(n*m) with nested loops.

## 9. Complexity analysis

| Operation | Average | Worst Case | Notes |
|---|---|---|---|
| `x in s` | O(1) | O(n) | Hash-based membership test |
| `s.add(x)` | O(1) | O(n) | Amortized, includes rare resizes |
| `s.remove(x)` | O(1) | O(n) | Raises KeyError if not present |
| `s.discard(x)` | O(1) | O(n) | Silent if not present |
| `s.pop()` | O(1) | O(n) | Removes arbitrary element |
| `len(s)` | O(1) | O(1) | Stored on object |
| `s \| t` (union) | O(len(s) + len(t)) | — | Creates new set |
| `s & t` (intersection) | O(min(len(s), len(t))) | — | Creates new set |
| `s - t` (difference) | O(len(s)) | — | Creates new set |
| `s ^ t` (symmetric diff) | O(len(s) + len(t)) | — | Creates new set |
| `s <= t` (subset) | O(len(s)) | — | |
| `s >= t` (superset) | O(len(t)) | — | |

The critical entry: `x in s` is O(1) average, versus O(n) for a list. For repeated membership tests, this is the most impactful single performance difference in the module.

## 10. Step-by-step visual walkthrough

**Data reconciliation using set operations:**

Scenario: two systems export lists of customer IDs. Find customers in one system but not the other.

```
System A IDs: [101, 102, 103, 104, 105]
System B IDs: [102, 103, 104, 106, 107]

Convert to sets:
set_a = {101, 102, 103, 104, 105}
set_b = {102, 103, 104, 106, 107}

In A but not B (difference: set_a - set_b):
  Check each element of A: is it in B?
  101 → not in B → include
  102 → in B → exclude
  103 → in B → exclude
  104 → in B → exclude
  105 → not in B → include
  Result: {101, 105}  ← customers only in System A

In B but not A (difference: set_b - set_a):
  Result: {106, 107}  ← customers only in System B

In both (intersection: set_a & set_b):
  Result: {102, 103, 104}

In either (union: set_a | set_b):
  Result: {101, 102, 103, 104, 105, 106, 107}

In one but not both (symmetric difference: set_a ^ set_b):
  Result: {101, 105, 106, 107}
```

**Deduplication walkthrough:**

```
Input: [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

Add 3 → hash(3) → bucket X → {3}
Add 1 → hash(1) → bucket Y → {3, 1}
Add 4 → {3, 1, 4}
Add 1 → hash(1) → bucket Y → already occupied by 1 → skip
Add 5 → {3, 1, 4, 5}
Add 9 → {3, 1, 4, 5, 9}
Add 2 → {3, 1, 4, 5, 9, 2}
Add 6 → {3, 1, 4, 5, 9, 2, 6}
Add 5 → already in set → skip
Add 3 → already in set → skip
Add 5 → already in set → skip

Result: {1, 2, 3, 4, 5, 6, 9}  (order not guaranteed)
```

## 11. Syntax

**Creation:**
```python
empty = set()        # NOT {} — that creates an empty dict
numbers = {1, 2, 3}
from_list = set([1, 2, 2, 3, 3])  # {1, 2, 3}
from_string = set("hello")          # {'h', 'e', 'l', 'o'}
```

**Membership and modification:**
```python
s = {1, 2, 3}

print(1 in s)     # True — O(1)
print(4 in s)     # False — O(1)

s.add(4)          # {1, 2, 3, 4}
s.add(2)          # {1, 2, 3, 4} — no duplicate added, no error
s.remove(3)       # {1, 2, 4} — KeyError if 3 not present
s.discard(99)     # no error if 99 not present
popped = s.pop()  # removes and returns an arbitrary element
s.clear()         # empties the set
```

**Set operations — methods and operators:**
```python
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

# Union — all elements from either set
print(a | b)             # {1, 2, 3, 4, 5, 6}
print(a.union(b))        # same

# Intersection — only elements in both sets
print(a & b)             # {3, 4}
print(a.intersection(b)) # same

# Difference — elements in a but not b
print(a - b)             # {1, 2}
print(a.difference(b))   # same

# Symmetric difference — elements in exactly one set
print(a ^ b)                        # {1, 2, 5, 6}
print(a.symmetric_difference(b))    # same

# In-place operations (modify the set instead of creating a new one)
a |= b   # a becomes {1, 2, 3, 4, 5, 6}
a &= b   # a becomes intersection
a -= b   # a becomes difference
a ^= b   # a becomes symmetric difference
```

**Subset and superset:**
```python
a = {1, 2, 3}
b = {1, 2, 3, 4, 5}

print(a <= b)         # True — a is a subset of b
print(a.issubset(b))  # same

print(b >= a)           # True — b is a superset of a
print(b.issuperset(a))  # same

print(a < b)   # True — a is a proper subset (a ≠ b)
print(a <= a)  # True — every set is a subset of itself
print(a < a)   # False — not a proper subset of itself

print(a.isdisjoint({4, 5}))  # True — no elements in common
```

**Frozenset:**
```python
# frozenset is an immutable set — hashable, usable as dict key or set element
fs = frozenset([1, 2, 3])
# fs.add(4)  # AttributeError — frozenset is immutable

# Useful as a dictionary key when the key is a collection of items
permissions = {
    frozenset(["read", "write"]): "editor",
    frozenset(["read"]): "viewer",
}
user_perms = frozenset(["read", "write"])
print(permissions[user_perms])  # "editor"
```

**Set comprehensions:**
```python
squares = {x**2 for x in range(10)}
# {0, 1, 4, 9, 16, 25, 36, 49, 64, 81}

unique_lengths = {len(word) for word in ["hello", "world", "hi", "bye"]}
# {2, 3, 5}
```

## 12. Common mistakes

**Using `{}` to create an empty set.** This creates an empty dictionary, not an empty set. Always use `set()` for an empty set.

```python
wrong = {}        # dict — type(wrong) is dict
correct = set()   # set — type(correct) is set
```

**Using `remove()` when the element might not be present.** `remove()` raises `KeyError` for missing elements. Use `discard()` when the element's presence isn't guaranteed.

**Forgetting that sets are unordered.** You cannot rely on any particular iteration order. If order matters, a set is the wrong structure.

**Trying to put mutable objects into a set.**

```python
s = set()
s.add([1, 2, 3])   # TypeError: unhashable type: 'list'
s.add((1, 2, 3))   # Works — tuple is hashable
```

**Converting a list to a set when order must be preserved.** `list(set(lst))` deduplicates but destroys order. Use the "seen set + loop" pattern from Lesson 3 instead.

## 13. Debugging tips

If `x in my_collection` inside a loop is making your code noticeably slow, convert `my_collection` to a set before the loop. If you're getting `TypeError: unhashable type` when adding to a set, the element is a mutable type — convert it to an immutable equivalent (e.g., list → tuple) first. If a set operation returns unexpected results, print both sets first and trace through the operation manually against the step-by-step walkthrough model above.

## 14. Best practices

Use a set instead of a list any time you only care about membership (not position or duplicates). Use `discard()` over `remove()` unless you specifically want an error when an element is absent. Prefer set operators (`|`, `&`, `-`, `^`) over method equivalents for conciseness in expressions, and method equivalents when clarity matters or when operating on iterables rather than sets. Use `frozenset` when you need to use a set as a dictionary key or as an element of another set.

## 15. Performance considerations

The O(1) average membership test is the primary performance argument for sets. The main cost is memory: a set uses more memory than a list of equivalent elements, due to hash table overhead, similar to dictionaries. For very small collections (under ~20 elements), the overhead of a set may not be worth the lookup speed gain. For any collection you'll be searching repeatedly, the set pays for itself immediately.

## 16. Code style

Use set literals (`{1, 2, 3}`) over `set([1, 2, 3])` when the elements are known at write time. Name sets for what they contain: `visited_ids`, `active_users`, `processed_emails`. When using set operations for data comparison, prefer the operator syntax (`a - b`, `a & b`) in simple expressions and the method syntax (`.difference()`, `.intersection()`) when working in chains or when the readability benefit of the English name outweighs the conciseness of the operator.

## 17. Interview questions with model answers

**Q: When would you use a set instead of a list?**

When you need fast membership testing, uniqueness enforcement, or mathematical set operations. `x in my_list` is O(n); `x in my_set` is O(1) average. If you're checking membership repeatedly on a large collection, the set is dramatically faster. If you need deduplication, converting to a set is a one-line O(n) solution. If you need to compare two collections to find common or unique elements, set operations express that naturally and efficiently.

**Q: Why can't a list be added to a set?**

Because sets require their elements to be hashable, and hashability requires immutability. If a list were in a set and then mutated, its hash value would change, making it unfindable at its original hash location. Python enforces the hashability requirement at the type level, making mutable types (list, dict, set) unhashable and therefore ineligible as set members.

**Q: What's the difference between `remove()` and `discard()`?**

Both remove an element from a set. `remove()` raises `KeyError` if the element isn't present; `discard()` does nothing. Use `remove()` when the element's absence would be a bug you want to know about; use `discard()` when the element may or may not be present and that's acceptable.

**Q: What is a frozenset and when would you use one?**

A `frozenset` is an immutable version of a set. It supports all the read operations of a set (membership testing, set operations) but not modification. Because it's immutable, it's hashable, making it usable as a dictionary key or as an element of another set. A practical use case: a dictionary mapping sets of permissions to role names, where each key is a `frozenset` of permission strings.

## 18. Knowledge check

1. Why is `{}` an empty dictionary rather than an empty set?
2. What's the time complexity of `x in my_set` and why?
3. What does `set_a ^ set_b` produce?
4. Give one situation where converting a list to a set before checking membership changes an O(n²) operation to O(n).
5. Why can't you add a list to a set?

## 19. Hands-on exercises

**Easy**

1. Create a set of five fruits, add a duplicate, and confirm the set still has five elements.
2. Given two lists of integers, find their intersection (elements appearing in both) using sets.
3. Write a one-liner that removes all duplicates from a list using a set.

**Medium**

4. Given two lists of customer IDs from two different systems, use set operations to find: (a) customers in both systems, (b) customers only in system A, (c) customers only in system B, (d) customers in exactly one system.
5. Write a function `has_duplicates(lst)` that returns `True` if a list has any duplicate values, using a set to detect them in O(n).
6. Write a function that takes a list of tags for each document and a query set of tags, and returns all documents that contain at least one of the query tags. Use set intersection.

**Hard**

7. Implement a `UniqueQueue` class that behaves like a regular FIFO queue but rejects duplicate items (items that have already been enqueued, even if since dequeued). Use a `deque` for the queue and a `set` for the membership tracking. Discuss the tradeoff of also tracking dequeued items in the seen set.
8. Given a list of 50,000 email addresses with roughly 20% duplicates, write two deduplication functions: one using a list with `not in` checks (O(n²)) and one using a set (O(n)). Time both and print the speedup ratio.

## 20. Stretch challenge

Build a `TagIndex` class for a document tagging system. Each document has an ID and a set of tags. The `TagIndex` should support:
- `add_document(doc_id, tags)` — indexes a document and its tags
- `find_by_tag(tag)` — returns all document IDs with that tag
- `find_by_all_tags(tags)` — returns document IDs that have ALL the specified tags (set intersection across per-tag ID sets)
- `find_by_any_tag(tags)` — returns document IDs that have ANY of the specified tags (set union across per-tag ID sets)

The internal structure should be a dictionary mapping each tag to a set of document IDs. The set operations for `find_by_all_tags` and `find_by_any_tag` should be performed directly on those per-tag sets, making both operations efficient without scanning every document.

## 21. Summary

A set is a hash table of unique hashable elements, providing O(1) average membership testing, O(1) add and remove, and efficient set algebra (union, intersection, difference, symmetric difference). The two problems sets solve best are deduplication (convert to set, done) and repeated membership testing (check against a set instead of a list, O(1) per check instead of O(n)). `frozenset` is the immutable, hashable variant for use as dictionary keys or set elements. The most impactful habit to build from this lesson: before writing `if x in my_list` inside a loop, ask whether `my_list` should be a set.

## 22. Additional resources

- [Python official docs: Sets](https://docs.python.org/3/tutorial/datastructures.html#sets)
- [Python official docs: frozenset](https://docs.python.org/3/library/stdtypes.html#frozenset)
- [Python wiki: TimeComplexity — set operations](https://wiki.python.org/moin/TimeComplexity)

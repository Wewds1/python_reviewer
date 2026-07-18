# Lesson 3: Lists and Dynamic Arrays

## 1. Learning objectives

By the end of this lesson you should be able to:

- Explain how Python's list is implemented as a dynamic array at the C level
- State the time complexity of every common list operation, not just "lists are fast"
- Use slicing, list comprehensions, and nested lists correctly and efficiently
- Recognize when a list is the wrong choice and something else would be better
- Write list-heavy code that reads clearly and performs predictably

## 2. Prerequisites

Lessons 1 and 2 of this module. You need Big O notation solid before this lesson's complexity analysis will mean anything.

## 3. Introduction

Python's list is the most used data structure in the language, and also the most misused. It's so easy to reach for that it becomes a default even in situations where a set, deque, or dictionary would be dramatically faster. This lesson goes deeper than "lists store things in order" — it covers the implementation that determines performance, every operation's cost, and the specific situations where lists genuinely are the right tool and where they're not.

## 4. Theory

A Python list is a **dynamic array**: a contiguous block of memory holding references (pointers) to objects, not the objects themselves. This distinction matters:

```
list: [ref0, ref1, ref2, ref3, ...]
         ↓     ↓     ↓     ↓
        "a"  "b"   "c"   "d"    (actual objects, stored elsewhere in memory)
```

Because references are stored contiguously, index access is O(1): Python calculates the memory address of index i as `base_address + i * pointer_size` in a single arithmetic operation. There's no scanning involved.

**Dynamic resizing** is what makes it a *dynamic* array. Every Python list has both a length (how many elements it currently holds) and a capacity (how many it could hold before needing to reallocate). When you append past capacity, Python:

1. Allocates a new, larger block of memory (roughly 1.125x the current capacity)
2. Copies all existing references to the new block
3. Adds the new element
4. Frees the old block

This resize is O(n), but it happens so infrequently that appending is O(1) amortized.

## 5. Why this concept exists

The alternative to a dynamic array is either a fixed-size array (cheap but inflexible) or a linked list (flexible but O(n) for index access). Python's list is a deliberate compromise: the flexibility of dynamic resizing with the performance of array-based index access. For the vast majority of ordered-data use cases in Python, it's the right default.

## 6. Internal implementation

Under CPython, a list is implemented as a C struct containing:
- A pointer to the data array (array of `PyObject*` pointers)
- The current length (`ob_size`)
- The allocated capacity (`allocated`)

When `allocated == ob_size` and you call `.append()`, Python's list resize algorithm kicks in. The new capacity is computed as approximately `(ob_size * 9 // 8) + 6`, which is the growth pattern that produces amortized O(1) appends. You can observe this with `sys.getsizeof()`:

```python
import sys

lst = []
prev_size = sys.getsizeof(lst)
for i in range(20):
    lst.append(i)
    current = sys.getsizeof(lst)
    if current != prev_size:
        print(f"Resize at n={i+1}: {prev_size} → {current} bytes")
        prev_size = current
```

The resizes happen at 1, 5, 9, 17... elements, not on every append.

## 7. Real-world analogy

A Python list is like a hotel that occasionally needs to expand. Most nights, guests check in and get a room immediately, O(1). But occasionally the hotel is full, and the manager has to build a new wing (allocate memory), move all existing guests over (copy references), and then check in the new guest. That wing-building is expensive, but it happens rarely and adds lots of capacity at once, so the average cost per guest over time stays low.

## 8. Enterprise use cases

**Batch processing:** Processing a list of records one at a time is the backbone of ETL pipelines: read records into a list, iterate, transform, output.

**Ordered results:** Any time results need to maintain the order they were found or processed (audit logs, ranked search results, time-series data), a list is the natural structure.

**In-memory data tables:** Before data hits a database, it often lives as a list of dictionaries in memory during processing. Understanding list performance at that stage matters for pipeline throughput.

**Sliding window operations:** Rate limiting, moving averages, and session tracking often use a list as a bounded buffer, appending new items and removing old ones.

## 9. Complexity analysis

| Operation | Complexity | Notes |
|---|---|---|
| `lst[i]` (index access) | O(1) | Direct memory offset calculation |
| `lst[i] = x` (index assignment) | O(1) | Same |
| `lst.append(x)` | O(1) amortized | Occasional O(n) resize |
| `lst.pop()` (from end) | O(1) amortized | No shifting required |
| `lst.insert(i, x)` | O(n) | Everything after index i shifts right |
| `lst.pop(i)` (from middle) | O(n) | Everything after index i shifts left |
| `del lst[i]` | O(n) | Same as pop(i) |
| `x in lst` | O(n) | Linear scan — use set for repeated lookups |
| `lst.index(x)` | O(n) | Linear scan |
| `lst.sort()` | O(n log n) | Timsort in-place |
| `sorted(lst)` | O(n log n) | Returns new sorted list |
| `len(lst)` | O(1) | Stored directly on the object |
| `lst + lst2` | O(n + m) | Creates a new list |
| `lst * k` | O(nk) | Creates a new list |
| `lst[a:b]` (slicing) | O(b - a) | Creates a new list |
| `lst.reverse()` | O(n) | In-place |
| `lst.copy()` | O(n) | Shallow copy |

The most important ones to memorize: index access is O(1), insertion/deletion at the front or middle is O(n), and membership testing is O(n) (which is why you should use a set for repeated lookups).

## 10. Step-by-step visual walkthrough

**Inserting at the front of a list — why it's O(n):**

```
Initial: [A, B, C, D]   (insert X at index 0)

Step 1: Shift D right:  [A, B, C, D, D]
Step 2: Shift C right:  [A, B, C, C, D]
Step 3: Shift B right:  [A, B, B, C, D]
Step 4: Shift A right:  [A, A, B, C, D]
Step 5: Place X:         [X, A, B, C, D]
```

Every element had to move. For a list of 1 million elements, inserting at the front means 1 million shifts. This is why `collections.deque` exists specifically for front-insertion-heavy workloads.

**List comprehension vs. loop — same result, different readability:**

```python
# Explicit loop — O(n), clear but verbose
squares = []
for x in range(10):
    squares.append(x ** 2)

# List comprehension — O(n), concise and idiomatic
squares = [x ** 2 for x in range(10)]

# With filtering — O(n)
even_squares = [x ** 2 for x in range(10) if x % 2 == 0]
```

List comprehensions are not just syntactic sugar; they're slightly faster than the equivalent loop because they avoid the overhead of repeatedly calling `.append()` through the Python interpreter. The speed difference is small but real and measurable.

## 11. Syntax

**Creation:**
```python
empty = []
numbers = [1, 2, 3, 4, 5]
mixed = [1, "hello", True, None, 3.14]
from_range = list(range(1, 11))
```

**Indexing and slicing:**
```python
lst = [10, 20, 30, 40, 50]

print(lst[0])      # 10 — first element
print(lst[-1])     # 50 — last element
print(lst[1:3])    # [20, 30] — index 1 up to (not including) 3
print(lst[::2])    # [10, 30, 50] — every second element
print(lst[::-1])   # [50, 40, 30, 20, 10] — reversed
```

**Modification:**
```python
lst = [1, 2, 3]
lst.append(4)        # [1, 2, 3, 4]
lst.insert(1, 99)    # [1, 99, 2, 3, 4]
lst.remove(99)       # [1, 2, 3, 4] — removes first occurrence
lst.pop()            # [1, 2, 3] — removes and returns last element
lst.pop(0)           # [2, 3] — removes and returns element at index 0 (O(n)!)
del lst[0]           # same effect as pop(0)
lst.extend([4, 5])   # [2, 3, 4, 5] — adds all elements from another iterable
```

**Searching and sorting:**
```python
lst = [3, 1, 4, 1, 5, 9, 2]
print(lst.index(4))    # 2 — index of first occurrence
print(lst.count(1))    # 2 — how many times 1 appears
lst.sort()              # [1, 1, 2, 3, 4, 5, 9] — in-place
print(sorted(lst, reverse=True))  # [9, 5, 4, 3, 2, 1, 1] — new list
```

**Nested lists:**
```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
print(matrix[1][2])  # 6 — row 1, column 2

# Transposing a matrix with a comprehension
transposed = [[matrix[row][col] for row in range(3)] for col in range(3)]
```

**List comprehensions:**
```python
# Basic
doubles = [x * 2 for x in range(5)]

# With condition
positives = [x for x in [-3, -1, 0, 2, 4] if x > 0]

# Nested — flatten a matrix
flat = [val for row in matrix for val in row]

# With function call
cleaned = [s.strip().lower() for s in ["  Hello ", "WORLD  "]]
```

## 12. Common mistakes

**Using `pop(0)` or `insert(0, x)` repeatedly on a large list.** Both are O(n). If you need fast front insertions and removals, use `collections.deque` instead.

**Using `x in my_list` inside a tight loop.** If you're checking membership many times, convert to a set once and check membership there. Membership in a list is O(n); in a set, O(1) average.

**Assuming `list.copy()` is a deep copy.** It's a shallow copy: the list is new, but the objects inside are still shared references. Mutating a nested list inside the copy mutates the original.

```python
original = [[1, 2], [3, 4]]
shallow = original.copy()
shallow[0].append(99)
print(original)  # [[1, 2, 99], [3, 4]] — the inner list is shared
```

**Modifying a list while iterating over it**, which causes elements to be skipped or processed twice.

```python
items = [1, 2, 3, 4, 5]
for item in items:
    if item % 2 == 0:
        items.remove(item)  # dangerous — skips elements
# Safe alternative: iterate over a copy, or build a new list
items = [item for item in items if item % 2 != 0]
```

## 13. Debugging tips

If elements seem to be getting skipped during iteration, check whether you're modifying the list inside the loop. If a list operation is slower than expected, check its complexity against the table above — `insert(0, x)` on a 100,000-element list will be noticeably slow. If you're seeing unexpected shared state between two "different" lists, check whether one was created with `.copy()` (shallow) and contains mutable objects.

## 14. Best practices

Use list comprehensions for simple transformations and filters — they're more idiomatic and marginally faster than equivalent loops. Prefer `.append()` over `.insert(0, x)` for building lists; if order matters and you're prepending, build the list in reverse and call `.reverse()` at the end, which is O(n) once rather than O(n) per insertion. Use `enumerate()` instead of `range(len(lst))` when you need both index and value. Convert to a set for any repeated membership checks.

## 15. Performance considerations

For workloads involving many front insertions or deletions, `collections.deque` provides O(1) operations at both ends. For large numerical datasets, `numpy` arrays are dramatically faster than Python lists because they store actual values (not object references) in contiguous memory and can apply operations across the whole array at the C level. Python lists are the right default for general-purpose ordered collections; they're not the right tool for high-performance numerical computation.

## 16. Code style

Use `[]` rather than `list()` for empty list creation. Write list comprehensions when the logic fits on one readable line; switch to a loop when the comprehension would require nested conditionals that hurt readability. Always prefer the idiomatic approach (`enumerate`, `zip`, comprehensions) over manual index arithmetic, which is more error-prone and harder to read.

## 17. Interview questions with model answers

**Q: What's the time complexity of inserting an element at the beginning of a Python list?**

O(n), because all existing elements must be shifted one position to the right to make room at index 0. This is a consequence of the underlying array representation: elements are stored contiguously, so there's no way to insert at the front without moving everything else. If front-insertion is a frequent operation, `collections.deque` provides O(1) front insertion.

**Q: What's the difference between `list.append()` and `list.insert()`?**

`append()` adds to the end in O(1) amortized, since no shifting is required. `insert(i, x)` inserts at an arbitrary position in O(n), because everything from position i onward must shift right. For building a list incrementally, `append()` is almost always the right choice.

**Q: What's a shallow copy versus a deep copy, and when does the difference matter?**

A shallow copy (`list.copy()` or `lst[:]`) creates a new list object but copies references to the same inner objects. Mutating a mutable inner object (like a nested list) through either the original or the copy affects both. A deep copy (`copy.deepcopy()`) recursively copies every object, so the original and copy are fully independent. The difference matters whenever a list contains mutable objects as elements.

## 18. Knowledge check

1. Why is `lst[i]` O(1) for any index i?
2. Why is `lst.insert(0, x)` O(n) rather than O(1)?
3. What happens to all existing elements when a Python list needs to resize?
4. Write a list comprehension that produces the squares of all odd numbers between 1 and 20.
5. What's the safe way to filter elements from a list while iterating over it?

## 19. Hands-on exercises

**Easy**

1. Create a list of the first 10 even numbers using a list comprehension.
2. Given `lst = [5, 3, 8, 1, 9, 2]`, sort it in place and print the result, then use `sorted()` to get a reverse-sorted copy without modifying the original.
3. Write a function that returns the last three elements of any list using slicing.

**Medium**

4. Write a function `rotate_left(lst, k)` that rotates a list k positions to the left (e.g., `[1,2,3,4,5]` rotated 2 → `[3,4,5,1,2]`) without using any external library.
5. Write a function that flattens a list of lists into a single list, using a list comprehension.
6. Write a function that removes duplicates from a list while preserving the original order (without converting to a plain set, which loses order).

**Hard**

7. Write a function `chunk(lst, size)` that splits a list into chunks of a given size (the last chunk may be smaller), and return a list of lists.
8. Implement a simple sparse matrix representation using a list of lists, with methods `get(row, col)`, `set(row, col, value)`, and `transpose()`.

## 20. Stretch challenge

Implement a `DynamicArray` class from scratch (without using Python's built-in list as the primary storage mechanism, though you may use a list as a starting point to simulate a fixed-size array). Your class should support `append()`, `get(index)`, `set(index, value)`, and `length()`, and should double its capacity when full. Add a `capacity()` method that shows the current allocated size. Observe the resize events by printing when they occur. This exercise builds the mental model of what Python is doing under the hood every time you append to a list.

## 21. Summary

Python's list is a dynamic array: index access is O(1) because elements are in contiguous memory, but insertion and deletion in the middle are O(n) because everything must shift. Append is O(1) amortized because Python over-allocates and resizes infrequently. The most common performance mistake with lists is using `in` for repeated membership checks on large collections; converting to a set first changes that from O(n) per check to O(1). List comprehensions are idiomatic, slightly faster than equivalent loops, and worth using for simple transformations.

## 22. Additional resources

- [Python official docs: Lists](https://docs.python.org/3/tutorial/datastructures.html#more-on-lists)
- [Python wiki: TimeComplexity](https://wiki.python.org/moin/TimeComplexity)
- [Laurent Luce's blog: Python list implementation](http://www.laurentluce.com/posts/python-list-implementation/)

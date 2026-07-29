# 11. Recursion

## Module 11: Advanced Recursion in Enterprise Python

---

## Learning Objectives

By the end of this module, you will be able to:

- Explain call stack behavior and recursion depth management
- Implement practical recursive algorithms beyond math-only examples
- Identify and mitigate `RecursionError` and stack overflow risks
- Use memoization with `functools.lru_cache` for performance
- Solve hierarchical problems (trees, file systems, nested JSON)
- Decide when iteration is safer than recursion in Python

---

## Prerequisites

- Module 05: Stacks (LIFO fundamentals)
- Module 07: Dictionaries (key-value lookup patterns)
- Basic understanding of Python execution flow

---

## Theory: Beyond Simple Math

Factorial and Fibonacci are useful teaching examples, but enterprise recursion is usually about traversing, transforming, and searching nested structures.

Common enterprise use cases:

- Traversing file system trees
- Processing nested JSON from APIs
- Walking tree-like business objects
- Solving constrained search problems with backtracking

---

## Recursive Case Strategies

### 1. Divide and Conquer

Break one large problem into smaller independent sub-problems.

- Example: Merge Sort

### 2. Depth-First Traversal

Go as deep as possible before backtracking.

- Example: Directory crawling

### 3. Backtracking

Build candidates incrementally and prune invalid branches early.

- Example: Sudoku solver

---

## Complex Example 1: Recursive Directory Crawler

In backend operations, you may need the total size of a nested directory tree.

```python
import os


def get_total_size(path: str) -> int:
    total = 0
    try:
        if os.path.isdir(path):
            for item in os.listdir(path):
                total += get_total_size(os.path.join(path, item))
        else:
            # Base case: current path is a file
            total = os.path.getsize(path)
    except PermissionError:
        return 0

    return total
```

---

## Complex Example 2: Nested JSON / Dictionary Search

Enterprise APIs often return deeply nested payloads. Recursion helps locate keys without hardcoding path depth.

```python
def find_key(data, target_key):
    # Base case: only dictionaries can contain keys
    if not isinstance(data, dict):
        return None

    # Check current level
    if target_key in data:
        return data[target_key]

    # Recursive case: search nested dictionaries
    for value in data.values():
        if isinstance(value, dict):
            result = find_key(value, target_key)
            if result is not None:
                return result

    return None
```

---

## Performance and Optimization

### Use `functools.lru_cache`

For repetitive sub-problems, caching removes redundant work.

```python
from functools import lru_cache


@lru_cache(maxsize=128)
def fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci(n - 1) + fibonacci(n - 2)
```

### Memory complexity and recursion depth

Each recursive call consumes stack space.

- Python recursion depth is often around 1000 frames by default.
- `sys.setrecursionlimit()` should be used with extreme caution.
- If depth can exceed roughly 500 in realistic data, prefer iterative algorithms with an explicit stack.

---

## Common Production Pitfalls

- **Recursion explosion in high-traffic APIs**
  - Unbounded recursion can trigger `RecursionError` and cause service instability.
- **Missing base-case guardrails**
  - Every branch must eventually terminate.
- **Mutable default arguments**
  - Avoid mutable defaults in recursive helpers; state can leak across calls.

---

## Knowledge Check

1. Why does recursion over large file systems risk `RecursionError`?
2. How does `lru_cache` change time-space trade-offs?
3. When is an explicit stack preferable to Python's implicit call stack?

---

## Hands-on Exercises

- **Easy:** Write a recursive function to reverse a string.
- **Medium:** Flatten a nested list.
  - Input: `[1, [2, [3, 4], 5], 6]`
  - Output: `[1, 2, 3, 4, 5, 6]`
- **Hard:** Implement a recursive power-set generator (all subsets of a list).

---

## Stretch Challenge

Implement a recursive Sudoku solver using backtracking.

Explain:

- How invalid branches are detected early
- Why pruning reduces the search space dramatically
- Why the solver can still run quickly despite exponential worst-case complexity

---

## Summary

Recursion is a powerful declarative strategy when data depth is unknown or variable.

Use it responsibly:

- Validate termination paths
- Estimate maximum recursion depth
- Cache repeated sub-problems
- Switch to iterative stack-based approaches for massive or deeply nested structures

---

## Additional Resources

- Python `sys` module docs (`sys.setrecursionlimit`)
- Call stack visualizer: pythontutor.com

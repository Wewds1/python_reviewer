# Lesson 2: Time and Space Complexity

## 1. Learning objectives

By the end of this lesson you should be able to:

- Explain Big O notation in plain English, and use it correctly in a technical conversation
- Identify the time complexity of a piece of code by reading it, without running it
- Explain the difference between Big O, Big Theta, and Big Omega, and why Big O is the one that dominates practical engineering discussions
- Calculate space complexity, not just time complexity
- Explain amortized complexity and why it matters for Python's list
- Use complexity analysis to defend or critique a design choice in concrete terms

## 2. Prerequisites

Lesson 1 of this module. You need the "why does this matter" framing from Lesson 1 before the mathematical notation here will feel like more than abstract symbols.

## 3. Introduction

Big O notation is the language engineers use to talk about performance without needing to profile specific hardware, measure exact execution times, or argue about whether someone's laptop is faster than someone else's. It describes how an algorithm's resource usage scales as input size grows, which is the part that matters for engineering decisions. Two functions that both take 5ms on a dataset of 1,000 records might differ by a factor of a million when the dataset grows to 1,000,000 records, and Big O is what lets you see that coming before it happens.

## 4. Theory

**Big O notation** describes the upper bound on an algorithm's growth rate, the worst case, as a function of input size n.

```
O(1)        — constant: doesn't grow with input
O(log n)    — logarithmic: grows very slowly
O(n)        — linear: grows in direct proportion
O(n log n)  — linearithmic: common for good sorting algorithms
O(n²)       — quadratic: grows much faster than input
O(2ⁿ)       — exponential: becomes unusable quickly
```

The key insight: we drop constants and lower-order terms. `O(2n + 50)` simplifies to `O(n)`, because for large n the `2` and `50` stop mattering; what dominates is the linear growth. `O(n² + n)` simplifies to `O(n²)` for the same reason.

**Big Omega (Ω)** describes the lower bound, the best case. Linear search on a list is Ω(1) (you might find the target on the first try).

**Big Theta (Θ)** describes a tight bound, when best and worst case are the same growth rate. Accessing an element by index in a list is Θ(1), it's always constant regardless of input.

In practice, engineers almost always discuss Big O (worst case) because that's what determines how a system behaves under load, on bad data, or for unlucky inputs.

## 5. Why this concept exists

Without a shared vocabulary for performance, engineering discussions devolve into arguments about specific benchmark numbers that vary by machine, dataset, and day. Big O gives a machine-independent, input-independent way to compare algorithms and make design decisions that will hold at any scale. It's also the single most common technical interview topic in backend engineering, not because interviewers want you to do math, but because it's a proxy for whether you think about scale at all.

## 6. Internal implementation

At the hardware level, every basic operation (memory access, comparison, arithmetic) takes roughly constant time. Big O counts how many of these basic operations an algorithm performs as a function of input size. A single loop that runs n times is O(n) because it performs approximately n operations. A nested loop that runs n times inside n iterations is O(n²) because it performs approximately n² operations. The exact coefficients don't matter because we're asking "how does this grow," not "how long does this take right now."

## 7. Real-world analogy

Think of Big O as describing how long a chef's preparation time grows as the number of guests increases.

**O(1):** Checking whether a restaurant is open. Doesn't matter if you're feeding 10 people or 10,000, a single look at the sign answers the question.

**O(n):** Shaking each guest's hand as they arrive. Time grows linearly with guest count.

**O(n²):** Introducing every guest to every other guest. If you have 10 guests, that's 90 introductions. 100 guests: 9,900 introductions. 1,000 guests: essentially impossible in a reasonable timeframe.

**O(log n):** Finding a specific page in a phone book by opening to the middle, deciding which half, and repeating. 1,000 pages → about 10 decisions. 1,000,000 pages → about 20 decisions. The work grows barely at all.

## 8. Enterprise use cases

**Database query design:** An O(n²) query over a table with 10 million rows isn't a slow query, it's a system outage waiting to happen. Enterprise backend engineers think in Big O before writing queries.

**API endpoint performance:** An endpoint that runs in O(n) where n is the number of records a user has is fine at 100 records per user; it's a latency problem at 100,000.

**Data pipeline efficiency:** ETL jobs processing millions of rows need to be O(n) or O(n log n) at worst, because O(n²) at that scale simply can't finish in a business day.

## 9. Complexity analysis

**Common complexity classes, ranked from best to worst:**

| Notation | Name | Example |
|---|---|---|
| O(1) | Constant | Dictionary lookup, list index access |
| O(log n) | Logarithmic | Binary search |
| O(n) | Linear | Linear search, single loop over n items |
| O(n log n) | Linearithmic | Merge sort, Python's `sort()` |
| O(n²) | Quadratic | Nested loops, bubble sort |
| O(2ⁿ) | Exponential | Naive recursive Fibonacci |

**Space complexity** measures memory usage rather than time. An algorithm that creates a copy of its input array uses O(n) extra space. An algorithm that works in-place uses O(1) extra space. Both time and space matter; sometimes you trade one for the other deliberately.

**Amortized complexity:** Python's list `.append()` is described as O(1) amortized, not O(1) always. Occasionally, when the underlying array is full, Python must allocate a new, larger array and copy everything over, which is O(n) for that single operation. But it happens so infrequently, and each time the array doubles, the amortized cost across all appends works out to O(1) per operation on average. This is why you'll see "O(1) amortized" specifically for list append, dictionary insertion, and set insertion.

## 10. Step-by-step visual walkthrough

**Reading time complexity directly from code:**

```python
# Example 1 — O(1)
def get_first(items):
    return items[0]  # one operation, regardless of len(items)
```

```python
# Example 2 — O(n)
def find_max(items):
    max_val = items[0]       # 1 operation
    for item in items:        # n iterations
        if item > max_val:    # 1 comparison per iteration
            max_val = item
    return max_val             # 1 operation
# Total: roughly 2n + 2, simplifies to O(n)
```

```python
# Example 3 — O(n²)
def find_duplicates(items):
    duplicates = []
    for i in range(len(items)):           # n iterations
        for j in range(i + 1, len(items)):  # up to n iterations each
            if items[i] == items[j]:
                duplicates.append(items[i])
    return duplicates
# Total: roughly n²/2 comparisons, simplifies to O(n²)
```

```python
# Example 4 — O(n) with O(n) space — the better approach to duplicates
def find_duplicates_fast(items):
    seen = set()
    duplicates = []
    for item in items:           # n iterations
        if item in seen:          # O(1) set lookup
            duplicates.append(item)
        seen.add(item)            # O(1) set insertion
    return duplicates
# Time: O(n). Space: O(n) for the seen set.
```

Same problem, dramatically different time complexity. Example 3 is O(n²); Example 4 is O(n), trading O(n) extra memory for a dramatic speed improvement.

**Counting operations systematically:**

```
Step 1: Identify loops and what they iterate over (n? a constant? log n?)
Step 2: Identify nested loops (multiply their complexities)
Step 3: Identify what happens inside the loop (O(1) operations? O(n) operations?)
Step 4: Sum all terms, then keep only the dominant one
Step 5: Drop constant coefficients
```

## 11. Syntax

```python
import time

# Measuring actual runtime for comparison
def time_it(func, *args):
    start = time.time()
    result = func(*args)
    end = time.time()
    return result, end - start

# Demonstrating O(n) vs O(n²) empirically
import random

data_small = list(range(1000))
data_large = list(range(10000))

def linear(items):
    return [x for x in items if x % 2 == 0]

def quadratic(items):
    result = []
    for i in items:
        for j in items:
            if i == j and i % 2 == 0:
                if i not in result:
                    result.append(i)
    return result

_, t1 = time_it(linear, data_small)
_, t2 = time_it(linear, data_large)
print(f"Linear: {t1:.4f}s → {t2:.4f}s (ratio: {t2/t1:.1f}x)")

_, t3 = time_it(quadratic, data_small)
_, t4 = time_it(quadratic, data_large)
print(f"Quadratic: {t3:.4f}s → {t4:.4f}s (ratio: {t4/t3:.1f}x)")
# Linear ratio ≈ 10 (dataset grew 10x)
# Quadratic ratio ≈ 100 (dataset grew 10x, time grew 100x)
```

## 12. Common mistakes

**Forgetting that Big O is about growth rate, not absolute speed.** An O(n²) algorithm might be faster than an O(n) one on very small inputs if the constant factors differ significantly. Big O describes behavior at scale, not raw speed on a specific machine.

**Treating average case as worst case.** Dictionary lookup is O(1) average, but in a pathological collision scenario it degrades to O(n). Knowing both matters for defensive engineering.

**Ignoring space complexity.** An algorithm that creates a new copy of every intermediate result might be fast (time-wise) but could exhaust memory on a large dataset. Memory and time are both limited resources.

**Miscounting nested operations.** An O(n) operation inside an O(n) loop is O(n²), not O(n) + O(n). Operations inside loops multiply, not add.

## 13. Debugging tips

If code is running much slower than expected as data grows, count the loops. Two nested loops over n-sized data that you assumed were independent is often the culprit. Replacing an `in` check on a list inside a loop with a set membership check is one of the most common single-line performance fixes in Python.

## 14. Best practices

When describing a solution in an interview or code review, state its complexity proactively. "This is O(n log n) time and O(1) space" is more useful than "this should be pretty fast." Target O(n) or better for anything that runs repeatedly on large data; treat O(n²) as a warning sign that warrants a second look.

## 15. Performance considerations

Big O ignores constants, which can matter in practice. An O(n log n) algorithm with a large constant might be slower than an O(n²) one for very small n. Python's `sort()` is O(n log n) and benchmarks faster in practice than hand-written O(n) approaches that have large constant factors, because the built-in is implemented in C. Use Big O for architecture decisions; use profiling for micro-optimization.

## 16. Code style

Express complexity in comments for non-obvious algorithms, particularly for functions others will maintain. `# O(n) time, O(n) space` at the top of a function is a useful signal, the same way a docstring is. Don't annotate trivial getter functions; annotate anything where the complexity might surprise a reader.

## 17. Interview questions with model answers

**Q: Explain Big O notation in simple terms.**

Big O describes how an algorithm's resource usage grows as the input gets larger. It tells you the worst case growth rate, not the exact running time. O(n) means "if the input doubles, the work roughly doubles." O(n²) means "if the input doubles, the work quadruples." It lets engineers compare algorithms without needing to benchmark them on specific hardware.

**Q: What's the time complexity of accessing an element by index in a Python list?**

O(1) — constant time. Python lists are backed by arrays in contiguous memory, so the element at index i is at a fixed memory offset from the list's start, reachable in one operation regardless of the list's size.

**Q: What's the difference between time complexity and space complexity?**

Time complexity measures how many operations an algorithm performs as a function of input size. Space complexity measures how much additional memory it uses. Both are important: an algorithm might be O(n) in time but O(n²) in space, which trades fast execution for unacceptable memory usage at scale. The tradeoff between the two is a real engineering decision in memory-constrained environments.

**Q: Why is Python's list `append()` described as O(1) amortized rather than O(1)?**

Because occasionally, when the underlying array is full, Python allocates a new, larger array and copies all elements, which is O(n) for that one operation. But Python doubles the array size each time, so this expensive resize happens exponentially rarely. Averaged across all append operations, the cost per operation works out to a constant, giving O(1) amortized.

## 18. Knowledge check

1. What does "dropping constants" mean in Big O? Give an example.
2. What's the time complexity of a function with a loop inside a loop, both running n times?
3. An algorithm uses a sorted list and binary search for lookups. What's the complexity of each lookup?
4. What's the space complexity of a function that creates a copy of its input list?
5. Why is O(n log n) considered "good" for sorting?

## 19. Hands-on exercises

**Easy**

1. Without running anything, state the time complexity of these operations: accessing `my_list[5]`, calling `my_list.append(x)`, calling `len(my_list)`.
2. Write a function that sums all elements in a list and state its complexity.
3. Write a function with a nested loop and state why it's O(n²).

**Medium**

4. Rewrite a function that uses `if x in my_list` inside a loop to use a set instead, and explain the complexity improvement.
5. Given the following function, identify its time and space complexity and explain your reasoning:
```python
def process(items):
    result = []
    seen = set()
    for item in items:
        if item not in seen:
            result.append(item * 2)
            seen.add(item)
    return result
```
6. Write a function that finds the intersection of two lists, first in O(n²) and then in O(n), and verify both produce the same output.

**Hard**

7. Write a benchmark that empirically demonstrates the difference between O(n), O(n log n), and O(n²) by timing functions at n = 100, 1000, 10000, and printing the growth ratios.
8. Analyze this function's time and space complexity completely, showing your reasoning step by step:
```python
def nested_frequency(matrix):
    counts = {}
    for row in matrix:
        for val in row:
            counts[val] = counts.get(val, 0) + 1
    return counts
```
(Where matrix is n rows × m columns.)

## 20. Stretch challenge

Profile the Module 1 or Module 2 capstone project using Python's `cProfile` module. Identify the three most time-consuming functions, state their approximate time complexity by reading the code, and propose at least one data structure change that would improve the complexity of the slowest one. Write a short analysis (five to ten sentences) explaining your findings and proposed change.

## 21. Summary

Big O notation describes how an algorithm's performance scales with input size, and it's the primary language engineers use to compare and defend design choices. Time complexity counts operations; space complexity counts memory. Drop constants and lower-order terms to find the dominant growth term. Amortized complexity handles data structures like Python's list, where occasional expensive operations are averaged across many cheap ones. Every remaining lesson in this module will carry explicit complexity analysis, because knowing what a data structure operation costs is inseparable from knowing when to use it.

## 22. Additional resources

- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)
- [Python official docs: TimeComplexity wiki](https://wiki.python.org/moin/TimeComplexity)
- [MIT OpenCourseWare: Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-fall-2011/)

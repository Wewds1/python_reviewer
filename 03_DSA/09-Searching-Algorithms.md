# Lesson 9: Searching Algorithms

## 1. Learning objectives

By the end of this lesson you should be able to:

- Implement linear search and binary search from scratch, correctly
- State the precondition for binary search and explain why it's not optional
- Explain why binary search is O(log n) by tracing how the search space halves each step
- Choose between linear and binary search correctly given the context
- Apply binary search to problems beyond simple element lookup

## 2. Prerequisites

Lessons 1 and 2 (Introduction, Complexity). The entire point of binary search is its O(log n) complexity versus linear search's O(n) — that contrast requires the complexity vocabulary to be solid.

## 3. Introduction

Searching is one of the most fundamental operations in computing: given a collection and a target, find whether the target exists and where. Linear search requires nothing of the data — any collection in any order works. Binary search requires the data to be sorted, but in exchange delivers dramatically faster lookup. Understanding both, and when to choose each, is a daily backend engineering decision.

## 4. Theory

**Linear Search** scans every element in sequence until it finds the target or exhausts the collection. No preconditions required. O(n) worst case.

**Binary Search** repeatedly halves the search space by comparing the target to the middle element. If the target is smaller, the right half is eliminated; if larger, the left half is eliminated. Continues until the target is found or the search space is empty. **Requires sorted data.** O(log n).

The key insight for binary search: every comparison eliminates half the remaining candidates. Starting with 1,000,000 elements:

```
After 1 comparison:   500,000 candidates remain
After 2 comparisons:  250,000
After 3 comparisons:  125,000
...
After 20 comparisons: ~1 candidate remains
```

log₂(1,000,000) ≈ 20. Twenty comparisons to search one million elements. Linear search would require up to one million.

## 5. Why this concept exists

Finding things is fundamental to every software system. The reason two algorithms exist for the same operation is the classic data structures tradeoff: linear search is universally applicable but slow at scale; binary search is dramatically faster but requires the data to be sorted, which itself costs time (O(n log n)) if the data isn't already sorted. Choosing correctly requires reasoning about how often the data changes versus how often it's searched.

## 6. Internal implementation

**Linear search** iterates through the collection, comparing each element to the target. In Python, `x in list` is essentially linear search implemented in C.

**Binary search** maintains two pointers, `left` and `right`, representing the current search bounds. It repeatedly calculates the midpoint and adjusts bounds based on the comparison. The invariant is that if the target exists in the collection, it lies within `[left, right]`. When `left > right`, the target is absent.

The midpoint calculation `mid = (left + right) // 2` is worth noting — in languages with fixed-size integers (like C), the naive `(left + right) // 2` can overflow for very large arrays. The safe version is `left + (right - left) // 2`. In Python, integers are arbitrary precision so overflow isn't a concern, but it's worth knowing for interviews that discuss this in lower-level contexts.

## 7. Real-world analogy

**Linear search** is looking for a specific book in an unsorted pile: you pick up each book, check the title, set it down if it's wrong, and continue.

**Binary search** is looking for a word in a printed dictionary. You open to the middle — if your word comes before the middle word alphabetically, you look only in the left half. Open to the middle of that half — if your word comes before that, look only in the left quarter. In just a few steps, you've eliminated most of the dictionary. You can only do this because the dictionary is sorted. Nobody binary-searches a pile of randomly ordered books.

## 8. Enterprise use cases

**Database indexes:** B-trees (a generalization of binary search trees) are how database engines implement indexes. An indexed lookup on a sorted column is O(log n) instead of a full O(n) table scan.

**Configuration lookups:** Binary search is used internally by Python's `bisect` module for efficient insertion into sorted lists and sorted range lookups.

**Feature flag systems:** A sorted list of enabled feature IDs can be searched with binary search to check whether a specific feature is enabled in O(log n).

**Log file analysis:** Binary search on timestamped log files (sorted by time) lets you jump directly to a specific time range without reading the entire file.

**API rate limiting:** Binary search on a sorted list of request timestamps finds the boundary between in-window and out-of-window requests in O(log n).

## 9. Complexity analysis

| Algorithm | Best Case | Average Case | Worst Case | Space |
|---|---|---|---|---|
| Linear Search | O(1) | O(n) | O(n) | O(1) |
| Binary Search | O(1) | O(log n) | O(log n) | O(1) iterative / O(log n) recursive |

**Practical impact at scale:**

| n | Linear Search (worst) | Binary Search (worst) |
|---|---|---|
| 100 | 100 comparisons | 7 comparisons |
| 10,000 | 10,000 | 14 |
| 1,000,000 | 1,000,000 | 20 |
| 1,000,000,000 | 1,000,000,000 | 30 |

Binary search's logarithmic growth means doubling the dataset adds exactly one comparison. This is the definition of a scalable algorithm.

## 10. Step-by-step visual walkthrough

**Binary search for target = 23 in [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]:**

```
Array:  [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]
Index:   0  1  2   3   4   5   6   7   8   9  10

Step 1: left=0, right=10, mid=5
  arr[5] = 23 → TARGET FOUND at index 5 ✓

(Got lucky — found on first comparison. Let's try a harder case.)
```

**Binary search for target = 56:**

```
Array:  [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]
Index:   0  1  2   3   4   5   6   7   8   9  10

Step 1: left=0, right=10, mid=5
  arr[5] = 23
  23 < 56 → target is in RIGHT half → left = mid + 1 = 6

Step 2: left=6, right=10, mid=8
  arr[8] = 56 → TARGET FOUND at index 8 ✓

2 comparisons for 11 elements.
```

**Binary search for target = 99 (not present):**

```
Array:  [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]

Step 1: left=0, right=10, mid=5
  arr[5]=23, 23 < 99 → left = 6

Step 2: left=6, right=10, mid=8
  arr[8]=56, 56 < 99 → left = 9

Step 3: left=9, right=10, mid=9
  arr[9]=72, 72 < 99 → left = 10

Step 4: left=10, right=10, mid=10
  arr[10]=91, 91 < 99 → left = 11

Step 5: left=11 > right=10 → STOP → NOT FOUND

4 comparisons to confirm 99 is absent from an 11-element sorted array.
```

## 11. Syntax

**Linear search — explicit implementation:**
```python
def linear_search(items, target):
    """
    Search for target in items.
    Returns index of first occurrence, or -1 if not found.
    Time: O(n), Space: O(1)
    """
    for index, item in enumerate(items):
        if item == target:
            return index
    return -1

# Python's built-in: uses linear search internally
numbers = [5, 2, 9, 1, 7]
print(7 in numbers)           # True — O(n) linear scan
print(numbers.index(9))        # 2 — O(n) linear scan
```

**Binary search — iterative implementation:**
```python
def binary_search(items, target):
    """
    Search for target in a sorted list.
    Returns index of target, or -1 if not found.
    Precondition: items must be sorted in ascending order.
    Time: O(log n), Space: O(1)
    """
    left, right = 0, len(items) - 1

    while left <= right:
        mid = left + (right - left) // 2  # safe midpoint calculation

        if items[mid] == target:
            return mid
        elif items[mid] < target:
            left = mid + 1   # target is in the right half
        else:
            right = mid - 1  # target is in the left half

    return -1  # target not found

sorted_nums = [2, 5, 8, 12, 16, 23, 38, 45, 56, 72, 91]
print(binary_search(sorted_nums, 23))   # 5
print(binary_search(sorted_nums, 99))   # -1
```

**Binary search — recursive implementation:**
```python
def binary_search_recursive(items, target, left=None, right=None):
    """
    Recursive binary search.
    Time: O(log n), Space: O(log n) — due to call stack depth
    """
    if left is None:
        left = 0
    if right is None:
        right = len(items) - 1

    if left > right:
        return -1  # base case: search space exhausted

    mid = left + (right - left) // 2

    if items[mid] == target:
        return mid
    elif items[mid] < target:
        return binary_search_recursive(items, target, mid + 1, right)
    else:
        return binary_search_recursive(items, target, left, mid - 1)
```

**Python's `bisect` module — production binary search:**
```python
import bisect

sorted_list = [1, 3, 5, 7, 9, 11]

# bisect_left: index where target would be inserted to keep sorted order
idx = bisect.bisect_left(sorted_list, 7)
print(idx)  # 3

# Check if element exists
def binary_search_bisect(sorted_list, target):
    idx = bisect.bisect_left(sorted_list, target)
    if idx < len(sorted_list) and sorted_list[idx] == target:
        return idx
    return -1

print(binary_search_bisect(sorted_list, 7))   # 3
print(binary_search_bisect(sorted_list, 6))   # -1

# bisect.insort: insert maintaining sorted order — O(n) due to list shift
bisect.insort(sorted_list, 6)
print(sorted_list)  # [1, 3, 5, 6, 7, 9, 11]
```

**Binary search applied beyond simple lookup — finding a boundary:**
```python
def first_occurrence(items, target):
    """
    Find the index of the FIRST occurrence of target in a sorted list
    (handles duplicates correctly).
    Time: O(log n)
    """
    left, right = 0, len(items) - 1
    result = -1

    while left <= right:
        mid = left + (right - left) // 2
        if items[mid] == target:
            result = mid       # record this match
            right = mid - 1   # but keep searching LEFT for earlier occurrence
        elif items[mid] < target:
            left = mid + 1
        else:
            right = mid - 1

    return result

print(first_occurrence([1, 2, 2, 2, 3, 4], 2))  # 1 (first occurrence)
```

## 12. Common mistakes

**Applying binary search to unsorted data.** Binary search silently produces wrong answers on unsorted data — it doesn't error out, it just finds the wrong element or returns -1 falsely. Always verify or enforce the sorted precondition.

**Off-by-one errors in boundary conditions.** The most common bug: using `left < right` instead of `left <= right` in the while condition, which misses the final element. Using `mid - 1` and `mid + 1` correctly to avoid infinite loops when `left == right`.

**Infinite loop when not updating boundaries correctly.** If `left = mid` instead of `left = mid + 1` when the target is in the right half, the loop can get stuck cycling between the same two indices.

**Forgetting that `bisect` returns an insertion point, not a membership result.** `bisect.bisect_left(lst, x)` returns where `x` would be inserted, not whether `x` is present. You must check `lst[idx] == x` afterward.

## 13. Debugging tips

If binary search returns wrong results, trace through the first few iterations manually with a small sorted example and print `left`, `right`, `mid`, and `items[mid]` on each iteration. Off-by-one errors are almost always the cause. If it returns -1 for an element you know is present, check whether the input is actually sorted and whether the comparison direction (< vs >) is correctly oriented for ascending versus descending sort.

## 14. Best practices

In production Python code, use `bisect` from the standard library rather than a hand-rolled binary search — it's implemented in C, handles edge cases correctly, and is well-tested. Hand-roll binary search in interviews to demonstrate understanding. Always document the sorted precondition on any function that uses binary search. Consider whether the cost of sorting (O(n log n)) is worth the repeated O(log n) lookups; if you only search once, linear search on an unsorted list is cheaper overall.

## 15. Performance considerations

**When is sorting + binary search worth it?**

Sort cost: O(n log n), one time.
Binary search: O(log n) per lookup.
Total for k lookups on a pre-sorted list: O(n log n) + k·O(log n).

Linear search on unsorted list: k·O(n).

Break-even: sorting pays off when `k · O(log n) < k · O(n)`, which is essentially always for k > 1 and any meaningful n. The exception: if you're only ever searching once and the data isn't already sorted, linear search on the unsorted data saves the sort cost.

## 16. Code style

Name binary search functions to communicate the precondition: `search_sorted(items, target)` is clearer than `binary_search(items, target)`. Always document `# Precondition: items must be sorted` in the docstring. For production code, prefer `bisect` over hand-rolled implementations.

## 17. Interview questions with model answers

**Q: What is the precondition for binary search and why?**

Binary search requires the data to be sorted in a consistent order. The algorithm works by eliminating half the remaining candidates on each step based on a comparison with the midpoint. This elimination is only valid if the data is ordered — if elements are random, concluding "the target is in the right half because it's greater than the midpoint" is not a valid inference. Binary search on unsorted data produces wrong answers without raising any error.

**Q: Explain why binary search is O(log n).**

Each comparison eliminates half the remaining search space. Starting with n elements, after one comparison you have n/2, after two you have n/4, and so on. The number of steps needed to reduce n to 1 is log₂(n). That's the definition of logarithm: log₂(n) is the exponent k such that 2^k = n. For n = 1,000,000, log₂(1,000,000) ≈ 20, meaning binary search finds any element (or determines it's absent) in at most 20 comparisons.

**Q: When would you choose linear search over binary search?**

When the data isn't sorted and sorting it would cost more than the search saves (searching only once on an unsorted collection). When the collection is very small (under ~20 elements), where linear search's simplicity outweighs the asymptotic advantage of binary search. When you need to find all occurrences, not just one. When the data is not a random-access structure (like a linked list), where binary search's midpoint calculation can't be done in O(1).

## 18. Knowledge check

1. What is the maximum number of comparisons binary search needs to find an element in a sorted list of 1,024 elements?
2. What goes wrong if you apply binary search to an unsorted list?
3. What does `bisect.bisect_left(lst, x)` return, and what additional check is needed to verify the element is present?
4. Write the loop condition for iterative binary search and explain why `<=` matters.

## 19. Hands-on exercises

**Easy**

1. Implement `linear_search(items, target)` that returns the index of the first occurrence of `target`, or `-1` if not found.
2. Implement `binary_search(items, target)` iteratively and test it against a sorted list of 10 elements, verifying both found and not-found cases.
3. Confirm that `binary_search` fails silently on an unsorted list by testing it on `[5, 2, 8, 1, 9]` for a target that is present.

**Medium**

4. Implement `count_occurrences(sorted_list, target)` using two binary searches: one to find the first occurrence and one to find the last, then return `last - first + 1`. Time complexity should be O(log n).
5. Use Python's `bisect` module to implement a `SortedList` class that maintains a sorted list and supports O(log n) `contains(x)` and O(log n + k) `insert(x)` where k accounts for the O(k) shift in the underlying list.
6. Implement binary search on a list of dictionaries sorted by a `"score"` field, finding the first record with score ≥ a given threshold.

**Hard**

7. Implement `binary_search_rotated(items, target)` that searches a sorted array that has been rotated at some unknown pivot point (e.g., `[4, 5, 6, 7, 0, 1, 2]`). This requires determining which half is sorted on each step before deciding which half to search.
8. Implement a `guess_number` game simulation: you're searching for a number between 1 and 1,000,000. Your only feedback is "too high," "too low," or "correct." Implement binary search as the guessing strategy and prove it finds any number in at most 20 guesses.

## 20. Stretch challenge

Implement binary search on a **virtual sorted dataset** that's too large to fit in memory. Simulate this with a function `get_element(index)` that returns the element at a given index (as if it were reading from a file or database). Your binary search should call `get_element()` only O(log n) times regardless of n. Track the number of `get_element()` calls and verify it never exceeds ⌈log₂(n)⌉ + 1 for any input.

## 21. Summary

Linear search works on any collection in any order, running in O(n). Binary search requires sorted data but runs in O(log n), making it dramatically faster at scale — 20 comparisons for 1 million elements rather than 1 million. The choice comes down to whether the data is sorted, how often it will be searched, and whether sorting it first is worth the O(n log n) upfront cost. In production Python, use `bisect` rather than hand-rolled binary search. In interviews, implement it from scratch and be ready to explain the loop invariant, boundary conditions, and why the algorithm terminates correctly.

## 22. Additional resources

- [Python official docs: bisect — Array bisection algorithm](https://docs.python.org/3/library/bisect.html)
- [Wikipedia: Binary search algorithm](https://en.wikipedia.org/wiki/Binary_search_algorithm)
- [Visualgo: Binary Search visualization](https://visualgo.net/en/bst)

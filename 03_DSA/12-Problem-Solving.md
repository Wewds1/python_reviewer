
def same_frequency(list1, list2):
    """
    Checks if two lists have the exact same elements and frequencies.
    """
    # Quick exit: if lengths differ, they can't have the same frequencies
    if len(list1) != len(list2):
        return False
        
    # Step 1: Build a frequency map for the first list
    # Python's built-in Counter does this efficiently in O(N) time
    counts1 = Counter(list1) 
    
    # Step 2: Build a frequency map for the second list
    counts2 = Counter(list2)
    
    # Step 3: Compare the dictionaries (O(N) operation)
    return counts1 == counts2
    """Finds the first pair of numbers in a sorted array that sum to zero."""
    left = 0
    right = len(sorted_arr) - 1
    
    while left < right:
        current_sum = sorted_arr[left] + sorted_arr[right]
        
        if current_sum == 0:
            return (sorted_arr[left], sorted_arr[right])
        elif current_sum > 0:
            # Sum is too large, move the right pointer down to a smaller number
            right -= 1
        else:
            # Sum is too small, move the left pointer up to a larger number
            left += 1
            
    return None
    """Finds the maximum sum of 'k' consecutive elements."""
    if len(arr) < k:
        return None
    
    # Calculate the sum of the VERY FIRST window
    max_sum = sum(arr[:k])
    current_window_sum = max_sum
    
    # Slide the window from index 'k' to the end of the array
    for i in range(k, len(arr)):
        # Subtract the element leaving the window behind, add the new element ahead
        current_window_sum = current_window_sum - arr[i - k] + arr[i]
        
        # Update max_sum if the current window is larger
        max_sum = max(max_sum, current_window_sum)
        
    return max_sum
# Module 12 — Problem Solving Patterns in Enterprise Python

## Learning objectives

By the end of this module you will be able to:

- Identify recurring algorithmic patterns in real-world backend tasks.
- Optimize O(N^2) brute-force solutions into O(N) or O(N log N) implementations.
- Apply the Frequency Counter pattern for efficient data comparison and deduplication.
- Utilize Two Pointers to navigate sequences without redundant iterations.
- Implement the Sliding Window pattern to analyze time-series data or substrings.
- Recognize when to apply Greedy logic vs exhaustive search.
- Communicate algorithmic choices and time-space trade-offs in interviews.

## Prerequisites

- Module 03: Lists and Dynamic Arrays
- Module 07: Dictionaries and Hash Tables
- Module 09: Searching Algorithms
- Module 10: Sorting Algorithms

## Introduction

In enterprise development you rarely invent new algorithms — you map business problems to known patterns (fraud detection, reconciliation, rolling-window analytics). These patterns trade small amounts of memory for large gains in time complexity.

### Real-world analogy

Finding duplicates by brute force is like comparing every receipt in Cabinet A to every receipt in Cabinet B (O(N^2)). A Frequency Counter is like making one quick tally sheet for Cabinet B, then checking Cabinet A against it (O(N)).

## Pattern 1 — Frequency Counter

### When to use

Comparing datasets, checking anagrams, counting occurrences, reconciling CSV exports against a DB dump.

### Complexity

- Time: O(N)
- Space: O(N)

### Example: compare frequencies of two lists

```python
from collections import Counter

def same_frequency(list1, list2):
    """Return True if both lists contain the same elements with the same frequencies."""
    if len(list1) != len(list2):
        return False
    return Counter(list1) == Counter(list2)
```

### Visual example

For `list1 = [1,2,2]` and `list2 = [2,1,2]`, both Counters equal `{1:1, 2:2}` → True.

## Pattern 2 — Two Pointers

### When to use

Sorted arrays or strings, finding complementary pairs, or problems where two indices move toward each other.

### Complexity

- Time: O(N)
- Space: O(1)

### Example: find first pair summing to zero in a sorted array

```python
def sum_zero(sorted_arr):
    left, right = 0, len(sorted_arr) - 1
    while left < right:
        s = sorted_arr[left] + sorted_arr[right]
        if s == 0:
            return (sorted_arr[left], sorted_arr[right])
        if s > 0:
            right -= 1
        else:
            left += 1
    return None
```

## Pattern 3 — Sliding Window

### When to use

Subarray/subsequence problems where you need an aggregate over contiguous elements (sums, counts, max/min) and want to avoid recomputing overlapping state.

### Complexity

- Time: O(N)
- Space: O(1)

### Example: maximum sum of `k` consecutive elements

```python
def max_subarray_sum(arr, k):
    if len(arr) < k:
        return None
    current = sum(arr[:k])
    best = current
    for i in range(k, len(arr)):
        current += arr[i] - arr[i - k]
        best = max(best, current)
    return best
```

## Pattern 4 — Greedy (intro)

Make the locally optimal choice at each step when that leads to a global optimum (e.g., interval scheduling, some shortest-path heuristics). Greedy choices are simple and fast but require proof they lead to an optimal solution.

## Common mistakes & debugging tips

- Over-engineering: prefer built-in `collections.Counter` over manual loops unless asked.
- Off-by-one errors: carefully test boundary conditions for pointers and windows.
- Unsorted data: sort before applying two-pointer patterns when necessary.
- Debug: print pointer positions and window boundaries when stuck.

## Best practices

- Use descriptive variable names (`left_index`, `right_index`, `window_start`).
- Include docstrings with time/space complexity.
- Avoid mutating inputs while iterating.

## Quick Q&A

- Q: When choose Two Pointers vs Hash Table?
  - A: Use Two Pointers when data can be sorted or is already sorted and you need O(1) extra space. Hash tables give O(N) time but O(N) space.

## Knowledge check

1. Which pattern is best for detecting anagrams? (Answer: Frequency Counter)
2. What is the space complexity of Two Pointers? (Answer: O(1))
3. Why often sort before using Two Pointers? (Answer: pointers rely on order to move deterministically)
4. What if `k` > len(arr) in a fixed-size sliding window? (Answer: handle as special case — return None or 0 depending on problem)

## Hands-on exercises (with example solutions)

### Easy — contains_duplicate (Frequency Counter)

```python
def contains_duplicate(nums):
    """Return True if any value appears at least twice."""
    from collections import Counter
    return any(count > 1 for count in Counter(nums).values())

# Alternative O(N) early-exit implementation
def contains_duplicate_early(nums):
    seen = set()
    for n in nums:
        if n in seen:
            return True
        seen.add(n)
    return False
```

### Medium — reverse_vowels (Two Pointers)

```python
def reverse_vowels(s):
    vowels = set('aeiouAEIOU')
    s = list(s)
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] not in vowels:
            left += 1
            continue
        if s[right] not in vowels:
            right -= 1
            continue
        s[left], s[right] = s[right], s[left]
        left += 1
        right -= 1
    return ''.join(s)
```

### Hard — longest_unique_substring (Sliding Window, dynamic)

```python
def longest_unique_substring(s):
    last_index = {}
    start = 0
    best = 0
    for i, ch in enumerate(s):
        if ch in last_index and last_index[ch] >= start:
            start = last_index[ch] + 1
        last_index[ch] = i
        best = max(best, i - start + 1)
    return best
```

### Stretch — minimal-length subarray with sum >= target (dynamic sliding window)

```python
def min_subarray_len(target, nums):
    n = len(nums)
    left = 0
    total = 0
    best = float('inf')
    for right in range(n):
        total += nums[right]
        while total >= target:
            best = min(best, right - left + 1)
            total -= nums[left]
            left += 1
    return 0 if best == float('inf') else best
```

## Summary

These patterns are essential for backend performance engineering. Applying the right pattern lets you handle millions of rows and high-throughput systems efficiently.

## Additional resources

- Grokking Algorithms by Aditya Bhargava
- Python `collections` module documentation
- LeetCode Patterns: "Sliding Window" and "Two Pointers"

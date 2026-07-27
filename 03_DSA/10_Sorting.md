# 10. Sorting

**Course:** Enterprise Python Backend Developer Bootcamp  
**Target role:** Python Developer Associate / Backend Engineer  
**Prerequisites:**

- 01 - Introduction to DSA
- 02 - Time and Space Complexity
- 03 - Lists and Dynamic Arrays
- 09 - Searching Algorithms

---

## 1. Learning Objectives

By the end of this lesson, you should be able to:

- Explain how Bubble Sort, Selection Sort, and Insertion Sort work.
- Explain divide-and-conquer strategies used by Merge Sort and Quick Sort.
- Distinguish in-place vs out-of-place sorting and stable vs unstable sorting.
- Use Python `list.sort()` and `sorted()` with custom `key` functions.
- Explain why Python uses Timsort and when it performs especially well.
- Choose practical sorting strategies for enterprise backend workloads.

---

## 2. Prerequisites

- Big-O notation: $O(1)$, $O(n)$, $O(n^2)$, $O(n \log n)$
- Python lists and mutation behavior
- Basic logarithms and recursion intuition
- Loops, conditionals, and function design

---

## 3. Why Sorting Matters in Backend Systems

Sorting is not just an interview topic. In backend systems, sorting impacts:

- Query performance and pagination
- Deduplication and reconciliation workflows
- Memory pressure and CPU usage
- Event ordering and deterministic processing

Even when using built-in sorting in production, understanding sorting behavior helps you avoid scalability and correctness problems.

---

## 4. Core Concepts

### 4.1 In-Place vs Out-of-Place

- **In-place:** Reorders data inside the same container with minimal extra memory.
  - Example: Insertion Sort, Selection Sort, most Quick Sort implementations.
- **Out-of-place:** Uses additional buffers during sorting.
  - Example: Merge Sort.

### 4.2 Stable vs Unstable

- **Stable sort:** Preserves original order for equal keys.
- **Unstable sort:** Equal-key records may be reordered.

Stability is important for multi-key business records. If you sort by secondary key first, then sort by primary key, the second pass must be stable to preserve secondary ordering.

---

## 5. Why Learn This If Python Already Has `sort()`?

### 5.1 The lower bound

Comparison-based sorting has a theoretical lower bound of $\Omega(n \log n)$ in the general case.

### 5.2 Data-shape adaptivity

No one algorithm is best for all data. Nearly sorted data behaves very differently from random or reverse-ordered data.

### 5.3 Real-world scale

At large data sizes (or when data exceeds memory), you need external sorting patterns and careful architecture choices.

---

## 6. Algorithm Overview

### 6.1 Bubble Sort

- Repeatedly compare adjacent values and swap when out of order.
- Largest unsorted values move toward the end each pass.

### 6.2 Selection Sort

- Repeatedly select the minimum value from unsorted region.
- Place it at the current boundary.

### 6.3 Insertion Sort

- Build a sorted prefix one element at a time.
- Shift larger elements right and insert current value.

### 6.4 Merge Sort

- Recursively split the list.
- Merge sorted halves.
- Predictable $O(n \log n)$ runtime and stable behavior.

### 6.5 Quick Sort

- Partition around a pivot.
- Recursively sort partitions.
- Fast average case, but poor pivot strategy can degrade to $O(n^2)$.

---

## 7. Enterprise Algorithm Selection Matrix

| Algorithm | Avg Time | Space | Stable | Typical Enterprise Use |
|---|---|---|---|---|
| Insertion Sort | $O(n^2)$ | $O(1)$ | Yes | Tiny payloads, nearly sorted buffers, hybrid sort base cases |
| Merge Sort | $O(n \log n)$ | $O(n)$ | Yes | Stable object sorting, external disk-based sorting |
| Quick Sort | $O(n \log n)$ | $O(\log n)$ stack | No | Fast in-memory primitive sorting where stability is not required |
| Timsort | $O(n \log n)$ | $O(n)$ | Yes | Python production default, adaptive to real-world partially sorted data |

---

## 8. Practical Scenarios

### Scenario A: Financial reconciliation

Sort by account while preserving timestamp order within each account. Use a stable sort (Timsort or Merge Sort).

### Scenario B: IoT edge ingestion

When packets are mostly ordered with occasional jitter, Insertion Sort can be very efficient for small sliding buffers.

---

## 9. Complexity Summary

| Algorithm | Worst | Average | Best | Space |
|---|---|---|---|---|
| Bubble Sort | $O(n^2)$ | $O(n^2)$ | $O(n)$* | $O(1)$ |
| Selection Sort | $O(n^2)$ | $O(n^2)$ | $O(n^2)$ | $O(1)$ |
| Insertion Sort | $O(n^2)$ | $O(n^2)$ | $O(n)$ | $O(1)$ |
| Merge Sort | $O(n \log n)$ | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ |
| Quick Sort | $O(n^2)$** | $O(n \log n)$ | $O(n \log n)$ | $O(\log n)$*** |
| Timsort | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | $O(n)$ |

\* With early-exit optimization.  
\** Worst case with poor pivot behavior.  
\*** Recursion stack in balanced cases.

---

## 10. Worked Example: Insertion Sort

Input: `[5, 2, 4, 6, 1, 3]`

- Pass 1: Insert `2` before `5` -> `[2, 5, 4, 6, 1, 3]`
- Pass 2: Insert `4` between `2` and `5` -> `[2, 4, 5, 6, 1, 3]`
- Pass 3: `6` already in place -> `[2, 4, 5, 6, 1, 3]`
- Pass 4: Insert `1` at front -> `[1, 2, 4, 5, 6, 3]`
- Pass 5: Insert `3` after `2` -> `[1, 2, 3, 4, 5, 6]`

---

## 11. Merge Sort Mental Model

Merge Sort repeatedly:

1. Splits input into halves until length is 1
2. Merges sorted sublists while preserving order

This structure gives consistent performance and stability.

---

## 12. Python Implementations

### 12.1 Bubble, Selection, Insertion

```python
from typing import Any


def bubble_sort(arr: list[Any]) -> list[Any]:
    n = len(arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        if not swapped:
            break
    return arr


def selection_sort(arr: list[Any]) -> list[Any]:
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


def insertion_sort(arr: list[Any]) -> list[Any]:
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr
```

### 12.2 Merge Sort and Quick Sort

```python
import random
from typing import Any


def merge_sort(arr: list[Any]) -> list[Any]:
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left = merge_sort(arr[:mid])
    right = merge_sort(arr[mid:])
    return _merge(left, right)


def _merge(left: list[Any], right: list[Any]) -> list[Any]:
    merged: list[Any] = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1

    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def quick_sort(arr: list[Any], low: int = 0, high: int | None = None) -> list[Any]:
    if high is None:
        high = len(arr) - 1

    if low < high:
        pivot_idx = _randomized_partition(arr, low, high)
        quick_sort(arr, low, pivot_idx - 1)
        quick_sort(arr, pivot_idx + 1, high)
    return arr


def _randomized_partition(arr: list[Any], low: int, high: int) -> int:
    rand_idx = random.randint(low, high)
    arr[rand_idx], arr[high] = arr[high], arr[rand_idx]
    return _partition(arr, low, high)


def _partition(arr: list[Any], low: int, high: int) -> int:
    pivot = arr[high]
    i = low - 1
    for j in range(low, high):
        if arr[j] <= pivot:
            i += 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1
```

---

## 13. Built-In Sorting: `list.sort()` vs `sorted()`

```python
# Mutates in place and returns None
ids = [1042, 8831, 2011, 4099]
ids.sort(reverse=True)

# Returns a new list
immutable_ids = (55, 12, 89, 3)
ordered = sorted(immutable_ids)
```

### Key-function engineering

```python
from dataclasses import dataclass
from operator import attrgetter

transactions = [
    {"tx_id": "TX-901", "amount": 4500.50, "status": "PENDING"},
    {"tx_id": "TX-102", "amount": 120.00, "status": "SETTLED"},
    {"tx_id": "TX-443", "amount": 4500.50, "status": "SETTLED"},
]

transactions.sort(key=lambda x: (-x["amount"], x["status"]))


@dataclass
class Employee:
    emp_id: int
    name: str
    department: str
    salary: int


employees = [
    Employee(101, "Zoe Chen", "Engineering", 145000),
    Employee(102, "Alex Smith", "Consulting", 120000),
    Employee(103, "Bob Vance", "Consulting", 120000),
]

employees.sort(key=attrgetter("department", "salary"))
```

---

## 14. Common Mistakes

- Expecting `list.sort()` to return a new list
- Using unstable sort behavior for multi-key records
- Choosing predictable pivots in Quick Sort (`arr[0]`, `arr[-1]`) without protection
- Sorting mixed incomparable types in Python 3 (causes `TypeError`)

---

## 15. Debugging Tips

- Test edge cases:
  - `[]`
  - `[42]`
  - already sorted list
  - all equal elements
- For Quick Sort recursion bugs, log `low`, `high`, and pivot index each call.

---

## 16. Performance Best Practices

- Prefer built-in Python sorting in production.
- Use composite keys instead of writing manual comparison loops.
- For nearly sorted data, built-in Timsort can approach near-linear behavior.
- In large pipelines, measure before replacing built-in behavior.

---

## 17. Hands-On Challenges

### Level 1 (Easy): Sort server logs

```python
from typing import List


def sort_server_logs(logs: List[str]) -> List[str]:
    # ISO timestamps sort lexicographically in chronological order
    return sorted(logs)
```

### Level 2 (Medium): Multi-attribute client sorting

```python
from typing import Any


def sort_enterprise_clients(clients: list[dict[str, Any]]) -> list[dict[str, Any]]:
    sla_weights = {"PLATINUM": 1, "GOLD": 2, "SILVER": 3, "BRONZE": 4}

    def key_fn(c: dict[str, Any]):
        return (
            -c["contract_value"],
            sla_weights.get(c["sla_tier"], 99),
            c["company_name"].lower(),
        )

    return sorted(clients, key=key_fn)
```

### Level 3 (Hard): Dutch National Flag

```python
def sort_packet_priorities(arr: list[int]) -> list[int]:
    low = 0
    mid = 0
    high = len(arr) - 1

    while mid <= high:
        if arr[mid] == 0:
            arr[low], arr[mid] = arr[mid], arr[low]
            low += 1
            mid += 1
        elif arr[mid] == 1:
            mid += 1
        else:
            arr[mid], arr[high] = arr[high], arr[mid]
            high -= 1
    return arr
```

---

## 18. Interview Questions

1. Why does Python use Timsort instead of Quick Sort by default?
2. Compare Merge Sort vs Quick Sort space complexity and container memory impact.
3. How would you sort massive logs when data does not fit in memory?
4. Why is stability critical for multi-key enterprise records?

---

## 19. Stretch Challenge: External Merge Sort

Design an out-of-core sorting engine:

1. Read a large input file in fixed-size chunks.
2. Sort each chunk in memory.
3. Write sorted chunks to temporary files.
4. Merge all chunks with `heapq.merge`.
5. Stream final sorted output to destination file.
6. Delete temporary files.

Target complexity for merge phase: $O(n \log k)$ where $k$ is the number of chunk files.

---

## 20. Summary

- Comparison sorts have a lower bound of $\Omega(n \log n)$ in general.
- Insertion Sort is useful for tiny or nearly sorted inputs.
- Merge Sort offers stable and predictable performance.
- Quick Sort is strong on average but needs safe pivot handling.
- Python uses Timsort, which is adaptive and stable for real-world data.

---

## 21. Additional Resources

- Python docs: Sorting HOW TO
- Tim Peters notes on Timsort
- Papers and talks on practical Quick Sort improvements (for deeper study)

# Lesson 1: Introduction to Data Structures & Algorithms

## 1. Learning objectives

By the end of this lesson you should be able to:

- Explain what a data structure is and what an algorithm is, in your own words, not just by definition
- Articulate why the choice of data structure directly determines an algorithm's performance
- Describe the fundamental trade-off between speed and memory in real backend systems
- Recognize the kinds of real engineering decisions this module is building toward

## 2. Prerequisites

Modules 1 and 2, or equivalent Python fundamentals. You should be comfortable with lists, dictionaries, functions, and classes before this module's concepts will have the right context to land.

## 3. Introduction

Every program you've written so far has made implicit choices about how to store and process data. You've used lists, dictionaries, and sets. You've written loops and functions. This module makes those choices explicit and teaches you to make them deliberately, because the same problem solved with the right data structure can be a thousand times faster than the same problem solved with the wrong one, and at enterprise scale, "a thousand times faster" is often the difference between a feature that works and one that doesn't.

## 4. Theory

A **data structure** is a way of organizing data in memory so it can be used efficiently. Different structures make different operations fast or slow: a list makes indexed access fast, a set makes membership testing fast, a queue makes first-in-first-out access predictable. The structure you choose determines which operations are cheap and which are expensive.

An **algorithm** is a step-by-step procedure for solving a problem or performing a computation. Algorithms don't exist in isolation from data structures: binary search is fast because it assumes the data is already sorted in a list; a hash map lookup is fast because a dictionary's underlying structure is designed specifically to support it. The two are inseparable.

```python
# Two solutions to the same problem: which names from list_a appear in list_b?

names_a = ["Alex", "Sam", "Jordan", "Taylor"]
names_b = ["Jordan", "Sam", "Riley", "Casey"]

# Solution 1: nested loops — O(n²)
common_slow = []
for name in names_a:
    for other in names_b:
        if name == other:
            common_slow.append(name)

# Solution 2: convert list_b to a set first — O(n)
set_b = set(names_b)
common_fast = [name for name in names_a if name in set_b]

print(common_slow)  # ['Sam', 'Jordan']
print(common_fast)  # ['Sam', 'Jordan']
```

Both produce the same answer. With four names each, the difference is invisible. With 100,000 names each, Solution 1 makes 10 billion comparisons; Solution 2 makes 100,000. That gap is what this module is about.

## 5. Why this concept exists

Software engineering at scale consistently runs into the same fundamental problem: the amount of data grows, and code that worked fine at small scale becomes unbearably slow or runs out of memory. Understanding data structures and algorithms gives you the vocabulary and judgment to design solutions that stay fast as data grows, rather than discovering the problem in production when a client's dataset is ten times larger than the one you tested on.

## 6. Internal implementation

At the hardware level, all data is ultimately stored in memory as bytes, and the CPU accesses it through memory addresses. A data structure is really a contract about how those bytes are arranged: a list stores elements in contiguous memory (which makes indexed access O(1) but insertion at the front O(n)); a hash table distributes elements across memory buckets using a hash function (which makes lookup O(1) average but insertion O(1) amortized). The specific guarantees each structure provides come directly from these physical arrangements.

## 7. Real-world analogy

Think of data structures as different ways of organizing a library's books, and algorithms as the different strategies a librarian uses to find something.

A **list** is books stacked in a single pile: you can grab the third one from the top instantly (indexed access), but inserting one in the middle means moving every book above it.

A **dictionary** is books arranged alphabetically by author with an index card system: looking up any author is nearly instant regardless of how many books there are, because the index tells you exactly where to go.

A **set** is a guest list at a door: the bouncer doesn't read the whole list to check if your name is there, they check it in roughly constant time using the same index trick.

The **algorithm** is the librarian's actual procedure: do they scan every shelf, or do they go straight to the index?

## 8. Enterprise use cases

**Financial systems:** A bank processing millions of daily transactions needs to look up account balances, detect duplicate transactions, and sort records for reporting. The difference between O(n) and O(1) lookup at this scale is measurable in real seconds on real hardware.

**Search and filtering:** A consulting dashboard filtering 500,000 client records by region and status needs algorithms that avoid scanning every record for every filter. Indexed lookup structures make this tractable.

**Task scheduling:** An enterprise workflow system queuing hundreds of tasks for background workers relies on queue data structures with guaranteed ordering properties, not ad-hoc lists.

**Data deduplication:** ETL pipelines processing client data extract often need to deduplicate millions of records. A set-based approach does this in O(n) where a naive nested-loop approach would be O(n²).

## 9. Complexity analysis

This section is a preview; the full treatment is Lesson 2. The core idea: we measure how an algorithm's performance scales as the input size grows, expressed as a function of n (the input size).

| Algorithm approach | Input size doubles | Time roughly |
|---|---|---|
| O(1) — constant | doubles | stays the same |
| O(n) — linear | doubles | doubles |
| O(n²) — quadratic | doubles | quadruples |

The nested loop approach above is O(n²). The set approach is O(n). At n=1000, that's 1,000,000 operations versus 1,000. At n=1,000,000, it's 10¹² versus 10⁶.

## 10. Step-by-step visual walkthrough

**Finding a name in a list of 8 names: two approaches side by side.**

Names: `["Alex", "Sam", "Jordan", "Taylor", "Riley", "Casey", "Morgan", "Drew"]`
Target: `"Morgan"`

**Linear search (no structure advantage):**
```
Check Alex    → no
Check Sam     → no
Check Jordan  → no
Check Taylor  → no
Check Riley   → no
Check Casey   → no
Check Morgan  → YES — found at step 7
```
7 comparisons for 8 elements. At 8 million elements, up to 8 million comparisons.

**Set membership (structure advantage):**
```
Hash "Morgan" → jump directly to the right memory location → found
```
1 effective operation regardless of how many elements are in the set.

That's the entire argument for choosing the right data structure.

## 11. Syntax

```python
# Picking the right structure for the right job

# Ordered, duplicates allowed, index access needed → list
tasks = ["write tests", "deploy", "write docs"]

# Fast membership testing, no duplicates → set
processed_ids = {1001, 1002, 1003}

# Key-value lookup, fast retrieval by identifier → dict
user_by_id = {1001: "Alice", 1002: "Bob"}

# Fixed, unchanging data → tuple
coordinates = (37.7749, -122.4194)

# FIFO processing order → collections.deque (preview)
from collections import deque
task_queue = deque(["task_a", "task_b", "task_c"])
```

## 12. Common mistakes

**Defaulting to a list for everything.** Lists are versatile, but `if item in my_list` is O(n). If you're checking membership repeatedly on a large collection, you want a set or a dictionary, not a list.

**Optimizing prematurely.** Don't reach for a complex data structure when a simple one solves the problem at the scale you're actually working with. Profile first; optimize what's actually slow.

**Conflating "works" with "works at scale."** Code that produces correct results on your test data and crushes in production when the dataset is a hundred times larger is one of the most common production failures in backend engineering.

## 13. Debugging tips

When code is unexpectedly slow, the first question is "what operation is being performed most often inside a loop?" If that operation is `in` on a list, and the list is large, replacing it with a set lookup is often a one-line fix with a dramatic performance payoff.

## 14. Best practices

Before writing a solution, ask: what operations need to be fast? Lookup? Insertion? Ordering? Uniqueness? The answer tells you which data structure to start with. Write correct code first, measure it against realistic data sizes, then optimize the specific operations that are actually slow.

## 15. Performance considerations

Memory and speed are in constant tension. A set gives you fast lookup but uses more memory than a sorted list with binary search. A hash table gives you O(1) average lookup but degrades to O(n) in worst-case collision scenarios. Understanding these trade-offs is what separates someone who memorizes data structures from someone who actually engineers with them.

## 16. Code style

Use the most semantically honest structure for your data: if something shouldn't have duplicates, use a set and communicate that intent clearly to the next reader. If something is ordered, a list makes that explicit. Choosing the right structure is itself a form of documentation.

## 17. Interview questions with model answers

**Q: What's the difference between a data structure and an algorithm?**

A data structure organizes data in memory to make specific operations efficient. An algorithm is a step-by-step procedure for solving a problem. They're deeply connected: the same algorithm can perform very differently depending on the data structure it operates on. Binary search is O(log n) on a sorted list but impossible on an unordered one.

**Q: Why would you choose a dictionary over a list for storing user records?**

If you need to look up a user by ID or username, a dictionary gives you O(1) average lookup regardless of how many users there are. A list requires O(n) to find a record that isn't at a known index. At small scales the difference is invisible; at enterprise scales with millions of users, it's the difference between instant and unacceptably slow.

**Q: What does "choosing the right data structure" actually mean in practice?**

It means identifying which operations need to be fast for your specific use case, then selecting the structure that provides those operations at the lowest cost. The right structure for a deduplication job (set) is different from the right structure for ordered task processing (queue), even if both are technically solvable with a list.

## 18. Knowledge check

1. What's the practical difference between O(n) and O(n²) when n is 1,000,000?
2. Name one situation where a set is dramatically faster than a list.
3. Why isn't "it produces the correct result" a sufficient evaluation of a solution?
4. What question should you ask before choosing a data structure for a problem?

## 19. Hands-on exercises

**Easy**

1. Write a function that checks whether a given name is in a list of 10 names, using a simple `in` check. Then rewrite it to convert the list to a set first and measure (or reason about) the performance difference.
2. Given a list of product ids, convert it to a set and demonstrate that duplicate ids disappear.
3. Write a short comment in code (not actual code) describing what data structure you'd use to store: (a) a list of today's tasks in order, (b) the set of countries a user has visited, (c) a mapping of product codes to prices.

**Medium**

4. Write a function that takes two lists of integers and returns those appearing in both, first using nested loops (O(n²)), then using a set (O(n)), and confirm both produce the same result.
5. Given a list of 10,000 numbers (use `range(10000)`), compare the time to check membership of the last element using `in` on a list versus a set. Use Python's `time` module to measure.
6. Write a short analysis, in comments, of what data structure you'd use for each of these operations in a real backend system: storing a user session, processing incoming API requests in order, tracking which email addresses have already received a newsletter.

**Hard**

7. Build a simple benchmark: create a list and a set both containing 100,000 strings, and time 10,000 membership checks on each. Print the ratio of list time to set time and explain the result.
8. Given a list of 50,000 transaction records (simulate with a list of dicts), write two functions that find all transactions over $500: one using a linear scan, one that first builds a filtered data structure. Analyze the complexity of each.

## 20. Stretch challenge

Find a piece of code you wrote in Module 1 or Module 2's capstone projects that uses `if item in some_list` inside a loop. Analyze its complexity, decide whether the list should have been a set or a dictionary for that use case, and rewrite it. Write a short paragraph explaining the change and what the performance impact would be at 100x the scale you originally tested at.

## 21. Summary

A data structure organizes data; an algorithm processes it. The choice of structure determines what operations are fast. At small scales, wrong choices are invisible; at enterprise scales, they're the difference between a system that works and one that doesn't. Every lesson in this module builds on this foundation: learning a new structure or algorithm is really learning when a specific set of operations becomes cheap, and when to pay for that with either memory or preprocessing time.

## 22. Additional resources

- [Python official docs: Data Structures](https://docs.python.org/3/tutorial/datastructures.html)
- [Wikipedia: Data structure](https://en.wikipedia.org/wiki/Data_structure)
- [Big-O Cheat Sheet](https://www.bigocheatsheet.com/)

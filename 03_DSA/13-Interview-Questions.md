Module 13: Technical Interview Preparation — Data Structures & Algorithms

## Introduction

Technical interviews for Enterprise Backend Developer roles at tier-one consulting firms (e.g., PwC, Deloitte, Accenture) and major tech companies test more than syntax. Interviewers evaluate memory usage, execution speed, algorithmic trade-offs, and edge-case handling. This guide contains high-frequency questions, model answers, common candidate mistakes, and interviewer evaluation criteria.

---

## Part 1: Core Data Structure Questions

### 1) Why choose a dictionary instead of a list?

**Model answer:**

I choose a dictionary when I need $O(1)$ average time complexity for lookups, insertions, and deletions by key. A list requires $O(N)$ to search for an element unless you already know its index. For example, repeatedly checking whether a user ID exists in a list of thousands is a performance bottleneck, while a dictionary (hash map) maps keys directly to values using a hash function, which scales much better for associative data.

**Common mistakes:**

- Failing to mention Big-O notation.
- Saying "dictionaries are faster" without explaining hashing or collision handling.

**Follow-up:** What happens if two keys hash to the same value?

**Answer:** This is a hash collision. Python resolves collisions using open addressing (probing) and other internal strategies to find the next available slot while maintaining correctness.

**Evaluation criteria:** Correct terminology (associative arrays / hash maps), clear complexity reasoning ($O(1)$ vs $O(N)$), and awareness of collisions and trade-offs.

---

### 2) When is a `set` more appropriate than a `list`?

**Model answer:**

A `set` is preferred when you need uniqueness guarantees and fast membership testing. Sets provide average-case $O(1)$ membership checks (hash-based), while lists take $O(N)$. Use sets for deduplication and membership-heavy operations.

**Common mistakes:**

- Using a list for membership checks on large collections.
- Forgetting that sets are unordered and unindexed (order is not preserved).

**Evaluation criteria:** Understands uniqueness, membership complexity, and ordering implications.

---

### 3) Spot the complexity issue (example)

Consider this naive deduplication function:

```python
def unique_logs(logs):
    unique_logs = []
    for log in logs:
        if log not in unique_logs:
            unique_logs.append(log)
    return unique_logs
```

**Candidate analysis (expected):**

The code is $O(N^2)$ because `log in unique_logs` is an $O(N)$ operation inside a loop. For small inputs this is fine, but it doesn't scale.

**Fixes:**

- If order does not matter: `return list(set(logs))` — $O(N)$ average-case using hashing.
- If order matters (preserve first occurrence): `list(dict.fromkeys(logs))` — preserves insertion order while using hashing for membership.

**Evaluation criteria:** Ability to spot hidden complexity (the `in` operator on lists) and propose an optimized, practical alternative.

---

## Interview tips & evaluation checklist

- Always state the complexity using Big-O.
- Mention both average and worst-case behaviors when relevant.
- Discuss space vs time trade-offs when proposing changes.
- Clarify constraints (e.g., preserve order, immutability, memory limits) before optimizing.

---

If you want, I can continue reformatting the remaining parts of this module (more questions, code examples, and model answers). Point me to any sections you'd like preserved verbatim.

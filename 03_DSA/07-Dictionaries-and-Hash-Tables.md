# Lesson 7: Dictionaries and Hash Tables

## 1. Learning objectives

By the end of this lesson you should be able to:

- Explain how a hash table works internally, including hashing, buckets, and collision handling
- Use every common dictionary method fluently and state its time complexity
- Write dictionary comprehensions for transformation and filtering tasks
- Recognize when a dictionary is the right data structure versus a list or set
- Use `collections.defaultdict` and `collections.Counter` for common dictionary patterns
- Design efficient lookup structures using dictionaries to replace O(n) list scans

## 2. Prerequisites

Lessons 1 through 3 of this module (Introduction, Complexity, Lists). Understanding why O(1) lookup matters requires the complexity foundation, and the dictionary's advantages over lists only make sense in contrast to list behavior.

## 3. Introduction

If you had to pick one data structure that makes Python so productive for real-world backend work, it would be the dictionary. O(1) average lookup regardless of size, flexible key-value structure that maps naturally to JSON and database results, and an implementation so well-optimized that it's literally the foundation of Python's own object system. Every object's attributes are stored in a dictionary. Every module's globals live in a dictionary. Understanding how dictionaries work, not just how to use them, is one of the most valuable things in this module.

## 4. Theory

A dictionary is a collection of **key-value pairs** where each key is unique. You look up a value by its key in O(1) average time, regardless of how many pairs the dictionary contains.

```python
user = {
    "name": "Alex",
    "role": "engineer",
    "active": True
}
print(user["name"])  # "Alex" — O(1) lookup
```

Under the hood, a dictionary is a **hash table**: a data structure that uses a **hash function** to convert a key into an index into an array of buckets, then stores the value at that index.

**How hashing works, step by step:**

1. You call `user["name"]`
2. Python calls `hash("name")` → produces an integer (e.g., `8226336974921648)
3. Python applies `hash_value % capacity` to get a bucket index (e.g., index 3 in an 8-bucket table)
4. Python looks at bucket 3, finds the key `"name"`, confirms it matches, returns the value

Because step 3 is arithmetic (not a loop), the lookup is O(1) regardless of dictionary size.

## 5. Why this concept exists

Lists give you O(1) access by position, but position is often not the natural way to identify data. "Give me the user at index 47234" is not how people think about data; "give me the user with id 47234" is. Dictionaries let you define your own indexing scheme using meaningful keys (names, IDs, codes), while still getting the O(1) lookup guarantee that makes indexed access to lists fast. They also naturally model the key-value structure that appears everywhere in real systems: HTTP headers, JSON payloads, database rows, configuration files.

## 6. Internal implementation

CPython's dictionary implementation has evolved significantly and is now one of the most optimized hash tables in any mainstream language. Key implementation details:

**Hash function:** `hash()` in Python produces a fixed-size integer from a hashable object. Strings, integers, tuples are all hashable; lists and dictionaries are not (because they can change, which would invalidate their hash).

**Buckets and load factor:** The dictionary allocates an internal array of buckets. Each bucket can hold one entry. The **load factor** (entries / capacity) determines when to resize: when the dictionary gets about 2/3 full, CPython resizes the internal array (roughly doubling it) and rehashes all existing entries into the new larger array.

**Collision handling:** Two different keys can produce the same bucket index (a **collision**). CPython uses **open addressing with probing**: when a collision occurs, it checks the next bucket (or uses a more sophisticated probe sequence) until it finds an empty one. This is why the load factor is kept low — too many collisions degrade O(1) average lookup to O(n) worst case.

**Insertion order:** Since Python 3.7, dictionaries maintain insertion order as a language guarantee. The implementation uses a compact representation that stores entries in insertion order separately from the hash index, combining order preservation with lookup performance.

```python
# Python 3.7+ — insertion order is guaranteed
d = {}
d["c"] = 3
d["a"] = 1
d["b"] = 2
print(list(d.keys()))  # ['c', 'a', 'b'] — insertion order preserved
```

## 7. Real-world analogy

A dictionary is the index at the back of a textbook. You don't read every page to find "polymorphism" — you look it up in the index, which gives you the page number directly. That's O(1): the index has thousands of entries, but finding any one takes the same time. The "hashing" is what the index does conceptually: it maps a term (key) to a location (value). A collision is when two terms happen to fall on the same index line — the index handles this by listing both, or using a longer entry.

A **collision** in real life: imagine you hash "apple" and "apricot" and both produce index 3. The hash table needs a strategy to store both without losing either. Python's strategy (probing) is like looking at the next shelf when your designated shelf is already occupied.

## 8. Enterprise use cases

**Configuration management:** Application config as a dictionary of settings keys to values, loaded from JSON or environment variables, is the standard pattern in every Python backend.

**Request/response mapping:** HTTP headers, query parameters, and JSON bodies are all naturally represented as dictionaries. Parsing and building them is a core backend operation.

**Caching:** An in-memory cache is a dictionary mapping cache keys to cached values, giving O(1) cache hit checks.

**Frequency counting:** Counting occurrences of events, errors, user actions — all naturally expressed as a dictionary of item to count.

**Grouping and aggregation:** Grouping records by a field (region, category, status) is a dictionary-building operation: `{key: [records with that key]}`.

**Index building:** For fast lookup in a dataset, build a dictionary from the lookup field to the record. This converts repeated O(n) list scans to O(1) dictionary lookups.

```python
# Before: O(n) scan every time
records = [{"id": 1, "name": "Alex"}, {"id": 2, "name": "Sam"}]
def find_by_id(records, target_id):
    for r in records:
        if r["id"] == target_id:
            return r

# After: build index once O(n), lookup O(1) thereafter
index = {r["id"]: r for r in records}
user = index[1]  # O(1)
```

## 9. Complexity analysis

| Operation | Average | Worst Case | Notes |
|---|---|---|---|
| `d[key]` lookup | O(1) | O(n) | Worst case on pathological collisions |
| `d[key] = val` insert | O(1) | O(n) | Amortized O(1) including resizes |
| `del d[key]` | O(1) | O(n) | |
| `key in d` | O(1) | O(n) | Much faster than `key in list` |
| `len(d)` | O(1) | O(1) | Stored on the object |
| `d.keys()` / `d.values()` / `d.items()` | O(1) | O(1) | Returns a view, not a copy |
| Iteration over d | O(n) | O(n) | Must visit all entries |
| `d.get(key, default)` | O(1) | O(n) | Same as lookup, never raises |

Worst case O(n) is theoretical under pathological hash collisions with adversarial keys. In practice with normal data, average O(1) is what you'll always see.

## 10. Step-by-step visual walkthrough

**Building a word frequency counter:**

Input: `"the cat sat on the mat the cat"`

```
Start: counts = {}

Word "the":
  "the" not in counts → counts["the"] = 1
  counts = {"the": 1}

Word "cat":
  "cat" not in counts → counts["cat"] = 1
  counts = {"the": 1, "cat": 1}

Word "sat":
  counts = {"the": 1, "cat": 1, "sat": 1}

Word "on":
  counts = {"the": 1, "cat": 1, "sat": 1, "on": 1}

Word "the":
  "the" in counts → counts["the"] += 1 → 2
  counts = {"the": 2, "cat": 1, "sat": 1, "on": 1}

Word "mat":
  counts = {"the": 2, "cat": 1, "sat": 1, "on": 1, "mat": 1}

Word "the":
  counts["the"] += 1 → 3

Word "cat":
  counts["cat"] += 1 → 2

Final: {"the": 3, "cat": 2, "sat": 1, "on": 1, "mat": 1}
```

**Hash collision visualization:**

```
Keys: "apple", "mango"
Capacity: 8 buckets (indices 0–7)

hash("apple") % 8 = 3  → store in bucket 3
hash("mango") % 8 = 3  → COLLISION! bucket 3 occupied

Open addressing: check bucket 4 → empty → store "mango" in bucket 4

Lookup "mango":
  hash("mango") % 8 = 3
  bucket 3 contains "apple" ≠ "mango"
  probe bucket 4 → contains "mango" ✓ → return value
```

This probing is still O(1) amortized for sparse tables, O(n) in the extreme case where every bucket is full.

## 11. Syntax

**Creation:**
```python
empty = {}
user = {"name": "Alex", "age": 30}
from_pairs = dict([("a", 1), ("b", 2)])
from_kwargs = dict(name="Alex", age=30)
from_keys = dict.fromkeys(["a", "b", "c"], 0)  # {"a": 0, "b": 0, "c": 0}
```

**Access and modification:**
```python
d = {"name": "Alex", "role": "engineer"}

# Access
print(d["name"])            # "Alex" — KeyError if missing
print(d.get("name"))        # "Alex" — None if missing
print(d.get("dept", "N/A")) # "N/A" — custom default if missing

# Modification
d["role"] = "senior engineer"    # update
d["department"] = "backend"       # insert
del d["department"]                # delete — KeyError if missing
popped = d.pop("role", "default") # delete and return — no error if missing

# Checking existence
print("name" in d)      # True — O(1)
print("dept" in d)      # False
```

**Iteration:**
```python
d = {"a": 1, "b": 2, "c": 3}

for key in d:                    # iterate keys
    print(key)

for key in d.keys():             # explicit key iteration
    print(key)

for value in d.values():         # iterate values
    print(value)

for key, value in d.items():     # iterate key-value pairs
    print(f"{key}: {value}")
```

**Merging:**
```python
base = {"a": 1, "b": 2}
updates = {"b": 99, "c": 3}

# Python 3.9+ — merge operator
merged = base | updates       # {"a": 1, "b": 99, "c": 3}

# All versions
merged = {**base, **updates}  # same result

# In-place update
base.update(updates)          # base is now {"a": 1, "b": 99, "c": 3}
```

**Dictionary comprehensions:**
```python
# Transform values
squared = {k: v**2 for k, v in {"a": 2, "b": 3}.items()}
# {"a": 4, "b": 9}

# Filter entries
active_users = {uid: u for uid, u in users.items() if u["active"]}

# Invert a dictionary (only safe if values are unique)
inverted = {v: k for k, v in original.items()}

# Build from two lists
codes = ["USD", "EUR", "GBP"]
rates = [1.0, 0.92, 0.79]
exchange = {code: rate for code, rate in zip(codes, rates)}
```

**`collections.defaultdict`:**
```python
from collections import defaultdict

# Groups words by first letter — no KeyError on first access
groups = defaultdict(list)
for word in ["apple", "ant", "banana", "avocado", "blueberry"]:
    groups[word[0]].append(word)

print(dict(groups))
# {'a': ['apple', 'ant', 'avocado'], 'b': ['banana', 'blueberry']}

# Count without explicit initialization
counts = defaultdict(int)
for word in ["cat", "bat", "cat", "hat"]:
    counts[word] += 1  # no KeyError — missing keys default to 0
```

**`collections.Counter`:**
```python
from collections import Counter

words = ["the", "cat", "sat", "on", "the", "mat", "the", "cat"]
counts = Counter(words)
print(counts)              # Counter({'the': 3, 'cat': 2, ...})
print(counts.most_common(2))  # [('the', 3), ('cat', 2)]
print(counts["the"])           # 3
print(counts["dog"])           # 0 — Counter returns 0 for missing keys

# Arithmetic
c1 = Counter(a=3, b=1)
c2 = Counter(a=1, b=2)
print(c1 + c2)  # Counter({'a': 4, 'b': 3})
print(c1 - c2)  # Counter({'a': 2})
```

## 12. Common mistakes

**Using `d[key]` when the key might not exist.** This raises `KeyError`. Use `d.get(key)` or `d.get(key, default)` for safe access.

```python
# Dangerous
count = d["word"]  # KeyError if "word" not in d

# Safe
count = d.get("word", 0)
```

**Modifying a dictionary while iterating over it.** This raises `RuntimeError`. Iterate over a copy of keys or build a new dictionary:

```python
# Wrong
for key in d:
    if some_condition(key):
        del d[key]  # RuntimeError

# Correct
for key in list(d.keys()):  # iterate over a static list of keys
    if some_condition(key):
        del d[key]
```

**Using a mutable object as a dictionary key.** Lists and dicts can't be keys because they're not hashable. Use tuples instead.

```python
d = {}
d[[1, 2]] = "value"    # TypeError: unhashable type: 'list'
d[(1, 2)] = "value"    # Works — tuple is hashable
```

**Assuming dictionary values are always present without checking.** Especially when processing external data (API responses, user input), always use `.get()` with a default or check `key in d` before accessing.

## 13. Debugging tips

`KeyError` means you're accessing a key that doesn't exist. Print `list(d.keys())` to see what's actually in the dictionary versus what you expected. For nested dictionaries, access failures can cascade; use `.get()` at each level to avoid chain `KeyError`s. If dictionary values seem to be shared across what should be independent entries (e.g., modifying one list value appears in another), check whether you used `dict.fromkeys(keys, [])` with a mutable default — all entries share the exact same list object.

```python
# The fromkeys mutable default trap
d = dict.fromkeys(["a", "b", "c"], [])
d["a"].append(1)
print(d)  # {"a": [1], "b": [1], "c": [1]} — all share the same list!

# Fix: use a defaultdict or comprehension
d = {k: [] for k in ["a", "b", "c"]}  # each key gets its own list
```

## 14. Best practices

Use `.get(key, default)` over `d[key]` whenever the key's presence isn't guaranteed. Use `defaultdict` for grouping and counting patterns to eliminate the "initialize if not exists" boilerplate. Use `Counter` for frequency counting rather than rolling your own. Build an index dictionary (field → record) when you'll be doing repeated lookups on a list of records — convert O(n) repeated scans to O(1) lookups at the cost of one O(n) upfront build.

## 15. Performance considerations

Dictionary operations are O(1) average, making them the right default for any lookup-by-key pattern. The main practical consideration is memory: a dictionary uses significantly more memory than a list of equivalent length, due to the hash table overhead. For very large datasets where every byte matters, this tradeoff is worth evaluating. For normal backend workloads at enterprise scale (millions rather than billions of records), dictionary memory usage is not a concern compared to the performance gains.

## 16. Code style

Use dict comprehensions for single-expression transformations; use explicit loops for anything requiring multiple statements per entry. Name dictionary variables for what they map: `user_by_id`, `count_by_category`, `score_by_player` communicates both the key type and value type immediately. Prefer `d.get(key)` consistently over `d[key]` in any code path where key presence isn't guaranteed.

## 17. Interview questions with model answers

**Q: How does a dictionary work internally?**

A dictionary is a hash table. When you set `d[key] = value`, Python computes `hash(key)`, maps it to a bucket index using modulo arithmetic, and stores the value there. When you look up `d[key]`, Python repeats the hash computation, finds the bucket, and returns the stored value. This is O(1) average because the hash computation is constant-time arithmetic. Collisions — when two keys hash to the same bucket — are handled by probing to adjacent buckets, which remains fast in a sparsely populated table.

**Q: Why can't you use a list as a dictionary key?**

Dictionary keys must be hashable, and hashability generally requires immutability. If a list were used as a key and then mutated, its hash value would change, but the dictionary would still look for it at the old hash location — it would be permanently lost in its own index. Python's type system enforces this by making mutable types (list, dict, set) non-hashable, and immutable types (int, str, tuple) hashable.

**Q: What's the difference between `d[key]` and `d.get(key)`?**

`d[key]` raises `KeyError` if the key doesn't exist. `d.get(key)` returns `None` (or a specified default) if the key doesn't exist. In code that processes external data where key presence can't be guaranteed — API responses, user input, database results — `.get()` is the safer default because it handles the missing case without an exception.

**Q: When would you choose a dictionary over a list?**

When you need to retrieve data by a meaningful identifier (name, id, code) rather than by position. A list gives O(1) access by index; a dictionary gives O(1) access by any hashable key. If you're scanning a list repeatedly looking for records that match a condition, building a dictionary index first converts repeated O(n) scans to O(1) lookups at the cost of one O(n) build, which pays off immediately if you do more than one lookup.

## 18. Knowledge check

1. What happens internally when Python looks up `d["key"]` in a dictionary?
2. Why does Python 3.7+ preserve insertion order in dictionaries?
3. What's the difference between `d["key"]` and `d.get("key", default)`?
4. Why is `dict.fromkeys(["a","b","c"], [])` dangerous?
5. When would you use `defaultdict` over a regular dictionary?

## 19. Hands-on exercises

**Easy**

1. Create a dictionary representing a product with `name`, `price`, and `in_stock` fields. Access each value and demonstrate `.get()` for a key that doesn't exist.
2. Write a function that counts the frequency of each character in a string, returning a dictionary.
3. Given a dictionary of `{name: score}`, use a dictionary comprehension to produce a new dictionary containing only entries where the score is above 70.

**Medium**

4. Write a function that groups a list of words by their length, returning `{length: [words]}`. Use `defaultdict(list)`.
5. Given a list of transaction dictionaries (`{"id", "amount", "category"}`), build an index by category that maps each category to a list of all its transactions, then calculate the total amount per category.
6. Write a function that inverts a dictionary (swaps keys and values), raising a `ValueError` if any values are duplicated (since duplicate values would make ambiguous keys).

**Hard**

7. Using only a dictionary, implement a simple **LRU (Least Recently Used) cache** with a maximum size. When a new item is inserted past the limit, the least recently accessed item should be evicted. (Hint: Python 3.7+ dict preserves insertion order; `OrderedDict` provides `move_to_end()`.)
8. Given a list of 100,000 employee records (simulate with generated dicts having `id`, `department`, `salary`), write two approaches to find all employees in a given department: (a) linear scan, (b) pre-built dictionary index. Compare their complexity and demonstrate the performance difference empirically using `time`.

## 20. Stretch challenge

Build a **two-level nested cache** (a cache of caches) that maps `(user_id, report_type)` compound keys to report data. Your `ReportCache` class should support `get(user_id, report_type)`, `set(user_id, report_type, data)`, and `invalidate_user(user_id)` (removes all cached reports for a given user). Implement it using a dictionary of dictionaries. Then implement the same interface using a flat dictionary keyed by `(user_id, report_type)` tuples, and explain in a comment which design is cleaner for the `invalidate_user` operation and why.

## 21. Summary

A dictionary is a hash table that provides O(1) average key-value lookup, making it Python's most powerful general-purpose data structure for any problem involving lookup by a meaningful key. Internally, it hashes keys to bucket indices, handles collisions through probing, and maintains insertion order since Python 3.7. Keys must be hashable (immutable). Use `.get()` for safe access, `defaultdict` for grouping patterns, `Counter` for frequency counting, and dictionary comprehensions for transformation. The single highest-impact performance improvement in many Python programs is replacing repeated `if x in list` checks with `if x in dict`, converting O(n) scans to O(1) lookups.

## 22. Additional resources

- [Python official docs: Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries)
- [Python official docs: collections.defaultdict](https://docs.python.org/3/library/collections.html#collections.defaultdict)
- [Python official docs: collections.Counter](https://docs.python.org/3/library/collections.html#collections.Counter)
- [Brandon Rhodes: The Dictionary Even Mightier (PyCon 2017)](https://www.youtube.com/watch?v=66P5FMkWoVU)

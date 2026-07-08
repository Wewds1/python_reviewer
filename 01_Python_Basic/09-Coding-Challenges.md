# Coding Challenges — Module 1

## How to use this file

Try every problem yourself before you look at the answer key. That's not a formality, it's the actual point. If you copy an approach without struggling with it first, you'll recognize it later but you won't be able to produce it under pressure, and pressure is exactly the condition you'll be in during a real interview or a real production incident.

Answers and detailed explanations live in a separate answer key so you're not tempted to peek mid-attempt. Work through a batch, check yourself, then move on.

---

## Beginner (20)

1. Write a function that returns the square of a number.
2. Write a function that checks whether a number is positive, negative, or zero.
3. Write a function that returns the larger of two numbers without using `max()`.
4. Print the numbers from 1 to 20, but print "buzz" instead of any multiple of 4.
5. Write a function that counts the vowels in a string.
6. Reverse a list without using `.reverse()` or slicing.
7. Write a function that returns the average of a list of numbers.
8. Check whether a string is a palindrome, ignoring case.
9. Write a function that converts a temperature from Celsius to Fahrenheit.
10. Given a list of numbers, return a new list with only the even ones.
11. Write a function that counts how many words are in a sentence.
12. Given a dictionary of item names to prices, print each item with its price formatted as currency.
13. Write a function that returns the factorial of a number using a loop, not recursion.
14. Given a list of names, return the longest one.
15. Write a function that removes all whitespace from a string.
16. Given two numbers, return their greatest common divisor using a loop.
17. Write a function that capitalizes the first letter of every word in a sentence.
18. Given a list of numbers, return how many of them are negative.
19. Write a simple calculator function that takes two numbers and an operator string (`"+"`, `"-"`, `"*"`, `"/"`) and returns the result.
20. Given a string, count how many times each character appears and return the result as a dictionary.

## Intermediate (20)

1. Given a list of dictionaries representing students (name and grade), return the name of the student with the highest grade.
2. Write a function that flattens a list of lists into a single list, without using any library.
3. Given a sentence, return the frequency of each word as a dictionary, ignoring punctuation and case.
4. Write a function that checks whether two strings are anagrams of each other.
5. Given a list of numbers, return the second largest value without sorting the whole list.
6. Write a function that groups a list of words by their first letter, returning a dictionary of lists.
7. Given a list of transactions (each a dict with `amount` and `type`, where type is `"credit"` or `"debit"`), return the final balance.
8. Write a function that removes duplicate entries from a list of dictionaries based on one key, keeping the first occurrence.
9. Implement a basic Caesar cipher that shifts each letter of a string by a given number of positions.
10. Given a list of tuples representing coordinates, return the one closest to the origin.
11. Write a function that merges two dictionaries, and when a key exists in both, keeps the value from the second one.
12. Given a paragraph of text, return the three most common words, excluding a provided list of stop words.
13. Write a function that validates whether a string is a properly formatted email address, using basic checks rather than a regular expression.
14. Given a list of numbers, return `True` if the list is sorted in ascending order, `False` otherwise.
15. Write a function that takes a list of file names and groups them by extension.
16. Given a nested dictionary representing a company's departments and employees, count the total number of employees.
17. Write a function that generates the first n numbers of the Fibonacci sequence using a loop.
18. Given two lists representing set A and set B, return their union, intersection, and difference without using Python's built-in set operators directly (use loops).
19. Write a function that takes a list of prices and a discount percentage, and returns the discounted prices rounded to two decimals.
20. Given a list of log entries as strings ("2026-01-04 ERROR disk full"), return a count of entries per severity level.

## Advanced (15)

1. Given a list of orders (each with a customer id and an amount), return a dictionary mapping each customer to their total spend, sorted by spend from highest to lowest.
2. Implement a basic LRU cache using a dictionary, where inserting past a fixed capacity evicts the least recently used item. No `functools.lru_cache`.
3. Given a large CSV file (simulate with a generated list of rows), process it in chunks rather than loading it all into memory, and produce a running total of one numeric column.
4. Write a function that validates a deeply nested JSON-like structure against a simple schema (a dictionary describing expected keys and types), returning a list of every validation error found rather than stopping at the first one.
5. Implement a simple state machine for an order's lifecycle (`pending`, `processing`, `shipped`, `delivered`, `cancelled`), where invalid transitions raise a custom exception.
6. Given a list of overlapping time intervals, merge them into the minimal set of non-overlapping intervals.
7. Write a function that detects a circular reference in a dictionary that references other dictionaries by key, without infinite looping.
8. Build a simple in-memory rate limiter, allowing at most n calls per rolling time window, using nothing but the standard library.
9. Given a list of dependencies between tasks (as pairs, task A depends on task B), return a valid execution order, or raise an exception if the dependencies contain a cycle.
10. Write a function that parses a simplified INI-style config string into a nested dictionary, handling sections and key-value pairs.
11. Implement a basic retry decorator (a function that wraps another function) that retries the wrapped function up to n times on a specific exception, with a delay between attempts.
12. Given a list of financial transactions with timestamps, write a function that detects any account with more than five transactions within any 60-second window, a simple fraud-pattern check.
13. Write a function that deep-merges two nested dictionaries, recursively combining values rather than overwriting entire sub-dictionaries.
14. Implement a basic tokenizer that splits an arithmetic expression string (like `"3 + 4 * 2"`) into a list of numbers and operators.
15. Given a list of employee records with a manager id field, build and return the full management hierarchy as a nested structure, starting from the top-level executive.

## Debugging exercises (10)

Each of these has a bug. Find it, explain why it happens, and fix it.

1. 
```python
def get_total(prices=[]):
    prices.append(0)
    return sum(prices)
```

2.
```python
count = 0
def increment():
    count += 1
    return count
```

3.
```python
def divide(a, b):
    return a / b

print(divide(10, "2"))
```

4.
```python
for i in range(5):
    if i == 3:
        continue
    print(i)
else:
    print("done")
```
(This one isn't actually broken. Explain what it prints and why the `else` still runs.)

5.
```python
data = {"name": "Alex"}
print(data["age"])
```

6.
```python
def process(items):
    for item in items:
        if item < 0:
            items.remove(item)
    return items

print(process([1, -2, 3, -4, 5]))
```

7.
```python
try:
    value = int("abc")
except:
    pass
print(value)
```

8.
```python
class ConfigError(Exception):
    pass

def load_config(path):
    if not path:
        raise ConfigError
    return {"loaded": True}

load_config("")
```
(This one runs, but the error message it produces to whoever hits it is useless. Fix that.)

9.
```python
a = (1, 2, 3)
a[0] = 99
```

10.
```python
def safe_get(d, key):
    if d[key]:
        return d[key]
    return None

print(safe_get({"count": 0}, "count"))
```

## Code reading exercises (10)

Read each snippet and explain, in your own words, exactly what it does before running it.

1.
```python
result = [x**2 for x in range(10) if x % 2 == 0]
```

2.
```python
names = ["ana", "Bo", "carl"]
print(sorted(names, key=str.lower))
```

3.
```python
a, *b, c = [1, 2, 3, 4, 5]
```

4.
```python
def outer():
    x = 10
    def inner():
        nonlocal x
        x += 5
    inner()
    return x
```

5.
```python
data = {"a": 1, "b": 2}
print({v: k for k, v in data.items()})
```

6.
```python
x = [1, 2, 3]
y = x.copy()
y.append(4)
print(x, y)
```

7.
```python
def make_multiplier(n):
    return lambda x: x * n

double = make_multiplier(2)
triple = make_multiplier(3)
print(double(5), triple(5))
```

8.
```python
values = [None, 1, 0, "", "hi", [], [1]]
print([v for v in values if v])
```

9.
```python
class Counter:
    total = 0
    def __init__(self):
        Counter.total += 1

a = Counter()
b = Counter()
print(Counter.total)
```

10.
```python
with open("data.txt", "w") as f:
    f.write("first line\n")
    raise ValueError("interrupted")
```
(Explain what state the file is left in after this runs, and why.)

## Output prediction exercises (10)

Predict the exact output before running each one.

1. `print(3 == 3.0)`
2. `print("5" * 3)`
3. `print([1, 2] + [3, 4])`
4. `print({1, 2, 3} & {2, 3, 4})`
5. `print(bool(""), bool(" "), bool(0), bool([]))`
6. `print(list(range(10, 0, -2)))`
7.
```python
def f(x, y=[]):
    y.append(x)
    return y

print(f(1))
print(f(2))
```
8.
```python
x = 5
def change():
    x = 10
change()
print(x)
```
9. `print("a" < "b", "10" < "9")`
10.
```python
try:
    print("try")
    raise ValueError
except ValueError:
    print("except")
finally:
    print("finally")
```

---

A separate answer key with full explanations for every problem above will walk through not just the correct solution, but why the wrong instincts are wrong, since that's usually the more useful thing to actually understand.

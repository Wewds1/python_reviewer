# Lesson 3: Control Flow

## 1. Learning objectives

By the end of this lesson you should be able to:

- Write conditional logic with if/elif/else and know when nesting is the right call versus a sign you should restructure
- Use Python 3.10's match-case for the situations where it actually beats a chain of elifs
- Write for loops and while loops confidently, and know which one fits which problem
- Use range(), enumerate(), and zip() instead of manually managing index variables
- Control loop execution with break, continue, and pass, and explain the (often skipped) for-else construct

## 2. Prerequisites

Lessons 1 and 2. You need variables and an understanding of at least booleans and lists before conditionals and loops mean anything.

## 3. Introduction

Every program that does more than print one fixed thing needs to make decisions and repeat work. That's what this lesson is. It's less conceptually deep than the last one, but it's where you'll spend the most actual keystrokes for the rest of your career. Getting the idioms right here (enumerate instead of a manual counter, for-else instead of a flag variable) is one of the fastest ways to make your code look like it was written by someone who's done this before.

## 4. Theory

Control flow is what lets a program branch and repeat instead of just executing top to bottom. Python gives you two loop constructs (for and while) and one conditional construct (if/elif/else, plus match-case as of 3.10), and almost every algorithm you'll write in this module is some combination of the two.

The thing worth understanding early: Python's `for` loop isn't really a counting loop underneath, the way it is in C. It's an iteration loop. `for x in something` works on anything iterable, a list, a string, a dictionary, a file, a generator, and it always means "give me the next item until there isn't one." Counting with `range()` is just one common case of that, not the whole idea.

## 5. Why this concept exists

Without branching and looping, every program would need one line of code per action, with no way to react to data or repeat work. That obviously doesn't scale past "hello world." What's specific to Python here is the emphasis on iterating over things directly rather than manually managing indices, which is why `for item in my_list` is the idiomatic pattern and `for i in range(len(my_list)): my_list[i]` is something you'll get flagged for in review.

## 6. How Python implements it internally

`if`/`elif`/`else` compiles down to conditional jump instructions in the bytecode, nothing exotic. The more interesting one is `for`. Under the hood, `for x in iterable` calls `iter(iterable)` once to get an iterator object, then repeatedly calls `next()` on it until it raises `StopIteration`, at which point the loop ends. This is the same protocol whether you're looping over a list, a string, or a custom object you built yourself, which is why writing your own iterable classes later (outside this module) slots directly into the `for` syntax you already know.

## 7. Real-world analogy

An `if` statement is a fork in a hiking trail: you check a condition (is the left path flooded?) and take exactly one branch. A `for` loop is working through a stack of forms on your desk, one at a time, until the stack is empty; you don't know or care how many forms there are, you just keep going until there aren't any left. A `while` loop is more like waiting at a train platform: you don't know how many minutes it'll take, you just keep checking "has the train arrived yet?" until the answer changes.

## 8. Enterprise use cases

Validation logic in almost any intake form or API endpoint is a chain of conditionals. Processing a batch of client records, rows in a spreadsheet, transactions in a ledger, is almost always a for loop. `while` loops show up in retry logic for flaky network calls: keep trying until it succeeds or you've hit a maximum number of attempts, which is one of the clearest real cases where you genuinely don't know the iteration count ahead of time.

## 9. Syntax

**Conditionals:**

```python
score = 82

if score >= 90:
    grade = "A"
elif score >= 80:
    grade = "B"
else:
    grade = "C"
```

**Match-case (Python 3.10+):**

```python
match status_code:
    case 200:
        message = "OK"
    case 404:
        message = "Not Found"
    case 500 | 502 | 503:
        message = "Server Error"
    case _:
        message = "Unknown status"
```

The `case _` at the end is the wildcard, equivalent to a final `else`. Match-case really earns its keep when you're matching against several discrete values or, further down the line, unpacking structured data, not as a blanket replacement for every if/elif chain.

**For loops:**

```python
for name in ["Alex", "Jordan", "Sam"]:
    print(name)

for i in range(5):        # 0, 1, 2, 3, 4
    print(i)

for index, name in enumerate(["Alex", "Jordan"]):
    print(index, name)    # 0 Alex / 1 Jordan

for name, score in zip(["Alex", "Jordan"], [90, 85]):
    print(name, score)    # pairs them up positionally
```

**While loops:**

```python
attempts = 0
while attempts < 3:
    attempts += 1
    print(f"attempt {attempts}")
```

**break, continue, pass:**

```python
for n in range(10):
    if n == 5:
        break        # exit the loop entirely
    if n % 2 == 0:
        continue     # skip to the next iteration
    print(n)

if some_condition:
    pass  # placeholder, does nothing, useful while stubbing out code
```

## 10. Step-by-step examples

**Easy — grading logic:**

```python
score = 74
if score >= 60:
    print("Pass")
else:
    print("Fail")
```

**Medium — enumerate instead of manual indexing:**

```python
tasks = ["design", "build", "test", "deploy"]

# what a beginner writes:
for i in range(len(tasks)):
    print(i, tasks[i])

# what you should write instead:
for i, task in enumerate(tasks):
    print(i, task)
```

Both give the same output. The second one is shorter, can't go out of bounds, and is what an interviewer expects to see.

**Hard — for-else, the construct almost nobody teaches:**

```python
def find_first_negative(numbers):
    for n in numbers:
        if n < 0:
            print(f"found: {n}")
            break
    else:
        print("no negative numbers found")

find_first_negative([4, 7, 2, 9])   # no negative numbers found
find_first_negative([4, -7, 2])     # found: -7
```

The `else` on a `for` loop runs only if the loop completed without hitting a `break`. It's a clean replacement for the "found = False; ... if found: ..." flag-variable pattern beginners tend to reach for, and knowing it exists is a small but real signal that you've read past the basics.

## 11. Common mistakes

**Using `==` where a chain of comparisons was intended:**

```python
if 0 < x < 10:  # this is valid and does what you'd expect
    print("in range")
```

Python allows chained comparisons like that natively, which surprises people coming from languages that don't.

**Off-by-one errors with range():**

```python
for i in range(1, 10):  # goes up to 9, not 10 — range's upper bound is exclusive
    print(i)
```

**Infinite while loops from forgetting to update the condition variable:**

```python
count = 0
while count < 5:
    print(count)
    # forgot count += 1 — this loop never ends
```

**Mutating a list while iterating over it,** which produces confusing skipped or repeated elements:

```python
items = [1, 2, 3, 4]
for item in items:
    if item % 2 == 0:
        items.remove(item)  # don't do this
```

Iterate over a copy instead (`for item in items[:]`) or build a new list with a comprehension.

## 12. Debugging tips

If a `while` loop hangs, the first thing to check is whether the condition variable is actually being updated inside the loop body. If a `for` loop is skipping elements unexpectedly, check whether you're modifying the collection you're iterating over. `print()` statements showing the loop variable on each iteration are still the fastest way to see what's actually happening, don't be too proud to use them.

## 13. Best practices

Prefer `for item in collection` over indexing by hand. Use `enumerate()` the moment you need both the index and the value. Use `zip()` instead of indexing two lists in parallel. Keep nesting shallow, more than two or three levels of nested `if` inside a loop is usually a sign the logic wants to be pulled out into a function. Reach for `while` only when you genuinely don't know the number of iterations ahead of time; if you do know it, a `for` loop says that more clearly.

## 14. Performance considerations

`for` loops in Python have real per-iteration overhead compared to compiled languages, since each step goes through the interpreter. For anything performance-critical over large data, list comprehensions (covered briefly here, more in the strings and lists exercises) and vectorized libraries like NumPy will outperform a manual Python loop by a wide margin. For the scale of problems in this module, plain loops are completely fine, this is a "know it exists" note, not a "rewrite everything" instruction.

## 15. Code style (PEP 8)

Four spaces per indentation level, never tabs. A single space around comparison and logical operators (`if x == 5`, not `if x==5`). Avoid deeply nested conditionals; an early `return` or `continue` to handle an edge case up front usually reads better than wrapping the entire rest of the function in an `if`.

## 16. Interview questions with model answers

**Q: What's the difference between `break` and `continue`?**

`break` exits the loop entirely, immediately. `continue` skips only the rest of the current iteration and moves on to the next one. Mixing them up is a common beginner slip, so being able to state the difference cleanly, in one sentence each, is worth practicing out loud.

**Q: When would you use `while` instead of `for`?**

When you don't know the number of iterations ahead of time; classic examples are retrying a network call until it succeeds, or reading input until a user types "quit." If you already know how many times you're looping, `for` is the clearer, more idiomatic choice.

**Q: What does the `else` clause on a `for` loop do?**

It runs if the loop finished without hitting a `break`. Most candidates have never seen this, so being able to explain it correctly, ideally with the "searching for something, else means not found" framing, stands out.

## 17. Knowledge check

1. What does `range(2, 10, 2)` produce?
2. What's the output of a `for` loop with an `else` clause if a `break` fires partway through?
3. Why is `for item in my_list: my_list.remove(item)` risky?
4. Rewrite this using `enumerate()`: `for i in range(len(colors)): print(i, colors[i])`

## 18. Hands-on exercises

**Easy**

1. Write an if/elif/else chain that prints "cold," "mild," or "hot" based on a temperature variable.
2. Loop over a list of five numbers and print only the even ones.
3. Use a while loop to print the numbers 1 through 5.

**Medium**

4. Given a list of names, use `enumerate()` to print each name with its position, starting the count at 1 instead of 0.
5. Given two lists, one of product names and one of prices, use `zip()` to print them as pairs.
6. Use a for-else construct to check whether a target value exists in a list, printing "found" or "not found" accordingly, without using a separate flag variable.

**Hard**

7. Write a retry-loop simulation: attempt an operation (represented by a function that fails the first two times and succeeds the third), retrying up to 5 times with a `while` loop, and stopping early once it succeeds.
8. Given a list of transaction amounts, use `match`-`case` to categorize each one as `"refund"` (negative), `"small"` (0 to 100), `"large"` (over 100), and print the category for each transaction.

## 19. Stretch challenge

Write a function that takes a list of integers and returns the first pair of numbers that sum to a target value, using nested loops. Then rewrite it so the inner search stops early with a `break` the moment a match is found, instead of continuing to check pairs that no longer matter. Time both versions on a list of a few thousand numbers and see if you can measure the difference.

## 20. Summary

Conditionals branch, loops repeat, and Python's `for` loop is fundamentally about iterating over things, not counting up to a number, even though `range()` makes it look that way at first. `enumerate()` and `zip()` exist specifically so you never have to manage index variables by hand, and using them instead of manual indexing is one of the clearest tells that separates someone new to Python from someone comfortable in it. The for-else construct is niche but worth knowing; it'll come up in at least one interview eventually.

## 21. Additional resources

- [Python official docs: More Control Flow Tools](https://docs.python.org/3/tutorial/controlflow.html)
- [PEP 634 — Structural Pattern Matching](https://peps.python.org/pep-0634/), for the full match-case spec
- [Python official docs: Iterators](https://docs.python.org/3/tutorial/classes.html#iterators), for how `for` actually works underneath

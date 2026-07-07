# Lesson 7: Exception Handling

## 1. Learning objectives

By the end of this lesson you should be able to:

- Use try/except/else/finally correctly, and explain what each part actually guarantees
- Catch specific exceptions instead of blanket-catching everything
- Raise exceptions deliberately, with useful messages
- Write your own custom exception classes
- Recognize the exception-handling habits that get flagged in a real code review

## 2. Prerequisites

Lessons 1 through 6, particularly File Handling, since a lot of the motivating examples here involve things that can go wrong with files, input, and external data.

## 3. Introduction

Things go wrong. Files don't exist, users type letters where you expected numbers, a network call times out. Exception handling is how a program responds to that without simply crashing and taking down whatever else it was doing. Done well, it's the difference between a script that fails loudly and clearly on bad input and one that either crashes with a wall of confusing traceback, or worse, silently produces wrong output and nobody notices until later.

## 4. Theory

An exception is an object Python raises when something goes wrong during execution. If nothing catches it, the program halts and prints a traceback. `try`/`except` lets you catch specific exceptions and decide what to do instead of letting the program die.

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Can't divide by zero")
```

The `except` clause here is specific: it only catches `ZeroDivisionError`. Any other kind of error happening inside the `try` block would still propagate up uncaught. That specificity is deliberate and matters a lot, which is covered in Common Mistakes below.

## 5. Why this concept exists

Without exception handling, any unexpected condition, a missing file, bad user input, a network hiccup, would crash the entire program on the spot, with no chance to recover, log the problem, or fail gracefully. Exceptions give you a structured way to separate "the code that does the work" from "the code that handles things going wrong," instead of littering every function with manual error-code checks the way older languages like C require.

## 6. How Python implements it internally

When an exception is raised, Python creates an exception object and starts unwinding the call stack, checking each enclosing `try` block for a matching `except` clause. If it finds one, execution jumps there. If it reaches the top of the program without finding a match, Python prints the traceback and exits. Exception classes form a hierarchy (`ZeroDivisionError` and `TypeError` both inherit from `Exception`, for instance), and an `except` clause catches its named exception and any subclass of it, which is exactly why `except Exception:` catches almost everything, and exactly why that's usually a bad idea.

## 7. Real-world analogy

Think of a `try` block as walking into a room you're not entirely sure is safe, and `except` clauses as a set of specific contingency plans posted by the door: one plan for a fire, a different plan for a flood, and no generic "something bad happened, do something" plan taped up that covers everything indiscriminately. A good contingency plan is specific because a fire and a flood need genuinely different responses; treating them the same way is how people get hurt or belongings get ruined by using the wrong response. `finally` is the exit checklist you run through no matter which door you leave by, whether you left because everything went fine or because you were evacuating.

## 8. Enterprise use cases

Validating client-submitted data (an uploaded spreadsheet with the wrong column headers, a form field left blank when it shouldn't be) relies entirely on catching specific, expected failure modes and responding usefully, not crashing the whole batch job over one bad row. API calls to external services fail sometimes, timeouts, rate limits, temporary outages, and production code needs to catch those specific failures and retry or fail gracefully rather than taking down the whole application. Custom exceptions (`InsufficientFundsError`, `InvalidClientRecordError`) make error handling in business logic self-documenting: catching `InsufficientFundsError` tells the next reader exactly what condition is being handled, which a generic `ValueError` doesn't.

## 9. Syntax

**Full try/except/else/finally:**

```python
try:
    value = int(user_input)
except ValueError:
    print("That's not a valid number.")
else:
    print(f"Got a valid number: {value}")  # runs only if no exception occurred
finally:
    print("Done processing input.")  # always runs, exception or not
```

`else` runs only when the `try` block succeeded with no exception, and it exists specifically so you can separate "the code that might fail" from "the code that should only run once we know it didn't." `finally` always runs, success, failure, or even if you `return` out of the middle of the `try` block, which makes it the right place for cleanup that absolutely must happen.

**Catching multiple exception types:**

```python
try:
    data = process(raw_input)
except (ValueError, TypeError) as e:
    print(f"Bad input: {e}")
except KeyError as e:
    print(f"Missing expected field: {e}")
```

**Raising exceptions deliberately:**

```python
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError("Insufficient funds for withdrawal")
    return balance - amount
```

**Custom exception classes:**

```python
class InsufficientFundsError(Exception):
    """Raised when a withdrawal exceeds the available balance."""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Cannot withdraw {amount}, balance is only {balance}")

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(balance, amount)
    return balance - amount

try:
    withdraw(100, 250)
except InsufficientFundsError as e:
    print(e)
    print(e.balance, e.amount)  # custom exceptions can carry extra data
```

## 10. Step-by-step examples

**Easy — catching a single, specific exception:**

```python
try:
    age = int(input("Enter your age: "))
except ValueError:
    print("Please enter a valid whole number.")
```

**Medium — else and finally used properly, in a file-handling context:**

```python
try:
    f = open("data.txt", "r")
except FileNotFoundError:
    print("File not found.")
else:
    content = f.read()
    print(content)
    f.close()
finally:
    print("Attempted file read.")
```

**Hard — a custom exception hierarchy used to distinguish related but different failure modes:**

```python
class ValidationError(Exception):
    """Base class for all validation failures."""

class MissingFieldError(ValidationError):
    def __init__(self, field):
        self.field = field
        super().__init__(f"Missing required field: {field}")

class InvalidFormatError(ValidationError):
    def __init__(self, field, value):
        self.field = field
        self.value = value
        super().__init__(f"Invalid format for {field}: {value!r}")

def validate_record(record):
    if "email" not in record:
        raise MissingFieldError("email")
    if "@" not in record["email"]:
        raise InvalidFormatError("email", record["email"])

try:
    validate_record({"email": "not-an-email"})
except MissingFieldError as e:
    print(f"Missing data: {e}")
except InvalidFormatError as e:
    print(f"Bad data: {e}")
except ValidationError as e:
    print(f"Validation failed: {e}")  # catches any other ValidationError subclass
```

Because `MissingFieldError` and `InvalidFormatError` both inherit from `ValidationError`, code that only cares about "was there a validation problem, generically" can catch `ValidationError` alone, while code that needs to react differently to each specific case can catch them individually, and Python checks `except` clauses top to bottom, using the first one that matches.

## 11. Common mistakes

**Bare `except:` clauses,** which catch literally everything, including things you almost certainly didn't mean to catch, like `KeyboardInterrupt` (someone hitting Ctrl+C) or genuine bugs that should have crashed loudly so you'd notice them:

```python
try:
    risky_operation()
except:  # catches everything, hides real bugs
    pass
```

This is one of the fastest ways to make a bug nearly impossible to track down later, because the program just silently swallows the error and keeps going as if nothing happened.

**Catching `Exception` broadly "just to be safe,"** which has almost the same problem as a bare `except:`, just slightly narrower. If you don't know exactly what can go wrong, that's a sign to go find out, not a reason to catch everything indiscriminately.

**Using exceptions for ordinary control flow** when a simple `if` check would do:

```python
try:
    value = my_dict["key"]
except KeyError:
    value = "default"
```

This works, but `my_dict.get("key", "default")` says the same thing more directly and doesn't rely on triggering and catching an actual exception for something that isn't really exceptional.

**Swallowing exceptions silently** with `except SomeError: pass`, which makes failures invisible instead of handled. At minimum, log what happened.

## 12. Debugging tips

Read the traceback from the bottom up; the last line tells you the exception type and message, and the line right above it tells you exactly where it happened. Resist the urge to wrap code in a broad `try/except` just to make an error message go away without understanding it first, that almost always just relocates the bug somewhere harder to find. If you're not sure which exception a piece of code can raise, check the documentation, or temporarily catch `Exception` while debugging, print the type and message, and then narrow it down to the specific exception once you know what you're actually dealing with.

## 13. Best practices

Catch the most specific exception type that applies, never a bare `except:`. Use `else` to separate code that should only run after a successful `try` block from the risky code itself. Use `finally` for cleanup that has to happen regardless of outcome, closing a connection, releasing a lock. Write custom exceptions when a failure mode is meaningful to your specific business logic; it makes both the raising code and the catching code more self-explanatory. Include a useful message when you raise an exception; `raise ValueError("age cannot be negative")` is worth far more to whoever reads it later than `raise ValueError()`.

## 14. Performance considerations

Exceptions in Python are relatively cheap to raise and catch compared to some other languages, but they're not free, and using them for routine control flow in a hot loop (checking membership via `try/except KeyError` on every iteration of a large loop, for instance) can be noticeably slower than an equivalent `if` check or `.get()` call. This is a minor concern for most scripts, but worth knowing before reaching for exceptions as a default way to handle expected, common conditions.

## 15. Code style (PEP 8)

Keep the code inside a `try` block as short as possible, ideally just the one operation that can actually fail, so it's obvious exactly what the `except` clause is responding to. Name custom exception classes ending in `Error` (`InsufficientFundsError`, not `InsufficientFunds`). Avoid bare `except:`; if you truly need to catch everything (rare, usually at a top-level entry point logging unexpected crashes), catch `Exception` explicitly and say why in a comment.

## 16. Interview questions with model answers

**Q: What's the difference between `except Exception:` and a bare `except:`?**

`except Exception:` catches essentially all normal runtime errors but deliberately excludes a small set of low-level exceptions like `SystemExit` and `KeyboardInterrupt`, which inherit from `BaseException` rather than `Exception`. A bare `except:` catches literally everything, including those, which means it can swallow a user's Ctrl+C or a legitimate program exit signal. The specific `except Exception:` version is the lesser evil of the two, but neither should be reached for casually.

**Q: When would you write a custom exception class instead of using a built-in one?**

When the failure represents a specific condition in your business logic that built-in exceptions don't capture clearly, insufficient funds, an invalid client record, a failed validation rule. A custom exception makes both the code that raises it and the code that catches it more self-documenting than a generic `ValueError`, and it lets calling code catch that specific condition without accidentally also catching unrelated `ValueError`s from somewhere else.

**Q: What does the `else` clause on a try/except do, and why not just put that code inside the `try` block?**

`else` runs only if the `try` block completed without raising an exception. Putting code there instead of inside the `try` block makes it explicit which lines are actually expected to potentially fail, versus which lines are just what happens next once you know they didn't. It's a readability and correctness tool: if you put too much in the `try` block, you risk accidentally catching an exception from a line that wasn't the one you meant to guard against.

## 17. Knowledge check

1. Why is a bare `except:` considered bad practice?
2. What's the difference between `except` and `else` in a try/except block?
3. When does `finally` run?
4. Why would you create a custom exception class instead of always raising `ValueError`?

## 18. Hands-on exercises

**Easy**

1. Write a script that asks for a number and catches `ValueError` if the input isn't a valid integer.
2. Write a try/except/finally block around a file read that prints "cleanup complete" in the `finally` clause no matter what happens.
3. Deliberately trigger a `ZeroDivisionError` and catch it with a helpful message.

**Medium**

4. Write a function `safe_divide(a, b)` that catches `ZeroDivisionError` and returns `None` instead of crashing, and demonstrate it with both a valid and an invalid call.
5. Write a custom exception `NegativeAmountError` and a function `deposit(amount)` that raises it if `amount` is negative.
6. Write a try/except that catches `FileNotFoundError` and `PermissionError` separately, with a distinct message for each.

**Hard**

7. Build a small `ValidationError` hierarchy (a base class and at least two subclasses) for validating a user record with `name`, `email`, and `age` fields, and write a `validate(record)` function that raises the appropriate specific exception for each kind of problem.
8. Write a function that attempts an operation up to three times, catching a specific exception on each failed attempt and retrying, only letting the exception propagate if all three attempts fail.

## 19. Stretch challenge

Take the CSV-processing exercise from Lesson 6 and add proper exception handling to it: catch a missing file gracefully, catch and report (without crashing) any individual row that fails to parse correctly, and use a custom exception to represent a row that fails business-rule validation (say, a negative price) separately from a row that's just malformed. By the end, the script should be able to process a CSV with a few genuinely bad rows in it and produce a clean report of what succeeded and what didn't, instead of crashing on the first problem it hits.

## 20. Summary

Exception handling exists so a program can respond to things going wrong instead of simply dying, but "handling" an exception well means catching the specific thing you expected and actually doing something useful about it, not silencing every possible error indiscriminately. `try` isolates risky code, `except` responds to specific known failure modes, `else` runs only on success, and `finally` always runs for cleanup. Custom exceptions turn vague failures into self-documenting, specific ones, which is exactly the kind of detail a code reviewer notices and appreciates.

## 21. Additional resources

- [Python official docs: Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
- [Python official docs: Built-in Exceptions](https://docs.python.org/3/library/exceptions.html), for the full exception hierarchy
- [PEP 3134 — Exception Chaining and Embedded Tracebacks](https://peps.python.org/pep-3134/), for anyone curious about `raise ... from ...`

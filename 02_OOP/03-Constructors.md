# Lesson 3: Constructors

## 1. Learning objectives

By the end of this lesson you should be able to:

- Explain exactly what `__init__` does and when it runs
- Use default parameter values in a constructor safely
- Handle the lack of true constructor overloading in Python using idiomatic alternatives
- Validate incoming data at construction time instead of letting bad state slip into an object
- Follow initialization best practices that keep constructors predictable and testable

## 2. Prerequisites

Lessons 1 and 2. You've already used `__init__` informally; this lesson goes deep on it specifically.

## 3. Introduction

`__init__` is the first method most people learn and the one they understand least precisely. It's not technically "the constructor" in the strict sense used by languages like Java (that's actually `__new__`, which you'll rarely touch), but for everyday Python work, treating `__init__` as "the thing that sets up a new object" is accurate enough and is how the term gets used throughout this module. This lesson covers what it can do beyond the basics: defaults, validation, and the patterns Python uses instead of the constructor overloading you might expect from other languages.

## 4. Theory

`__init__` runs automatically, once, immediately after a new object is created, and its job is to establish that object's starting state.

```python
class Employee:
    def __init__(self, name, salary, department="Unassigned"):
        self.name = name
        self.salary = salary
        self.department = department
```

`department` has a default value here, so it's optional at construction time:

```python
alice = Employee("Alice", 65000)
bob = Employee("Bob", 58000, "Engineering")
```

`__init__` never explicitly returns anything (returning a non-`None` value from it is actually an error in Python), because its purpose isn't to produce a result, it's to configure the object that already exists.

## 5. Why this concept exists

Without a guaranteed initialization step, objects could be created in an incomplete or inconsistent state, some code remembering to set every required field, other code forgetting one and leaving an object with missing or garbage data. `__init__` gives every object a single, mandatory point of entry where required data has to be provided and validated before the object is usable, which is exactly the guarantee that makes objects trustworthy to work with elsewhere in a codebase.

## 6. Internal behavior

When you call `Employee("Alice", 65000)`, Python first calls `__new__` to allocate the raw object (an implementation detail this module won't dwell on), then immediately calls `__init__` on that freshly allocated object, passing along whatever arguments you provided after `self`. If `__init__` raises an exception partway through, for instance during a validation check, the object still technically exists in memory at that point but the calling code never receives a usable reference to it, since the exception propagates up out of the constructor call entirely. This is why validation inside `__init__` is such an effective guard: a bad `Employee(...)` call never successfully produces an `Employee` you could accidentally use.

## 7. Real-world analogy

Think of `__init__` as the intake form at a doctor's office, not the appointment itself. Before you're seen, certain fields are mandatory, name, date of birth, and some are optional with sensible defaults, "preferred contact method" defaulting to email if you don't specify. If you leave a mandatory field blank, the front desk doesn't file an incomplete form and hope for the best, they stop you right there and ask you to fix it before anything proceeds. That's exactly what validation inside `__init__` does for an object.

## 8. Enterprise use cases

Constructors are where a huge amount of practical data validation lives in real systems: an `Order` constructor rejecting a negative quantity, a `User` constructor rejecting a malformed email, before either object is ever handed off to the rest of the application. Getting this validation right at construction time means the rest of the codebase can simply trust that any `Order` or `User` object it receives is already valid, rather than every downstream function needing to re-check the same things defensively.

## 9. UML-style explanation

```
┌─────────────────────────────────┐
│              Employee              │
├─────────────────────────────────┤
│ - name: str                        │
│ - salary: float                     │
│ - department: str                   │
├─────────────────────────────────┤
│ + __init__(name, salary,             │
│    department="Unassigned")          │
└─────────────────────────────────┘
```

UML diagrams typically show the constructor as a regular method in the operations section, sometimes marked distinctly, since it's the one method every object is guaranteed to have called before anything else happens to it.

## 10. Syntax

**Default arguments in a constructor:**

```python
class Task:
    def __init__(self, title, priority="medium", completed=False):
        self.title = title
        self.priority = priority
        self.completed = completed
```

**Validating input inside `__init__`:**

```python
class Product:
    def __init__(self, name, price):
        if price < 0:
            raise ValueError("Price cannot be negative")
        self.name = name
        self.price = price
```

**Python doesn't support true constructor overloading** (defining `__init__` twice with different signatures, the way Java or C# would), because a later `def __init__` in the same class simply replaces the earlier one. The idiomatic alternatives:

```python
# Option 1: default arguments covering multiple "shapes" of construction
class Rectangle:
    def __init__(self, width, height=None):
        self.width = width
        self.height = height if height is not None else width  # defaults to a square

# Option 2: classmethods as alternate, named constructors
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @classmethod
    def square(cls, side):
        return cls(side, side)

r1 = Rectangle(4, 9)
r2 = Rectangle.square(5)  # reads clearly as an alternate way to build one
```

That second pattern, a `@classmethod` used as an alternate constructor, is genuinely idiomatic Python and shows up constantly in real codebases (`datetime.fromtimestamp()` in the standard library is built the same way). Lesson 5 covers `@classmethod` in full; this is a preview of one of its most common uses.

## 11. Step-by-step examples

**Easy — a constructor with a default value:**

```python
class Coffee:
    def __init__(self, size="medium"):
        self.size = size

c1 = Coffee()
c2 = Coffee("large")
print(c1.size, c2.size)
```

**Medium — validation that prevents an invalid object from ever existing:**

```python
class Age:
    def __init__(self, years):
        if years < 0:
            raise ValueError("Age cannot be negative")
        self.years = years

try:
    bad = Age(-5)
except ValueError as e:
    print(f"Rejected: {e}")
```

**Hard — an alternate constructor pattern using `@classmethod`:**

```python
class Event:
    def __init__(self, name, start_hour, end_hour):
        self.name = name
        self.start_hour = start_hour
        self.end_hour = end_hour

    @classmethod
    def all_day(cls, name):
        return cls(name, 0, 24)

    def duration(self):
        return self.end_hour - self.start_hour

meeting = Event("Standup", 9, 9.5)
conference = Event.all_day("Company Offsite")

print(meeting.duration(), conference.duration())
```

`Event.all_day(...)` reads clearly at the call site: this is specifically an all-day event, without the caller needing to know or guess the right start and end hours to pass manually.

## 12. Common mistakes

**Doing expensive or risky work inside `__init__`** that has nothing to do with initializing the object's own state, opening a network connection, reading a large file. This makes objects slow and awkward to create, and hard to test in isolation, since creating a test object now has side effects you didn't ask for.

**Skipping validation and trusting the caller.** If a constructor accepts a `price` and never checks it, a negative price can end up baked into an object and silently propagate through the rest of the system before anyone notices.

**Trying to overload `__init__` by defining it twice,** not realizing the second definition simply replaces the first:

```python
class Broken:
    def __init__(self, x):
        self.x = x

    def __init__(self, x, y):  # this silently replaces the one above
        self.x = x
        self.y = y
```

## 13. Debugging tips

If an object seems to be missing an attribute you expected it to have, check whether `__init__` actually ran to completion, an exception raised partway through construction means later attribute assignments never happened. If validation isn't catching bad data, confirm the check is actually inside `__init__` and not, say, in a separate method that isn't guaranteed to be called.

## 14. Best practices

Validate everything you can at construction time; catching bad data as early as possible keeps the rest of the codebase simpler, since it can trust the objects it receives. Keep `__init__` focused purely on establishing state, no I/O, no heavy computation. Use `@classmethod` alternate constructors when a class genuinely needs to be built in more than one meaningful way, rather than piling on optional parameters that only make sense in certain combinations.

## 15. Performance considerations

Validation logic inside `__init__` runs on every single object creation, so keep it proportionate: simple range and type checks are fine, but anything that hits a database or makes a network call to validate a field will make object creation noticeably slow and should generally happen elsewhere, before the constructor is even called.

## 16. Code style

Keep required parameters first in the constructor signature, followed by parameters with defaults, matching standard Python function conventions. Raise clear, specific exceptions (with a useful message) on invalid input rather than silently clamping or ignoring bad values. Keep `__init__` bodies short; if it's doing more than assigning attributes and running a few validation checks, consider whether some of that logic belongs in a separate method instead.

## 17. Interview questions with model answers

**Q: Is `__init__` really the constructor?**

Strictly, no. `__new__` is the method responsible for actually creating the object; `__init__` runs afterward to initialize it. In everyday Python usage, though, `__init__` does the job people mean by "constructor," and interviewers are generally satisfied with an answer that shows you know the distinction exists, without needing a deep dive into `__new__`, which is rarely overridden in typical application code.

**Q: How would you support multiple ways of constructing an object in Python, given there's no real constructor overloading?**

The two idiomatic approaches are default parameter values, when the variations are simple, and `@classmethod` alternate constructors, when the variations represent genuinely different, meaningfully named ways of building the object. A concrete example, like `Rectangle.square(side)` alongside the standard `Rectangle(width, height)`, makes the answer land better than describing it abstractly.

**Q: Why validate input inside `__init__` rather than somewhere else?**

Because it guarantees that if an object exists at all, it's already in a valid state, no code anywhere else in the system has to re-check that a `Product`'s price isn't negative, because a `Product` with a negative price could never have been successfully constructed in the first place. That guarantee is what lets the rest of the codebase trust objects it's handed.

## 18. Knowledge check

1. What actually happens if you don't define `__init__` at all in a class?
2. Why can't you define `__init__` twice in the same class to support different argument combinations?
3. What's the benefit of a `@classmethod` alternate constructor over a pile of optional parameters?
4. Why is doing a network call inside `__init__` generally considered bad practice?

## 19. Hands-on exercises

**Easy**

1. Write a `Movie` class with `title`, `year`, and a default `rating` of `"unrated"`.
2. Write a constructor for a `Temperature` class that raises a `ValueError` if a value below absolute zero (-273.15°C) is provided.
3. Create two objects from the same class, one using only required arguments and one supplying every optional argument, and print both.

**Medium**

4. Write a `Circle` class with a `radius`, validating that it's positive, and add a `@classmethod` `from_diameter(cls, diameter)` that constructs a `Circle` from a diameter value instead.
5. Write a `User` class that validates an email contains an `"@"` symbol at construction time, raising a clear exception if it doesn't, and demonstrate both a successful and a failed construction.
6. Write a `Meeting` class with a `@classmethod` `recurring(cls, name, times_per_week)` alternate constructor, separate from the standard one-time meeting constructor.

**Hard**

7. Write a `BankAccount` class whose constructor validates that the opening balance isn't negative, and add a `@classmethod` `open_with_bonus(cls, name)` that constructs an account with a fixed starting bonus balance, demonstrating the alternate-constructor pattern with real validation behind both paths.
8. Design a `Shape` base setup (just the constructor logic for now, not full inheritance, which comes in Lesson 7) where a `Rectangle` class validates both width and height are positive, and includes a `@classmethod` `square(cls, side)`, and write test code that demonstrates both valid and invalid construction attempts for each path.

## 20. Stretch challenge

Design a `Flight` class where a regular constructor requires an origin, destination, and departure time, and add two separate `@classmethod` alternate constructors: `layover_flight(cls, origin, destination, departure_time, layover_city)` and `direct_flight(cls, origin, destination, departure_time)`, where the direct version simply omits the layover concept entirely rather than setting it to some placeholder value. Think carefully about what attribute (if any) should represent "no layover" for a direct flight, and be ready to justify that choice; this is exactly the kind of small design decision that turns into a permanent, awkward compromise if it's made carelessly early on.

## 21. Summary

`__init__` is where an object's initial state gets established, and it's the natural place to validate incoming data before an object is ever considered "real" and usable elsewhere in a system. Python doesn't support true constructor overloading, but default arguments and `@classmethod` alternate constructors cover the same ground idiomatically, and the alternate-constructor pattern in particular is worth recognizing, since it shows up constantly in the standard library and in real production code.

## 22. Additional resources

- [Python official docs: `__init__` and object initialization](https://docs.python.org/3/reference/datamodel.html#object.__init__)
- [Python official docs: classmethod](https://docs.python.org/3/library/functions.html#classmethod)
- [Real Python: Alternative Python Constructors](https://realpython.com/python-multiple-constructors/)

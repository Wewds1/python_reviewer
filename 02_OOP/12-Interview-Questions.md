# Interview Preparation Guide — Module 2

## How to use this file

Module 1's interview guide mixed topics the way a real interview does. This one goes further: OOP interviews, especially for a backend or consulting role, spend real time on design judgment, not just definitions. Expect to be asked to design something on the spot, defend a choice, or find the flaw in a class someone else wrote. Practice explaining your reasoning out loud, not just arriving at the right answer silently.

---

## Conceptual questions

**[Easy | Classes] What's the difference between a class and an object?**

A class is the blueprint, defining what attributes and behavior every instance will have. An object is one specific instance built from that blueprint, with its own independent data. The follow-up worth being ready for: can you create objects without a class? Not custom ones, no, every object in Python is an instance of some class, even built-in types like `int` and `str`.

**[Medium | Encapsulation] Why does Python use naming conventions for privacy instead of enforced access control?**

Python's design philosophy leans toward trusting developers rather than restricting them at the language level, "we're all consenting adults here" is the commonly quoted phrasing from the community. Single-underscore protected and double-underscore private (with name mangling) communicate intent clearly without a hard compiler-level wall, which keeps the language simpler while still giving developers the signal they need to respect a boundary.

**[Medium | Inheritance] What's the difference between inheritance and composition, and which does the industry generally favor?**

Inheritance models "is-a," composition models "has-a." The general industry guidance is to favor composition over inheritance by default, because it produces more flexible, more testable, more loosely coupled code, but inheritance remains the right tool when the "is-a" relationship is genuinely stable and structural. A strong answer gives a concrete example of each, not just the definitions.

**[Hard | Abstraction] Why does Python enforce abstract methods at instantiation time rather than at class definition time?**

Because an abstract base class is allowed to exist, and be inherited from, in an incomplete state; the incompleteness only becomes a real problem the moment someone tries to actually create a usable object from a class that hasn't fulfilled every required method. Checking at instantiation time catches the mistake exactly where it becomes real, without over-restricting how abstract classes and partial subclasses can be defined and extended along the way.

**[Hard | Polymorphism] Explain duck typing and why it matters in a dynamically typed language like Python.**

Duck typing means an object's suitability for an operation is judged by whether it has the right methods and attributes, not by its declared type or class hierarchy, "if it walks like a duck and quacks like a duck." It matters in Python specifically because there's no compiler checking formal interfaces ahead of time, so code that calls `.sound()` on an object doesn't need that object to inherit from any particular base class, it just needs `.sound()` to exist and work correctly when called.

---

## Practical coding questions

**[Easy] Write a `Rectangle` class with `width` and `height`, and a method `area()`.**

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height
```

The interviewer is checking basic class mechanics here, nothing tricky. A good candidate still gets it exactly right the first time.

**[Medium] Add a `@classmethod` to the `Rectangle` above that constructs a square.**

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    @classmethod
    def square(cls, side):
        return cls(side, side)

    def area(self):
        return self.width * self.height
```

They may follow up asking why `cls(side, side)` is preferred over `Rectangle(side, side)` here specifically, the answer being that `cls` correctly refers to whatever subclass actually called `square()`, which matters if `Rectangle` is ever subclassed.

**[Medium] Implement `__eq__` on a `Point` class so two points with the same coordinates compare equal.**

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y
```

A strong candidate proactively mentions that if `Point` objects need to go into a `set` or be used as dictionary keys, `__hash__` needs to be defined consistently too, since defining `__eq__` alone makes the default hash behavior inconsistent with equality.

**[Hard] Design a small class hierarchy for `Employee`, `Manager`, and `Executive`, where pay calculation differs at each level, and write a function that calculates total payroll for a mixed list.**

```python
class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def calculate_pay(self):
        return self.base_salary

class Manager(Employee):
    def __init__(self, name, base_salary, bonus):
        super().__init__(name, base_salary)
        self.bonus = bonus

    def calculate_pay(self):
        return self.base_salary + self.bonus

class Executive(Manager):
    def __init__(self, name, base_salary, bonus, stock_options):
        super().__init__(name, base_salary, bonus)
        self.stock_options = stock_options

    def calculate_pay(self):
        return super().calculate_pay() + self.stock_options

def total_payroll(employees):
    return sum(e.calculate_pay() for e in employees)
```

This is checking multilevel inheritance, proper `super()` usage across three levels, and polymorphism all at once, exactly the combination a real interview tends to test together rather than in isolation.

---

## Class design questions

**[Medium] Design a class to represent a library book, considering what state it needs to track and what operations it should support.**

A strong answer thinks out loud about the actual requirements before writing code: does a `Book` need to know if it's checked out? Who checked it out, and when it's due? Is `checkout()` a method on `Book` itself, or does that belong on a separate `Library` or `Loan` class instead? The interviewer isn't just checking whether you can write a class, they're checking whether you ask the right questions before committing to a design.

**[Hard] You're designing a system for a ride-sharing app: `Driver`, `Rider`, `Trip`, `Vehicle`. Sketch the relationships between these classes, including which are composition and which, if any, might reasonably use inheritance.**

A solid answer identifies that `Trip` composes a `Driver`, a `Rider`, and a `Vehicle` (a trip has these, isn't a specialized version of any of them), that `Vehicle` might reasonably have subclasses (`Car`, `Motorcycle`) if their behavior genuinely differs, and explicitly rules out inheritance between `Driver` and `Rider`, since despite both being "users" of the app, forcing a shared parent purely for code reuse without a genuine specialization relationship would be exactly the anti-pattern flagged in Lesson 7.

---

## Scenario-based design questions

**[Medium] A junior developer wrote a `User` class that inherits from a `Database` class so it can call `save()` directly. What's wrong with this, and how would you fix it?**

This is backwards inheritance: a `User` is not a kind of `Database`, there's no "is-a" relationship, the developer just wanted convenient access to `save()`. The fix is composition: `User` should hold a reference to a `Database` (or, better, a `Repository` abstraction) and call `self.database.save(self)`, keeping the relationship honest and keeping `User` free to be persisted by any storage mechanism, not permanently welded to one specific database implementation.

**[Hard] Your team's codebase has a `ReportGenerator` class that's grown to over 800 lines and handles data fetching, calculation, formatting, and email delivery. New features keep breaking unrelated parts of it. How do you approach fixing this?**

The strong answer walks through SRP explicitly: identify the genuinely distinct responsibilities tangled together, separate them into focused classes (`DataFetcher`, `Calculator`, `Formatter`, `EmailSender`), and have a slim `ReportGenerator` (or rename it entirely, something like `ReportService`) compose them together, coordinating without doing the work itself. Equally important: mention that this kind of refactor should happen incrementally, with tests in place, not as one giant rewrite, which shows awareness of real-world risk, not just textbook principles.

---

## Refactoring questions

**[Medium] Refactor this class, which has a clear cohesion problem.**

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def give_raise(self, amount):
        self.salary += amount

    def send_payslip_email(self):
        ...

    def calculate_company_tax_liability(self, all_employees):
        ...  # unrelated to a single employee's own concerns
```

`calculate_company_tax_liability` doesn't belong on `Employee` at all, it operates on a whole collection of employees and represents a company-level concern, not an individual one. It should move to a separate `Payroll` or `TaxCalculator` class that accepts a list of employees.

**[Hard] This code violates the Open/Closed Principle. Refactor it.**

```python
def calculate_shipping(order, method):
    if method == "standard":
        return order.weight * 0.5
    elif method == "express":
        return order.weight * 1.5
    elif method == "overnight":
        return order.weight * 3.0
```

The fix follows the exact OCP pattern from Lesson 11: an abstract `ShippingMethod` with `calculate(order)`, concrete subclasses for each method, and `calculate_shipping` reduced to simply calling `method.calculate(order)`, so a new shipping method is added by writing one new class rather than editing this function again.

---

## Common mistakes candidates make

Reciting the four pillars of OOP (encapsulation, inheritance, polymorphism, abstraction) as a memorized list without being able to explain why each one actually matters or give a concrete example. Reaching for inheritance in a design question purely because two classes share a couple of fields, without checking whether the relationship is genuinely "is-a." Forgetting that Python enforces very little at the language level, claiming private attributes are truly inaccessible, or that abstract methods can never have any implementation at all. Over-engineering a design answer with unnecessary abstraction layers for a problem that doesn't actually call for that much flexibility yet.

## Evaluation criteria interviewers actually use

Beyond correct syntax, interviewers are watching whether you ask clarifying questions before diving into a design (what does this system actually need to support, right now, versus hypothetically), whether you can justify a design decision when pushed on it rather than defending it reflexively, whether you recognize the tradeoffs in your own answer unprompted, and whether your class and method names actually communicate what they do without needing extra explanation. A design that's slightly less clever but clearly explained, with real tradeoffs acknowledged, consistently scores better than a flashier one you can't account for under questioning.

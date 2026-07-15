# Lesson 11: OOP Design Principles

## 1. Learning objectives

By the end of this lesson you should be able to:

- Explain coupling and cohesion in concrete terms, and evaluate a piece of code against both
- Apply the Single Responsibility Principle to spot a class that's doing too much
- Apply the Open/Closed Principle to recognize code that's fragile to extend
- Make and defend a real decision between composition and inheritance for a given scenario, not just recite the guidance
- Recognize the specific design mistakes beginners make repeatedly, in your own code, before they calcify into habits

## 2. Prerequisites

All of Lessons 1 through 10. This lesson doesn't introduce new syntax at all, it names and formalizes the judgment calls those ten lessons have been building toward.

## 3. Introduction

Every lesson in this module has quietly been teaching design judgment alongside syntax: when a mutable class attribute is dangerous, when private attributes fight against subclassing, when inheritance models a real relationship versus when it's forcing one. This lesson steps back and names those judgment calls properly, using the vocabulary the industry actually uses, so you can talk about them precisely in a design interview and recognize them instantly in a code review.

## 4. Theory

**Coupling** measures how much one piece of code depends on the internal details of another. High coupling means changing one class frequently forces changes in another; low coupling means classes can change independently. **Cohesion** measures how focused a single class is on one clear responsibility. High cohesion means everything inside a class genuinely belongs together; low cohesion means a class is a grab-bag of loosely related responsibilities stitched together for convenience.

```python
# Low cohesion, high coupling — a class doing too much, tightly bound to unrelated concerns
class OrderManager:
    def calculate_total(self, items):
        ...
    def save_to_database(self, order):
        ...
    def send_confirmation_email(self, customer):
        ...
    def generate_pdf_invoice(self, order):
        ...
```

`OrderManager` here is responsible for pricing logic, persistence, email delivery, and PDF generation, four genuinely separate concerns bolted onto one class. A change to how emails are sent risks touching a class that also handles pricing math, and every one of those four responsibilities is now coupled to the others through sharing a single class, whether they need to be or not.

```python
# Higher cohesion, lower coupling — responsibilities separated, composed together
class OrderPricer:
    def calculate_total(self, items):
        ...

class OrderRepository:
    def save(self, order):
        ...

class EmailNotifier:
    def send_confirmation(self, customer):
        ...

class InvoiceGenerator:
    def generate_pdf(self, order):
        ...

class OrderService:
    def __init__(self, pricer, repository, notifier, invoicer):
        self.pricer = pricer
        self.repository = repository
        self.notifier = notifier
        self.invoicer = invoicer
```

Each class now has exactly one reason to change. `OrderService` composes them together (directly applying Lesson 10), but doesn't do any of their work itself.

## 5. Why this concept exists

Software changes constantly, requirements shift, bugs get found, new features get requested, and the actual cost of a codebase over its lifetime is overwhelmingly the cost of making those changes safely, not the cost of writing the first working version. Coupling and cohesion are the two forces that most directly determine how expensive change is: tightly coupled, low-cohesion code means a small change ripples unpredictably through unrelated parts of the system, while loosely coupled, high-cohesion code means a change stays contained to the one place it actually belongs. This module's entire second half has effectively been teaching you to design for that second outcome.

## 6. Internal behavior

There's no interpreter mechanism here, this section instead covers how to actually diagnose coupling and cohesion in code you're reading. A practical test for cohesion: try to describe what a class does in one sentence, without using "and." If you can't, the class likely has more than one responsibility. A practical test for coupling: ask how many other classes would need to change if you modified this one class's internals, its private implementation, not its public interface. The more classes affected, the tighter the coupling, and the more fragile the system is to change.

## 7. Real-world analogy

A well-run restaurant kitchen has a line cook, a pastry chef, and a dishwasher, each with one clear job (high cohesion), coordinated by a head chef who directs the workflow without personally doing all three jobs (loose coupling, since replacing the dishwasher doesn't require retraining the pastry chef). A kitchen where one person is simultaneously plating, washing dishes, and managing the walk-in fridge inventory is the low-cohesion version: everything's tangled together, one person being out sick stalls the entire kitchen, and training a replacement means explaining four unrelated jobs at once instead of one focused one.

## 8. Enterprise use cases

The refactored `OrderService` example above is exactly the shape of real enterprise backend architecture: a thin coordinating "service" layer composed of focused, single-responsibility collaborators, each independently testable and independently replaceable. This is also precisely why unit testing becomes practical at scale, a highly cohesive `OrderPricer` can be tested with plain numbers and no database, mocked, or fake dependencies needed at all, while the tangled `OrderManager` version would require standing up a database connection and an email service just to test pricing math.

## 9. UML-style explanation

```
        ┌───────────────┐
        │  OrderService     │
        ├───────────────┤
        │ - pricer            │◆──────► OrderPricer
        │ - repository          │◆──────► OrderRepository
        │ - notifier             │◆──────► EmailNotifier
        │ - invoicer               │◆──────► InvoiceGenerator
        └───────────────┘
```

This is composition (Lesson 10) drawn explicitly in service of the Single Responsibility Principle: one coordinating class, several focused collaborators, each with exactly one filled diamond connecting it to the whole, and none of them connected to each other directly.

## 10. Syntax

**Single Responsibility Principle (SRP):** a class should have one, and only one, reason to change.

```python
# Violates SRP — pricing logic and formatting are two different reasons to change
class Invoice:
    def calculate_total(self, items):
        return sum(item.price for item in items)

    def print_formatted(self, items):
        total = self.calculate_total(items)
        return f"Total: ${total:.2f}\n" + "\n".join(str(i) for i in items)

# Follows SRP — split by actual reason to change
class InvoiceCalculator:
    def calculate_total(self, items):
        return sum(item.price for item in items)

class InvoiceFormatter:
    def format(self, items, total):
        return f"Total: ${total:.2f}\n" + "\n".join(str(i) for i in items)
```

**Open/Closed Principle (OCP):** a class should be open for extension, but closed for modification, you should be able to add new behavior without editing existing, already-tested code.

```python
# Violates OCP — adding a new discount type means editing this function every time
def apply_discount(price, discount_type):
    if discount_type == "percentage":
        return price * 0.9
    elif discount_type == "flat":
        return price - 10
    # every new discount type means another elif here, touching tested code

# Follows OCP — new discount types are added by writing a new class, not editing this one
from abc import ABC, abstractmethod

class Discount(ABC):
    @abstractmethod
    def apply(self, price):
        ...

class PercentageDiscount(Discount):
    def apply(self, price):
        return price * 0.9

class FlatDiscount(Discount):
    def apply(self, price):
        return price - 10

def apply_discount(price, discount: Discount):
    return discount.apply(price)  # never needs to change when a new Discount subclass appears
```

That second version is directly polymorphism (Lesson 8) and abstraction (Lesson 9) working together in service of OCP: adding `BuyOneGetOneDiscount` later means writing one new class, with zero changes to `apply_discount` itself.

## 11. Step-by-step examples

**Easy — identifying low cohesion by trying to summarize a class in one sentence:**

```python
class UserManager:
    def create_user(self, name):
        ...
    def send_welcome_email(self, user):
        ...
    def generate_sales_report(self, users):
        ...  # unrelated to user management, a clear cohesion violation
```

Try to describe `UserManager` in one sentence without "and." You can't, because `generate_sales_report` doesn't belong here at all, it's a completely separate responsibility that happened to get attached to a convenient existing class.

**Medium — applying SRP to split a real violation:**

```python
# Before
class ReportGenerator:
    def fetch_data(self, source):
        ...
    def calculate_statistics(self, data):
        ...
    def render_as_html(self, stats):
        ...

# After
class DataFetcher:
    def fetch(self, source):
        ...

class StatisticsCalculator:
    def calculate(self, data):
        ...

class HTMLRenderer:
    def render(self, stats):
        ...

class ReportGenerator:
    def __init__(self, fetcher, calculator, renderer):
        self.fetcher = fetcher
        self.calculator = calculator
        self.renderer = renderer

    def generate(self, source):
        data = self.fetcher.fetch(source)
        stats = self.calculator.calculate(data)
        return self.renderer.render(stats)
```

**Hard — a composition-versus-inheritance decision, made and justified explicitly, the real skill this lesson is teaching:**

Scenario: you're modeling `SavingsAccount` and `CheckingAccount`. Both need a balance, a `deposit()` method, and their own distinct `withdraw()` rules (savings limits withdrawals per month, checking allows overdraft up to a limit).

```python
class Account:  # shared "is-a" relationship is genuine here — both really are accounts
    def __init__(self, balance):
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

class SavingsAccount(Account):
    def __init__(self, balance, monthly_limit=6):
        super().__init__(balance)
        self.monthly_limit = monthly_limit
        self.withdrawals_this_month = 0

    def withdraw(self, amount):
        if self.withdrawals_this_month >= self.monthly_limit:
            raise ValueError("Monthly withdrawal limit reached")
        self.balance -= amount
        self.withdrawals_this_month += 1

class CheckingAccount(Account):
    def __init__(self, balance, overdraft_limit=100):
        super().__init__(balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if self.balance - amount < -self.overdraft_limit:
            raise ValueError("Overdraft limit exceeded")
        self.balance -= amount
```

Inheritance is the right call here specifically because "is-a" is genuinely true and stable: a `SavingsAccount` really is a kind of `Account`, sharing real, permanent structure (`balance`, `deposit`), while each subtype's `withdraw` rule is a legitimate specialization, not an unrelated bolt-on. Compare this to the `Manager`/`Team` composition exercise from Lesson 10, where inheritance would have been the wrong call, and notice that the deciding factor both times is the same question: is this genuinely "is-a," stable and structural, or is it "has-a" dressed up for convenience?

## 12. Common mistakes

**Treating SRP as "each class should have exactly one method."** SRP is about one reason to change, not one method; a cohesive class can have several methods that all serve the same single responsibility perfectly well.

**Applying OCP everywhere reflexively, adding abstract interfaces for things that will never realistically have a second implementation,** which is the same premature-abstraction mistake flagged in Lesson 9, now named as a design principle being over-applied rather than under-applied.

**Treating "favor composition over inheritance" as "never use inheritance."** The Lesson 11 example above shows a case where inheritance is genuinely correct. The principle is a default lean, not an absolute rule, and a good engineer can articulate why a specific case is the exception.

**Refactoring for cohesion and coupling without a real reason to, mid-project, disrupting working code for a purely theoretical improvement.** These principles are lenses for evaluating new design decisions and diagnosing genuine pain points, not a checklist to compulsively re-apply to everything that already works.

## 13. Debugging tips

If a bug fix in one class keeps requiring changes in several unrelated other classes, that's tight coupling actively costing you time right now, and it's worth pausing to ask whether those classes' responsibilities should be reorganized. If you're afraid to touch a class because you're not sure what else might break, that's usually a low-cohesion, high-coupling class, and it's exactly the kind of code these principles are meant to help you both diagnose and avoid creating in the first place.

## 14. Best practices

Ask "what's this class's one job?" before writing it, not after it's grown unwieldy. Default to composition for "has-a" relationships and reach for inheritance specifically when "is-a" is genuinely stable and structural. Apply OCP where a family of interchangeable variations is a real, current need, not a hypothetical future one. Revisit coupling and cohesion when a change is genuinely painful, that pain is real, actionable signal, not when a class is just working quietly and doing its job.

## 15. Performance considerations

None of these principles carry a runtime performance cost or benefit; they're entirely about the cost of understanding and changing code over its lifetime, not the cost of executing it. A tightly coupled, low-cohesion program runs exactly as fast as a well-designed one; it's just far more expensive, in engineering time, to safely change later.

## 16. Code style

A class name that needs "and" or a vague catch-all word like "Manager" or "Handler" to describe everything it does is a real style signal worth taking seriously, it often means the class's responsibility isn't actually singular. Constructor parameters that are abstract interfaces (Lesson 9), rather than concrete classes, are a visible style signal of intentional loose coupling, and worth favoring when a dependency might reasonably need to vary.

## 17. Interview questions with model answers

**Q: What's the difference between coupling and cohesion?**

Coupling measures how dependent one piece of code is on another's internal details, low coupling means classes can change independently. Cohesion measures how focused a single class is on one clear responsibility, high cohesion means everything inside the class genuinely belongs together. A strong answer explicitly notes the goal: low coupling, high cohesion, and can give a concrete before-and-after example, like the `OrderManager` refactor from this lesson, rather than only reciting the definitions.

**Q: Explain the Single Responsibility Principle with an example.**

A class should have exactly one reason to change. A strong answer picks a concrete violation, a class handling both business logic and, say, email sending, and explains specifically what happens when those two concerns are tangled together: a change to email formatting risks destabilizing unrelated business logic that happens to live in the same class, purely because of proximity, not genuine relationship.

**Q: When should you choose composition over inheritance, and when is inheritance still the right call?**

Composition is generally the safer default for "has-a" relationships and for anything that might need to vary or be swapped later. Inheritance remains the right call when the relationship is genuinely, stably "is-a," and the shared structure is real and unlikely to need untangling later, the `SavingsAccount extends Account` example from this lesson is a legitimate, defensible use of inheritance, not an anti-pattern. A candidate who can articulate both sides, including a case where inheritance is correct, is showing real judgment rather than reciting the "composition good, inheritance bad" version of this guidance, which is an oversimplification.

## 18. Knowledge check

1. What's a practical, one-sentence test for whether a class has good cohesion?
2. What's the actual formal difference between SRP and OCP?
3. Give an example where inheritance is genuinely the correct design choice, and explain why.
4. What real, ongoing cost does tight coupling and low cohesion actually impose on a team?

## 19. Hands-on exercises

**Easy**

1. Take a class with at least three unrelated responsibilities (write it yourself, deliberately) and identify each responsibility in a comment.
2. Rewrite that class into two or three separate, more cohesive classes.
3. Write one sentence describing what each of your new classes does, confirming none of them needed "and."

**Medium**

4. Take the `apply_discount` OCP example from this lesson and add a third discount type (`BuyOneGetOneDiscount`) without modifying `apply_discount` itself at all.
5. Identify a class from an earlier lesson's exercises that could be argued to violate SRP, and refactor it, explaining your reasoning in a short comment.
6. Design two classes, one where inheritance is clearly the right relationship and one where composition clearly is, and write a one-paragraph justification for each choice.

**Hard**

7. Take the `OrderManager` low-cohesion example from this lesson's theory section and fully refactor it into the separated, composed version, writing real (if simple) implementations for each of the four responsibilities, not just empty method stubs.
8. Design a small plugin-style discount or pricing engine (similar to the OCP example) that supports at least four different rule types, all added without ever modifying the core class that applies them, and write a short reflection on what would have gone wrong if you'd used an `if`/`elif` chain instead.

## 20. Stretch challenge

Go back to the Module 1 capstone project, or any earlier piece of code you've written in this course, and perform a genuine coupling-and-cohesion audit on it: pick one class or function, describe its actual responsibilities honestly (even if there are several), and decide, with real justification, whether it should be split apart, and if so, into what. Then actually do the refactor. This exercise is deliberately not hypothetical, applying these principles to code you already wrote and already understand is a much more honest test of whether the ideas have actually landed than applying them to a fresh example built to illustrate the point.

## 21. Summary

Coupling and cohesion are the two forces that most determine how expensive a codebase is to change over time, and every principle in this lesson, SRP, OCP, composition over inheritance, is really just a specific, actionable strategy for keeping coupling low and cohesion high. None of these are absolute rules; they're lenses for evaluating a real design decision, and knowing when a principle doesn't apply, like recognizing a genuinely valid use of inheritance, is just as much a sign of real understanding as applying the principle correctly in the first place. This closes out the conceptual core of Module 2; everything from here is applying it.

## 22. Additional resources

- [Wikipedia: SOLID (object-oriented design)](https://en.wikipedia.org/wiki/SOLID)
- [Martin Fowler: CouplingAndCohesion](https://martinfowler.com/ieeeSoftware/coupling.pdf)
- [Gang of Four design principle: composition over inheritance, revisited in context](https://en.wikipedia.org/wiki/Composition_over_inheritance)

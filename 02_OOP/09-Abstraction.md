# Lesson 9: Abstraction

## 1. Learning objectives

By the end of this lesson you should be able to:

- Explain abstraction as distinct from encapsulation, a distinction that's genuinely easy to blur
- Use Python's `abc` module to define abstract classes and abstract methods correctly
- Explain why Python enforces abstract methods at instantiation time rather than at import time
- Design a clean interface for a set of related classes before writing their concrete implementations
- Recognize when abstraction is genuinely earning its complexity versus adding ceremony for no real benefit

## 2. Prerequisites

Lessons 1 through 8, particularly Inheritance and Polymorphism. Abstraction is really about formalizing the shared interface that polymorphism relies on.

## 3. Introduction

Back in Lesson 8, the `Shape` base class had an `area()` method that just raised `NotImplementedError`, a way of saying "every real shape must implement this" without providing any real implementation itself. That was an informal abstraction. This lesson makes it formal, using Python's `abc` module to actually enforce that rule at the language level, so a class that forgets to implement a required method fails loudly and immediately, rather than only failing later when someone happens to call the missing method.

## 4. Theory

Abstraction means defining what something should do without necessarily specifying how, and, critically, preventing incomplete or purely conceptual classes from being instantiated directly.

```python
from abc import ABC, abstractmethod

class Shape(ABC):  # inheriting from ABC marks this as an abstract base class
    @abstractmethod
    def area(self):
        ...  # no implementation — subclasses are required to provide one

    @abstractmethod
    def perimeter(self):
        ...

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

    def perimeter(self):
        return 2 * 3.14159 * self.radius

c = Circle(5)  # works fine — Circle implements every abstract method
# s = Shape()   # TypeError — can't instantiate an abstract class directly
```

If `Circle` forgot to implement `perimeter()`, attempting `Circle(5)` would raise `TypeError` immediately, not silently succeed and only fail later when someone happened to call `.perimeter()`. That's the entire practical value abstraction adds over the informal `NotImplementedError` approach from Lesson 8: the mistake is caught the moment an incomplete subclass is instantiated, not buried until a specific code path happens to run.

## 5. Why this concept exists

The informal pattern (`raise NotImplementedError` in a base method) relies entirely on someone reading the code and understanding the convention; nothing stops you from instantiating the base class directly, or from forgetting to override the method in a subclass and not finding out until that specific method happens to get called in production. Abstraction, enforced properly through the `abc` module, turns "please implement this" from a comment and a convention into a hard, checked requirement, which is exactly the kind of guarantee that matters more as a codebase and its team grow.

## 6. Internal behavior

`ABC` is a class built on a metaclass, `ABCMeta`, which intercepts object instantiation and checks whether every method decorated with `@abstractmethod` on the class (or inherited abstract methods) has actually been overridden with a concrete implementation somewhere in the class hierarchy. If any abstract method remains unimplemented, attempting to instantiate that class raises `TypeError` immediately, before `__init__` even runs. This check happens at instantiation time, not at class definition time, which is why you can define `Shape(ABC)` with unimplemented abstract methods without any error, the error only appears the moment someone tries to actually create a `Shape()` instance directly, or an incomplete subclass instance.

## 7. Real-world analogy

An architect's blueprint for "a building with a foundation, walls, and a roof" describes a category, not an actual, livable structure. You cannot move into the blueprint. Every actual building constructed from it, a house, an office tower, a warehouse, has to genuinely provide a real foundation, real walls, and a real roof, the blueprint's requirements, filled in with concrete materials specific to that building. An abstract class is the blueprint category itself: conceptually essential, but never something you live in directly, and every concrete subclass is contractually required to actually build out every part the blueprint demanded.

## 8. Enterprise use cases

A `PaymentGateway` abstract base class defining `charge(amount)` and `refund(amount)` as abstract methods, with concrete `StripeGateway` and `PayPalGateway` subclasses each implementing the actual API calls, is a standard enterprise abstraction pattern. It guarantees, at the language level, that any new payment provider added later must implement both required operations, or the class simply can't be instantiated, catching an incomplete integration immediately during development rather than discovering a missing method in production when a specific, rarely used code path finally executes.

## 9. UML-style explanation

```
              «abstract»
           ┌─────────────────┐
           │      Shape          │
           ├─────────────────┤
           │ + area(): float       │  «abstract»
           │ + perimeter(): float    │  «abstract»
           └────────┬────────┘
                     │
             ┌───────▼───────┐
             │     Circle         │
             ├───────────────┤
             │ + area(): float      │
             │ + perimeter(): float   │
             └───────────────┘
```

UML marks abstract classes and abstract methods with the `«abstract»` stereotype (or italicized text, in tooling that supports it). This is a small but genuinely useful visual convention: it tells anyone reading the diagram, at a glance, "you cannot instantiate this box directly, it exists purely to define a contract."

## 10. Syntax

**Basic abstract class with the `abc` module:**

```python
from abc import ABC, abstractmethod

class Repository(ABC):
    @abstractmethod
    def save(self, item):
        ...

    @abstractmethod
    def find_by_id(self, item_id):
        ...

class InMemoryRepository(Repository):
    def __init__(self):
        self.items = {}

    def save(self, item):
        self.items[item["id"]] = item

    def find_by_id(self, item_id):
        return self.items.get(item_id)
```

**An abstract class can still provide concrete, shared methods alongside its abstract ones:**

```python
from abc import ABC, abstractmethod

class Employee(ABC):
    def __init__(self, name):
        self.name = name

    def introduce(self):  # concrete method, shared by every subclass, not abstract
        return f"Hi, I'm {self.name}"

    @abstractmethod
    def calculate_pay(self):  # every subclass must define its own version
        ...

class HourlyEmployee(Employee):
    def __init__(self, name, hours, rate):
        super().__init__(name)
        self.hours = hours
        self.rate = rate

    def calculate_pay(self):
        return self.hours * self.rate

emp = HourlyEmployee("Sam", 40, 25)
print(emp.introduce())          # inherited concrete method, works normally
print(emp.calculate_pay())       # required abstract method, correctly implemented
```

This mixed pattern, some concrete shared behavior alongside some strictly required abstract methods, is extremely common in real abstract base classes; abstraction doesn't mean a class has to be entirely empty of implementation.

## 11. Step-by-step examples

**Easy — confirming that an abstract class can't be instantiated directly:**

```python
from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def speak(self):
        ...

try:
    a = Animal()
except TypeError as e:
    print(f"Blocked: {e}")
```

**Medium — an incomplete subclass also fails at instantiation:**

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        ...
    @abstractmethod
    def perimeter(self):
        ...

class BrokenSquare(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2
    # perimeter() is missing entirely

try:
    s = BrokenSquare(4)
except TypeError as e:
    print(f"Blocked: {e}")
```

**Hard — designing an interface first, then filling in multiple concrete implementations, the realistic order of operations for a real feature:**

```python
from abc import ABC, abstractmethod

class NotificationChannel(ABC):
    @abstractmethod
    def send(self, recipient, message):
        ...

class EmailChannel(NotificationChannel):
    def send(self, recipient, message):
        return f"Emailing {recipient}: {message}"

class SMSChannel(NotificationChannel):
    def send(self, recipient, message):
        return f"Texting {recipient}: {message}"

def notify_all(channels, recipient, message):
    for channel in channels:
        print(channel.send(recipient, message))

notify_all([EmailChannel(), SMSChannel()], "alex@example.com", "Your order shipped")
```

Notice the order this was built in: the abstract interface (`NotificationChannel`) came first, defining exactly what any channel must be able to do, and the concrete classes were written to satisfy that contract afterward. That's the realistic, and recommended, order for designing abstraction in practice, not retrofitting an interface after several unrelated concrete classes already exist.

## 12. Common mistakes

**Confusing abstraction with encapsulation.** Encapsulation (Lesson 6) is about controlling access to an object's internal data. Abstraction is about defining a required interface, what a class must be able to do, without necessarily specifying how. They're often used together, but they're solving different problems, and conflating them in an interview answer is a common, easily avoidable stumble.

**Adding abstract methods for behavior that only ever has one implementation, and no realistic prospect of a second.** Abstraction earns its complexity when there's a genuine family of interchangeable implementations. A single, permanent implementation doesn't need an abstract interface sitting in front of it, that's ceremony without payoff.

**Forgetting `@abstractmethod` on a method that should be required,** which means Python won't enforce it at all, silently defeating the entire purpose of using `ABC` in the first place.

**Providing an actual implementation body under `@abstractmethod` and assuming it will run by default.** It won't, unless a subclass explicitly calls it via `super()`. An abstract method's own body, if it has one beyond `...` or `pass`, is only ever reachable through an explicit `super()` call from an overriding subclass.

## 13. Debugging tips

If instantiating a class you expected to work raises `TypeError` mentioning "Can't instantiate abstract class," check for any inherited abstract method that hasn't actually been overridden, sometimes several levels up an inheritance chain, not just directly in the immediate parent. If a required method isn't being enforced at all, double check the `@abstractmethod` decorator is actually present and that the class genuinely inherits from `ABC` (or uses `ABCMeta` directly), a class that forgets to inherit from `ABC` gets none of this enforcement, `@abstractmethod` alone does nothing without it.

## 14. Best practices

Design the abstract interface first, thinking through exactly what every concrete implementation must be able to do, before writing any concrete subclasses. Keep abstract methods focused on genuine behavioral contracts, not implementation details that different subclasses might reasonably want to vary in shape, not just in specifics. Mix concrete, shared methods into an abstract base class freely when behavior really is common to every subclass; don't force every single method to be abstract just for consistency.

## 15. Performance considerations

The `abc` module's enforcement check happens once, at instantiation time, and is negligible in cost compared to the rest of object construction. There's no meaningful runtime performance difference between a class that inherits from `ABC` and one that doesn't; this is purely a design-time safety mechanism, not a performance-relevant one.

## 16. Code style

Name abstract base classes for the role or capability they represent (`Repository`, `PaymentGateway`, `NotificationChannel`), not with a generic `Base` prefix that says nothing about what the class actually guarantees. Keep abstract method bodies minimal, `...` or a short docstring describing the contract, rather than dead code that looks like it does something but never actually runs unless a subclass explicitly opts in via `super()`.

## 17. Interview questions with model answers

**Q: What's the difference between abstraction and encapsulation?**

Abstraction defines what a class or interface must be able to do, a required contract, without necessarily specifying the internal how. Encapsulation controls access to an object's internal data and implementation details, restricting what's exposed and enforcing controlled access through methods or properties. They're complementary, a well-designed abstract interface typically hides its concrete implementations' internal details too, but they answer genuinely different design questions, and a candidate should be able to state that difference cleanly without conflating them.

**Q: Why use Python's `abc` module instead of just raising `NotImplementedError` in a base method?**

`NotImplementedError` is a convention, it only fails when the missing method is actually called, which could be much later, in a rarely exercised code path, possibly in production. The `abc` module enforces the requirement immediately, at instantiation time: an incomplete subclass simply can't be created at all, which surfaces the mistake the moment it's introduced, during development, rather than whenever an unlucky code path finally triggers it.

**Q: When would you decide not to use an abstract base class?**

When there's genuinely only one implementation, with no realistic near-term need for a second, interchangeable one. Introducing an abstract interface for a single concrete class adds a layer of indirection with no real payoff; it's premature abstraction. The interviewer is checking whether you reach for abstraction because it solves a real, present design problem, not out of reflexive "best practice" habit.

## 18. Knowledge check

1. What happens if you try to instantiate a class that inherits from `ABC` and still has an unimplemented `@abstractmethod`?
2. How is abstraction different from encapsulation?
3. Can an abstract base class contain concrete, non-abstract methods? Give an example of when that's useful.
4. Why is enforcing a missing method at instantiation time better than only discovering it when the method is finally called?

## 19. Hands-on exercises

**Easy**

1. Define an abstract `Vehicle` class with an abstract method `start_engine()`, and a concrete `Car` subclass that implements it.
2. Attempt to instantiate the abstract `Vehicle` class directly and confirm it raises `TypeError`.
3. Add a concrete, shared method `honk()` to the abstract `Vehicle` class (not abstract) and confirm every subclass inherits it without needing to redefine it.

**Medium**

4. Design an abstract `DataExporter` class with an abstract method `export(data)`, and build two concrete subclasses, `JSONExporter` and `CSVExporter`, each implementing it differently.
5. Deliberately create an incomplete subclass of an abstract class (missing one required method) and confirm instantiating it raises a clear `TypeError`.
6. Design an abstract `Repository` class with abstract methods `save(item)` and `find_by_id(item_id)`, and build a concrete `InMemoryRepository` implementation backed by a dictionary.

**Hard**

7. Design an abstract `PaymentGateway` class with abstract methods `charge(amount)` and `refund(amount)`, build at least two concrete implementations, and write a function that processes a list of mixed gateway objects polymorphically, tying this lesson directly back to Lesson 8.
8. Design an abstract class hierarchy for a notification system (`NotificationChannel`, abstract `send()`) with at least three concrete channels, and add a concrete, shared `log_attempt()` method on the abstract base that every channel inherits and uses internally before calling its own `send()` implementation via `super()` conventions, demonstrating the mixed concrete-and-abstract pattern from this lesson.

## 20. Stretch challenge

Design an abstract `Cache` interface with abstract methods `get(key)`, `set(key, value)`, and `delete(key)`. Build two concrete implementations: an `InMemoryCache` backed by a plain dictionary, and a `FileCache` that persists its data to a JSON file on disk between runs (tying this back to Module 1's file handling). Write test code that exercises both implementations through the exact same interface, calling `get`, `set`, and `delete` identically on each, and confirm both behave correctly according to the shared contract despite having completely different internals. This is abstraction actually paying for itself: swapping the storage mechanism entirely without changing a single line of code that uses the cache.

## 21. Summary

Abstraction defines a required contract, what a class must be able to do, and Python's `abc` module turns that from a polite convention into an enforced rule, checked the moment an incomplete class is instantiated rather than whenever a missing method happens to get called. It's distinct from encapsulation, which controls access to internal data rather than defining external behavioral requirements, even though the two frequently work together in a well-designed class. Abstraction earns its complexity when there's a genuine, ongoing family of interchangeable implementations behind a shared interface; reach for it deliberately, not reflexively.

## 22. Additional resources

- [Python official docs: abc — Abstract Base Classes](https://docs.python.org/3/library/abc.html)
- [PEP 3119 — Introducing Abstract Base Classes](https://peps.python.org/pep-3119/)
- [Real Python: Python's abc Module](https://realpython.com/python-interface/)

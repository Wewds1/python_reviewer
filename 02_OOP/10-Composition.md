# Lesson 10: Composition

## 1. Learning objectives

By the end of this lesson you should be able to:

- Explain "has-a" relationships and how they differ fundamentally from the "is-a" relationships inheritance models
- Distinguish composition from aggregation, and know why the difference (ownership and lifecycle) actually matters
- Build classes using composition, delegating behavior to contained objects rather than inheriting it
- Explain loose coupling and high cohesion in concrete, non-buzzword terms
- Make a real, defensible decision between composition and inheritance for a given design problem

## 2. Prerequisites

Lessons 1 through 9. This lesson is, in a real sense, the payoff and the counterbalance to everything Lesson 7 taught about inheritance.

## 3. Introduction

Every warning in Lesson 7 about forcing an "is-a" relationship where none really exists has been building toward this lesson. Composition is the other major way to build relationships between classes: instead of a subclass inheriting a parent's behavior, one class simply holds an instance of another as an attribute, and delegates to it. It's less flashy than inheritance, and in a huge number of real design situations, it's the better, more flexible choice.

## 4. Theory

A "has-a" relationship means one object contains, or is built from, another, rather than being a specialized version of it. A `Car` has an `Engine`; a `Car` is not a kind of `Engine`. That's composition.

```python
class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower

    def start(self):
        return f"Engine starting with {self.horsepower} HP"

class Car:
    def __init__(self, make, horsepower):
        self.make = make
        self.engine = Engine(horsepower)  # Car HAS an Engine, doesn't inherit from it

    def start(self):
        return f"{self.make}: {self.engine.start()}"  # delegating to the contained object

car = Car("Toyota", 180)
print(car.start())
```

`Car` doesn't inherit `start()` from `Engine`, it holds an `Engine` instance and delegates the actual work to it. This is a fundamentally different relationship from the `Dog(Animal)` inheritance shape from Lesson 7, and it solves a different kind of problem.

## 5. Why this concept exists

Not every real-world relationship is "is-a." A `Car` is not a specialized `Engine`; it's built from one, along with wheels, a chassis, and a transmission, each of which is its own independent, reusable concept. Forcing this into inheritance (`class Car(Engine)`) would be structurally wrong, and it would prevent an `Engine` from ever being reused independently, in a `Boat` or a `Generator`, since inheritance ties a subclass permanently to one specific parent's identity. Composition solves this by keeping each piece independent and swappable, assembled together rather than fused into a rigid hierarchy.

## 6. Internal behavior

There's no special language mechanism for composition, it's simply an object holding a reference to another object as an attribute, exactly the same variable-binding model covered all the way back in Module 1. `self.engine = Engine(horsepower)` stores a reference to an `Engine` instance inside the `Car` instance's own `__dict__`. Calling `self.engine.start()` is an ordinary method lookup on that referenced object, nothing about it is different from any other attribute access you've already learned. Composition's power comes entirely from the design choice to structure relationships this way, not from any new syntax.

## 7. Real-world analogy

A computer has a CPU, has RAM, has a hard drive. None of those components are "a kind of" computer, and a computer isn't "a kind of" CPU either. Each part is an independent, self-contained thing that can be manufactured, tested, and even replaced on its own, and the computer is assembled from them, coordinating their combined behavior. Swap in a faster CPU, and the computer as a whole benefits, without needing to redesign what "computer" fundamentally means. That's composition: independent, interchangeable parts, assembled into a whole, rather than a single rigid hierarchy where everything is permanently fused together.

## 8. Enterprise use cases

An `Order` class composed of a `Customer`, a list of `LineItem` objects, and a `ShippingAddress`, is a textbook composition structure: an order genuinely has a customer and has line items, it isn't a specialized kind of customer. Service classes in enterprise backends are also frequently composed rather than inherited: an `OrderService` might hold a `PaymentGateway` and a `NotificationChannel` as attributes (both abstract interfaces, tying directly back to Lesson 9), letting the concrete payment or notification implementation be swapped out entirely, in tests or in production, without changing `OrderService` itself at all. This swappability, a direct consequence of composition plus abstraction working together, is one of the most practically valuable patterns in real backend architecture.

## 9. UML-style explanation

```
┌───────────────┐  1        1  ┌───────────────┐
│      Car          │◆────────────│     Engine         │
├───────────────┤               ├───────────────┤
│ - make: str          │               │ - horsepower: int    │
│ - engine: Engine       │               ├───────────────┤
├───────────────┤               │ + start(): str         │
│ + start(): str         │               └───────────────┘
└───────────────┘
```

A filled diamond (◆) at the "whole" end of the line is the standard UML notation for composition, signaling that the `Engine` genuinely belongs to, and typically doesn't outlive, the specific `Car` it's part of. This is visually distinct from the open-triangle "is-a" arrow used for inheritance in Lesson 7, and from the hollow-diamond notation for the weaker aggregation relationship, covered next.

## 10. Syntax

**Composition versus aggregation**, a distinction worth being precise about:

Composition implies ownership and a shared lifecycle: the contained object is created by, and typically dies with, the containing object. If you delete the `Car`, its specific `Engine` instance has no independent purpose anymore.

```python
class Car:
    def __init__(self, make, horsepower):
        self.make = make
        self.engine = Engine(horsepower)  # composition — Car creates and owns this Engine
```

Aggregation implies a "has-a" relationship too, but without ownership; the contained object exists independently and could outlive, or be shared across, the containing object.

```python
class Department:
    def __init__(self, name, employees):
        self.name = name
        self.employees = employees  # aggregation — Employees exist independently of this Department

engineering = Employee("Alex")
sales_and_marketing = Employee("Sam")
dept = Department("Product", [engineering])  # dept doesn't own Alex; Alex existed before, and independently
```

If `dept` gets deleted, `engineering` (Alex, the actual `Employee` object) still exists and could be assigned to a different department entirely. That independent, shareable lifecycle is exactly what separates aggregation from true composition.

**Composition enabling loose coupling**, by depending on an abstract interface rather than a concrete class:

```python
from abc import ABC, abstractmethod

class NotificationChannel(ABC):
    @abstractmethod
    def send(self, message):
        ...

class EmailChannel(NotificationChannel):
    def send(self, message):
        return f"Emailing: {message}"

class OrderService:
    def __init__(self, notifier: NotificationChannel):
        self.notifier = notifier  # composed with an abstraction, not a specific concrete class

    def complete_order(self):
        return self.notifier.send("Your order is complete")

service = OrderService(EmailChannel())  # could just as easily be an SMSChannel, unchanged elsewhere
print(service.complete_order())
```

`OrderService` never mentions `EmailChannel` by name in its own definition, only the abstract `NotificationChannel` interface. Swapping in a completely different concrete channel requires zero changes to `OrderService` itself, which is exactly the loose coupling this section is named for.

## 11. Step-by-step examples

**Easy — basic composition, one class holding another:**

```python
class Address:
    def __init__(self, city, zip_code):
        self.city = city
        self.zip_code = zip_code

class Customer:
    def __init__(self, name, address):
        self.name = name
        self.address = address  # Customer HAS an Address

cust = Customer("Alex", Address("Springfield", "62704"))
print(cust.address.city)
```

**Medium — composing multiple objects and delegating combined behavior:**

```python
class Engine:
    def start(self):
        return "Engine on"

class Battery:
    def __init__(self, charge_percent):
        self.charge_percent = charge_percent

    def check(self):
        return f"Battery at {self.charge_percent}%"

class ElectricCar:
    def __init__(self, charge_percent):
        self.engine = Engine()
        self.battery = Battery(charge_percent)

    def start(self):
        return f"{self.battery.check()}, {self.engine.start()}"

print(ElectricCar(85).start())
```

**Hard — swapping a composed dependency to change behavior entirely, with zero changes to the class that uses it, the loose-coupling payoff made concrete:**

```python
from abc import ABC, abstractmethod

class Storage(ABC):
    @abstractmethod
    def save(self, data):
        ...

class LocalFileStorage(Storage):
    def save(self, data):
        return f"Saved '{data}' to local disk"

class CloudStorage(Storage):
    def save(self, data):
        return f"Uploaded '{data}' to the cloud"

class BackupManager:
    def __init__(self, storage: Storage):
        self.storage = storage

    def run_backup(self, data):
        return self.storage.save(data)

local_manager = BackupManager(LocalFileStorage())
cloud_manager = BackupManager(CloudStorage())

print(local_manager.run_backup("database.db"))
print(cloud_manager.run_backup("database.db"))
```

`BackupManager`'s code never changes between these two calls. Only which concrete `Storage` implementation it was composed with changes, at the moment it was constructed. This is the exact mechanism that makes automated testing far easier too: a test can compose `BackupManager` with a fake, in-memory storage implementation instead of the real one, with no changes to `BackupManager` needed at all.

## 12. Common mistakes

**Reaching for inheritance to reuse a chunk of behavior, when there's no genuine "is-a" relationship,** the exact anti-pattern flagged back in Lesson 7. If you catch yourself thinking "I'll just inherit from this class to get its methods," pause and ask whether the relationship is really "is-a," or whether it's actually "has-a" wearing inheritance's clothing.

**Confusing composition and aggregation, and not thinking about object lifecycle at all.** It matters in real design: if a contained object should be independently creatable, shareable across multiple containers, and outlive any one container, that's aggregation, and forcing true ownership-style composition onto it can create awkward, overly rigid designs.

**Composing with a concrete class instead of an abstraction when flexibility is actually needed later.** `self.notifier = EmailChannel()` hardcoded directly inside a class's `__init__`, instead of accepting any `NotificationChannel` as a constructor parameter, locks that class to one specific implementation and quietly reintroduces the same rigidity composition was supposed to avoid.

## 13. Debugging tips

If you're finding it hard to explain why one class inherits from another beyond "it needed some of those methods," that's a strong signal the relationship should have been composition instead. If a class is difficult to test in isolation because it always drags along a specific, heavy concrete dependency (a real database connection, a real payment API), check whether that dependency was composed in directly (hardcoded inside `__init__`) rather than accepted as a parameter, an abstraction, that a test could substitute a fake for.

## 14. Best practices

Default to composition when the relationship is genuinely "has-a" rather than "is-a," which, in real-world modeling, is more often than beginners initially expect. Compose against abstract interfaces (Lesson 9) rather than concrete classes whenever a dependency might reasonably need to be swapped, in production or in tests. Keep composed classes focused and independently meaningful, an `Engine` should make sense and be testable entirely on its own, without needing a `Car` to exist first.

## 15. Performance considerations

Composition has no inherent performance cost beyond the ordinary cost of object creation and attribute access already covered in earlier lessons, there's no meaningful runtime difference between "is-a" and "has-a" relationships at the interpreter level. The performance conversation here is entirely about design flexibility and testability over time, not raw execution speed.

## 16. Code style

Name composed attributes for what they represent (`self.engine`, `self.address`), not generically (`self.obj1`). When a composed dependency is meant to be swappable, accept it as a constructor parameter with a type hint pointing at the abstract interface, rather than instantiating a specific concrete class directly inside `__init__`.

## 17. Interview questions with model answers

**Q: What's the difference between composition and inheritance, and how do you decide between them?**

Inheritance models a genuine "is-a" relationship, one class is fundamentally a specialized version of another, and it makes the most sense when that relationship is stable and unlikely to need restructuring. Composition models a "has-a" relationship, one class is built from or contains another, and it's the better choice, in the majority of real design situations, whenever the relationship is really about assembly rather than specialization, or whenever flexibility to swap a component later matters. A strong answer states the general industry guidance directly: favor composition over inheritance, and reach for inheritance specifically, deliberately, when the "is-a" relationship is genuinely solid.

**Q: What's the difference between composition and aggregation?**

Both are "has-a" relationships, but composition implies ownership and a shared lifecycle, the contained object is created by and typically dies with its container. Aggregation implies a "has-a" relationship without that ownership, the contained object exists independently and can outlive or be shared across multiple containers. A concrete example works better than the abstract definition: a `Car` composes its own `Engine` (the engine has no purpose outside that specific car), while a `Department` aggregates `Employee` objects (an employee existed before joining, and can move to a different department later).

**Q: How does composition support loose coupling?**

By having a class depend on an abstract interface (an `ABC`, as covered in Lesson 9) rather than a specific concrete class, the concrete implementation it's actually composed with can be swapped freely, in production configuration or in a test suite, without requiring any changes to the class that depends on it. This is also exactly what makes classes genuinely unit-testable in isolation, a fake or mock implementation can be substituted for the real dependency with zero changes to the class under test.

## 18. Knowledge check

1. What's the core difference between an "is-a" and a "has-a" relationship?
2. How does composition differ from aggregation, specifically regarding object lifecycle?
3. Why does composing against an abstract interface, rather than a concrete class, improve testability?
4. Give an example of a relationship that's clearly composition, and one that's clearly aggregation, and explain why each is which.

## 19. Hands-on exercises

**Easy**

1. Write a `Wheel` class and a `Car` class where `Car` is composed of four `Wheel` instances.
2. Write an `Address` class and a `Person` class where `Person` has an `Address` attribute, and print a person's city through the composed object.
3. Identify, in a short comment, whether a `Library` containing `Book` objects is composition or aggregation, and justify your answer based on lifecycle.

**Medium**

4. Build a `Computer` class composed of a `CPU` and a `RAM` class, each with their own attributes and at least one method, and have `Computer.boot()` delegate to both composed objects.
5. Refactor a class that currently hardcodes a concrete dependency inside `__init__` (write a small example of this "before" version first) so that it instead accepts an abstract interface as a constructor parameter, following the loose-coupling pattern from this lesson.
6. Build a `Team` class that aggregates a list of existing `Player` objects (created independently, before the team), and demonstrate a player being reassigned from one team to another without being recreated.

**Hard**

7. Design an `OrderProcessor` class composed of an abstract `PaymentGateway` and an abstract `NotificationChannel` (reusing the interfaces from Lessons 8 and 9), and demonstrate constructing two different `OrderProcessor` instances with different concrete implementations of each, showing that `OrderProcessor` itself never changes.
8. Take a design that currently uses inheritance inappropriately (write a short "before" example where a `Manager` class inherits from a `Team` class just to access team-related methods, which isn't a genuine "is-a" relationship) and refactor it into composition instead, where `Manager` has a `Team` as an attribute.

## 20. Stretch challenge

Design a small "game character" system using composition throughout, deliberately avoiding inheritance entirely, even where it might be tempting. A `Character` class should be composed of a `Weapon` (abstract interface, with concrete `Sword` and `Bow` implementations), an `Armor` (a plain class holding a defense value), and an `Inventory` (a class managing a list of item names). Write code that assembles several different `Character` instances with different combinations of weapons and armor, and demonstrate swapping a character's weapon at runtime, just by reassigning the composed attribute, something a rigid inheritance-based design would make far more awkward.

## 21. Summary

Composition models "has-a" relationships by having one class hold an instance of another as an attribute and delegate to it, as opposed to inheritance's "is-a" relationships. Composition and aggregation are both "has-a," distinguished by ownership and lifecycle: composition typically creates and owns its contained object, aggregation references something that exists and can persist independently. Composing against abstract interfaces, rather than concrete classes, is what actually delivers loose coupling and testability in practice, and it's frequently, though not universally, the more flexible default choice over inheritance for real-world relationships between classes.

## 22. Additional resources

- [Python official docs: Classes, composition patterns](https://docs.python.org/3/tutorial/classes.html)
- [Gang of Four design principle: "favor composition over inheritance"](https://en.wikipedia.org/wiki/Composition_over_inheritance)
- [Real Python: Composition vs Inheritance](https://realpython.com/inheritance-composition-python/)

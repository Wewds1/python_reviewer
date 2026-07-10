# Lesson 7: Inheritance

## 1. Learning objectives

By the end of this lesson you should be able to:

- Create parent and child classes, and correctly override and extend parent behavior
- Use `super()` properly instead of hardcoding the parent class name
- Explain single, multiple, multilevel, and hierarchical inheritance, with a working example of each
- Explain Method Resolution Order (MRO) and diagnose the diamond problem when it comes up
- Make a genuine judgment call about when inheritance is the right tool and when it isn't

## 2. Prerequisites

Lessons 1 through 6. Inheritance builds directly on classes, constructors, and encapsulation, and it's the lesson where design judgment starts mattering as much as syntax.

## 3. Introduction

Inheritance lets one class take on the attributes and methods of another, then add to or override what it inherited. It's the most iconic OOP feature and also the most commonly misused one; it's genuinely powerful for modeling real "is-a" relationships, and genuinely damaging when reached for out of habit rather than fit. This lesson covers the mechanics thoroughly, and spends real time on when not to use it, which matters just as much.

## 4. Theory

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} makes a sound"

class Dog(Animal):  # Dog inherits from Animal
    def speak(self):  # overriding the parent's method
        return f"{self.name} barks"

generic = Animal("Creature")
rex = Dog("Rex")

print(generic.speak())  # Creature makes a sound
print(rex.speak())      # Rex barks — the overridden version
```

`Dog(Animal)` means `Dog` is a subclass (or child class) of `Animal`, the superclass (or parent class). `Dog` automatically gets everything `Animal` defines, `__init__` included, unless `Dog` explicitly overrides it. Here, `Dog` overrides `speak()` but doesn't touch `__init__`, so it still uses `Animal`'s constructor unchanged.

## 5. Why this concept exists

Many classes share genuine structural and behavioral overlap: a `Dog`, a `Cat`, and a `Bird` are all fundamentally `Animal`s, sharing a name and the general concept of "making a sound," while each also needing its own specific version of that sound. Without inheritance, you'd either duplicate the shared logic across every class, a maintenance liability the moment that shared logic needs to change, or you'd have no clean way to express "this class is fundamentally a specialized version of that one" at all.

## 6. Internal behavior

When Python looks up an attribute or method on an instance, it checks the instance's own `__dict__` first, then walks up the class's inheritance chain, checking each parent class in turn, until it finds a match or runs out of ancestors. That search order is called the Method Resolution Order (MRO), and you can inspect it directly:

```python
print(Dog.__mro__)
# (<class 'Dog'>, <class 'Animal'>, <class 'object'>)
```

Every class in Python ultimately inherits from `object`, even if you don't write that explicitly. For single inheritance, the MRO is simple and linear. For multiple inheritance, Python computes it using an algorithm called C3 linearization, which is where the diamond problem, covered later in this lesson, actually gets resolved rather than causing ambiguity.

## 7. Real-world analogy

Think of a company's job title hierarchy. "Software Engineer" defines certain baseline responsibilities and privileges. "Senior Software Engineer" inherits everything a regular Software Engineer has, and adds more: mentorship duties, higher approval limits. It doesn't redefine what a Software Engineer fundamentally is, it specializes it. If the base "Software Engineer" role gets a new baseline benefit, every specialization automatically inherits it too, without anyone needing to update each senior title individually. That's inheritance working as intended: shared structure defined once, specialized where it genuinely needs to differ.

## 8. Enterprise use cases

A `PaymentMethod` base class with `CreditCard`, `BankTransfer`, and `DigitalWallet` subclasses, each sharing a common interface (`process_payment()`) while implementing the specific mechanics differently, is a textbook enterprise inheritance use case. Exception hierarchies (built extensively in Module 1) are inheritance too: a base `ValidationError` with specific subclasses like `MissingFieldError`, letting calling code catch broadly or narrowly as needed. The common thread in good enterprise uses of inheritance: a genuine, stable "is-a" relationship, not just "these two classes happen to share a few fields right now."

## 9. UML-style explanation

```
                ┌───────────────┐
                │     Animal       │
                ├───────────────┤
                │ - name: str        │
                ├───────────────┤
                │ + speak(): str      │
                └───────┬───────┘
                         │  (inherits from)
           ┌────────────┼────────────┐
           │                          │
   ┌───────▼───────┐         ┌───────▼───────┐
   │      Dog          │         │      Cat          │
   ├───────────────┤         ├───────────────┤
   │ + speak(): str      │         │ + speak(): str      │
   └───────────────┘         └───────────────┘
```

An open-triangle arrow pointing from child to parent is the standard UML notation for inheritance, sometimes described as "is-a." This is the diagram shape you'll be drawing constantly for the rest of this module, and it's worth being able to sketch quickly by hand.

## 10. Syntax

**Single inheritance**, one parent, one child, the most common shape:

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)  # calls Employee's __init__
        self.team_size = team_size
```

`super()` gives you a proxy to the parent class, letting you call its methods without hardcoding the parent's name directly. Using `super().__init__(...)` instead of `Employee.__init__(self, ...)` matters more than it looks like it should, it's covered in Common Mistakes below.

**Multilevel inheritance**, a chain of more than one generation:

```python
class Vehicle:
    def __init__(self, make):
        self.make = make

class Car(Vehicle):
    def __init__(self, make, doors):
        super().__init__(make)
        self.doors = doors

class SportsCar(Car):
    def __init__(self, make, doors, top_speed):
        super().__init__(make, doors)
        self.top_speed = top_speed
```

**Hierarchical inheritance**, multiple children from one shared parent (this is the `Dog`/`Cat` shape from the UML diagram above):

```python
class Shape:
    def area(self):
        raise NotImplementedError

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return 3.14159 * self.radius ** 2

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2
```

**Multiple inheritance**, one child, more than one parent:

```python
class Swimmer:
    def swim(self):
        return "swimming"

class Flyer:
    def fly(self):
        return "flying"

class Duck(Swimmer, Flyer):
    pass

d = Duck()
print(d.swim(), d.fly())  # inherits from both parents
```

## 11. Step-by-step examples

**Easy — overriding a method:**

```python
class Shape:
    def describe(self):
        return "A generic shape"

class Triangle(Shape):
    def describe(self):
        return "A triangle with three sides"

print(Triangle().describe())
```

**Medium — extending, not just replacing, a parent's method using `super()`:**

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def summary(self):
        return f"{self.name}: ${self.salary}"

class Manager(Employee):
    def __init__(self, name, salary, team_size):
        super().__init__(name, salary)
        self.team_size = team_size

    def summary(self):
        base = super().summary()  # reuse the parent's version, then add to it
        return f"{base}, manages {self.team_size} people"

print(Manager("Alice", 90000, 5).summary())
```

`super().summary()` calls the parent's version and builds on top of it, rather than duplicating the formatting logic. This is the pattern to reach for whenever a child's version of a method genuinely extends the parent's behavior rather than replacing it outright.

**Hard — the diamond problem and how MRO resolves it:**

```python
class Base:
    def greet(self):
        return "Hello from Base"

class Left(Base):
    def greet(self):
        return "Hello from Left"

class Right(Base):
    def greet(self):
        return "Hello from Right"

class Diamond(Left, Right):
    pass

d = Diamond()
print(d.greet())              # Hello from Left
print(Diamond.__mro__)
# (Diamond, Left, Right, Base, object)
```

`Diamond` inherits from both `Left` and `Right`, which both inherit from `Base`, the classic diamond shape. Without a clear resolution order, it would be genuinely ambiguous which `greet()` should win. Python's C3 linearization algorithm produces a single, well-defined MRO, `Diamond → Left → Right → Base → object`, and always picks the first match in that order, which is why `Left`'s version wins here specifically because `Left` is listed before `Right` in `class Diamond(Left, Right)`. Swap that order and the result swaps too.

## 12. Common mistakes

**Hardcoding the parent class name instead of using `super()`:**

```python
class Manager(Employee):
    def __init__(self, name, salary, team_size):
        Employee.__init__(self, name, salary)  # works, but fragile
        self.team_size = team_size
```

This works for simple single inheritance, but it breaks down under multiple inheritance, where `super()` correctly follows the MRO and a hardcoded parent name doesn't. Using `super()` consistently, even in simple cases, builds the right habit for when it actually matters.

**Reaching for inheritance to share code between two classes that aren't genuinely related.** If `Car` and `HouseKey` both happen to have a `material` attribute, that's not a reason to give them a shared parent class, there's no real "is-a" relationship there. This is precisely the mistake composition (Lesson 10) is designed to avoid.

**Deep inheritance chains that become hard to reason about.** Four or five levels of inheritance, each adding a small tweak, makes it genuinely difficult to know where a given piece of behavior actually comes from without tracing the whole chain. If you find yourself several levels deep, it's worth asking whether composition would serve better.

**Overriding a method and accidentally breaking the parent's contract**, changing what a method returns or requires in a way that violates what code calling it through the parent type would expect. This is a subtle but real problem covered more formally as the Liskov Substitution Principle in Lesson 11.

## 13. Debugging tips

If a method call is resolving to a version you didn't expect, especially under multiple inheritance, print `ClassName.__mro__` and check the actual resolution order rather than guessing. If `super().__init__(...)` seems to be skipping expected behavior, confirm every class in the chain is correctly calling `super().__init__(...)` itself, a broken link anywhere in the chain can silently skip the classes above it.

## 14. Best practices

Use inheritance only for genuine "is-a" relationships that are stable over time, not for convenience code sharing. Always use `super()` rather than hardcoding parent class names. Keep inheritance chains shallow, two or three levels at most in typical application code; anything deeper is worth a second look. When overriding a method, make sure the overridden version still honors what callers reasonably expect from the parent's version, don't quietly change the contract.

## 15. Performance considerations

Method resolution through an inheritance chain has a small, real cost, Python has to walk up the MRO to find a method that isn't defined directly on the instance's own class, though this cost is negligible for any normal chain depth. This becomes a genuine concern only in extremely deep or wide multiple-inheritance hierarchies, which is yet another reason to keep inheritance structures shallow and deliberate.

## 16. Code style

Always call `super().__init__(...)` as the first line of a child's `__init__`, unless you have a specific, deliberate reason not to, so the parent's setup completes before the child adds its own. Keep multiple inheritance rare and well-documented when it's genuinely necessary; it's a powerful tool that reads poorly if used casually.

## 17. Interview questions with model answers

**Q: What's the difference between method overriding and method overloading, and does Python support both?**

Overriding is redefining a method in a subclass to provide a specialized version of behavior the parent already defines, and Python fully supports this, it's central to how inheritance works. Overloading is defining multiple versions of the same method name with different parameter signatures within the same class, which Python does not support in the traditional sense (Lesson 5 covers the idiomatic alternatives: default arguments and `*args`/`**kwargs`).

**Q: Explain the diamond problem and how Python resolves it.**

The diamond problem arises when a class inherits from two parent classes that both inherit from a common ancestor, creating ambiguity about which version of an inherited method should apply if both parents override it differently. Python resolves this deterministically using C3 linearization to compute a single Method Resolution Order, and whichever class appears first in that order, generally the leftmost path in the inheritance declaration, wins. A strong answer can walk through a concrete `class Diamond(Left, Right)` example and correctly predict which method executes.

**Q: When should you avoid inheritance?**

When the relationship between two classes isn't a genuine "is-a" relationship, when it would create a deep or fragile hierarchy that's hard to reason about, or when you just want to reuse some code without there being any real conceptual specialization happening. In those cases, composition, giving a class an instance of another class as an attribute rather than inheriting from it, is usually the better, more flexible choice, which Lesson 10 covers in depth.

## 18. Knowledge check

1. What does `super()` do, and why is it preferred over calling the parent class directly by name?
2. What's the difference between multilevel and hierarchical inheritance?
3. In `class Diamond(Left, Right)`, if both `Left` and `Right` override a method from a shared `Base`, which version does `Diamond` use, and why?
4. Name one situation where composition would be a better choice than inheritance.

## 19. Hands-on exercises

**Easy**

1. Create a `Vehicle` base class with a `describe()` method, and a `Motorcycle` subclass that overrides it.
2. Create a `Bird` base class and two subclasses, `Sparrow` and `Penguin`, where `Penguin` overrides a `fly()` method to reflect that penguins can't fly, instead of inheriting a nonsensical default.
3. Print the `__mro__` of a simple two-level single-inheritance class and explain each entry in a comment.

**Medium**

4. Build a three-level multilevel inheritance chain (`LivingThing` → `Animal` → `Dog`), where each level adds at least one new attribute via `super().__init__()`, and demonstrate a `Dog` instance has access to attributes from all three levels.
5. Build a hierarchical inheritance example with a `PaymentMethod` base class and at least two subclasses (`CreditCard`, `BankTransfer`), each implementing a `process()` method differently, and write a loop that processes a list containing both types uniformly.
6. Deliberately construct a diamond inheritance scenario with a `Base`, two children, and one grandchild inheriting from both children, print the MRO, and explain in a comment exactly why the resolution order is what it is.

**Hard**

7. Build a small exception hierarchy (a base `AppError`, with `ValidationError` and `AuthError` subclasses) and demonstrate catching a specific subclass separately from catching the shared base class, tying Lesson 7's inheritance directly back to Module 1's exception handling.
8. Take the `Shape`/`Circle`/`Square` hierarchical inheritance example from this lesson, add a `Triangle` subclass, and write a function that accepts a list of mixed `Shape` subclass instances and returns the one with the largest area, without needing to know which specific subclass each one is, this is a preview of polymorphism, which is the entire subject of the next lesson.

## 20. Stretch challenge

Design a small multiple inheritance scenario that's genuinely justified, not contrived: for example, a `Loggable` mixin class (a mixin is a class designed specifically to be combined with others, not to stand alone) providing a `log(message)` method, combined with a `Serializable` mixin providing a `to_dict()` method, both mixed into a real `Order` class alongside its own base behavior. Write out, in a short comment, why this multiple-inheritance use case is more defensible than the "two unrelated classes happen to share a field" anti-pattern warned against earlier in this lesson, and what specifically makes a mixin different from a normal parent class in intent.

## 21. Summary

Inheritance lets a subclass take on a parent's attributes and methods, then override or extend them, and it's the right tool specifically for genuine, stable "is-a" relationships. `super()` is how you correctly call up the inheritance chain without hardcoding parent class names, which matters even more once multiple inheritance and MRO enter the picture. The diamond problem, which sounds alarming in the abstract, is fully and deterministically resolved by Python's MRO, computable and inspectable at any time via `ClassName.__mro__`. The real skill this lesson is building isn't just the syntax, it's recognizing when inheritance is the right call and when composition, covered in Lesson 10, would serve the same goal without the same long-term fragility.

## 22. Additional resources

- [Python official docs: Inheritance](https://docs.python.org/3/tutorial/classes.html#inheritance)
- [Python official docs: super()](https://docs.python.org/3/library/functions.html#super)
- [Python official docs: Method Resolution Order (C3 linearization)](https://docs.python.org/3/howto/mro.html)

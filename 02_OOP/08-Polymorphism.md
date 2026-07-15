# Lesson 8: Polymorphism

## 1. Learning objectives

By the end of this lesson you should be able to:

- Explain polymorphism precisely, and distinguish it clearly from inheritance itself
- Use duck typing correctly, and explain why Python leans on it so heavily
- Write code that treats different object types uniformly through a shared interface
- Overload operators using magic methods, and know which ones are worth implementing
- Recognize why polymorphism is what actually makes inheritance hierarchies useful, not just structurally tidy

## 2. Prerequisites

Lessons 1 through 7, especially Inheritance. Polymorphism is the payoff for building a proper inheritance hierarchy, so you need the hierarchy mechanics solid first.

## 3. Introduction

You already wrote a small taste of this at the end of the Inheritance lesson's exercises: a function that could compute the area of a `Circle`, a `Square`, or a `Triangle` without needing to know which one it was actually holding. That's polymorphism, the ability for different types to respond to the same interface in their own way, and it's arguably the actual point of building an inheritance hierarchy in the first place. Inheritance without polymorphism is just code reuse. Polymorphism is what makes that hierarchy genuinely useful to the rest of your program.

## 4. Theory

Polymorphism, literally "many forms," means the same operation behaves differently depending on the type of object it's performed on, without the calling code needing to know or check which specific type it's dealing with.

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

shapes = [Circle(3), Square(4)]
for shape in shapes:
    print(shape.area())  # calls the correct version for each object automatically
```

The loop never checks `if isinstance(shape, Circle)`. It just calls `.area()` and trusts that whatever object it's holding knows how to answer that call correctly, on its own terms.

## 5. Why this concept exists

Without polymorphism, code that needs to work with multiple related types would be full of explicit type checks, `if isinstance(x, Circle): ... elif isinstance(x, Square): ...`, which grows more fragile and more repetitive every time a new type gets added, since every one of those scattered checks has to be found and updated. Polymorphism inverts that: each type is responsible for correctly implementing the shared behavior itself, and calling code stays completely unaware of, and unaffected by, how many types exist or what gets added later.

## 6. Internal behavior

When you call `shape.area()`, Python doesn't check the type of `shape` against a list of known cases at all. It looks up `area` starting on `shape`'s own class, walking up the MRO exactly as covered in Lesson 7, and calls whatever it finds first. There's no special polymorphism mechanism separate from ordinary method lookup, polymorphism in Python is really just a natural consequence of dynamic typing combined with method overriding: the interpreter doesn't need to know in advance what type an object is to call a method on it, it just needs the object to actually have that method.

## 7. Real-world analogy

Think of a universal remote's "power" button. Point it at a TV, and pressing power turns the TV on or off. Point it at a sound system, and the exact same button press turns the sound system on or off instead. The button doesn't need to know, and doesn't care, which specific device it's pointed at; it sends the same signal, and each device is responsible for correctly interpreting "power" in its own way. That's polymorphism: one interface, many device-specific implementations, and the remote never needs a special case for each brand.

## 8. Enterprise use cases

A payment processing system handling `CreditCard`, `BankTransfer`, and `DigitalWallet` objects can loop over a list of mixed payment methods and call `.process()` on each, with no branching logic checking which type it's handling, exactly the shape from Lesson 7's exercises. Report generation systems commonly do the same with different `ReportFormat` types (PDF, CSV, HTML), each implementing `.export()` differently. This pattern is precisely what makes it possible to add a brand new payment method or export format later without touching a single line of the existing processing loop, which is often the single biggest practical win OOP offers in a growing enterprise codebase.

## 9. UML-style explanation

```
                ┌─────────────────┐
                │      Shape          │
                ├─────────────────┤
                │ + area(): float       │  ← abstract-ish, no real implementation
                └────────┬────────┘
                          │
           ┌──────────────┼──────────────┐
           │                              │
   ┌───────▼───────┐             ┌───────▼───────┐
   │     Circle         │             │     Square         │
   ├───────────────┤             ├───────────────┤
   │ + area(): float      │             │ + area(): float      │
   └───────────────┘             └───────────────┘

        client code ──► calls shape.area() on any Shape, uniformly
```

The UML shape here looks identical to Lesson 7's hierarchical inheritance diagram, and that's the point: polymorphism isn't a different structure, it's what you get to do with the structure inheritance already built.

## 10. Syntax

**Duck typing**, Python's real day-to-day style of polymorphism, which doesn't require a shared base class at all:

```python
class Duck:
    def sound(self):
        return "Quack"

class Dog:
    def sound(self):
        return "Woof"

def make_it_speak(animal):
    print(animal.sound())  # works on anything with a .sound() method, no shared parent required

make_it_speak(Duck())
make_it_speak(Dog())
```

The phrase "duck typing" comes from "if it walks like a duck and quacks like a duck, it's a duck": `make_it_speak` doesn't care whether its argument is officially an `Animal` subclass, it only cares that the object has a `.sound()` method it can call. This is a genuinely different mindset from languages that require formal interface declarations, and it's central to how idiomatic Python is written.

**Operator overloading via magic methods**, first introduced briefly in Lesson 5:

```python
class Money:
    def __init__(self, amount):
        self.amount = amount

    def __add__(self, other):     # defines what + means for two Money objects
        return Money(self.amount + other.amount)

    def __str__(self):
        return f"${self.amount:.2f}"

    def __lt__(self, other):      # defines what < means
        return self.amount < other.amount

a = Money(10)
b = Money(15)
print(a + b)        # $25.00 — + now works because __add__ is defined
print(a < b)         # True — < now works because __lt__ is defined
```

Common magic methods worth knowing: `__add__` (`+`), `__eq__` (`==`), `__lt__` (`<`), `__len__` (`len()`), `__str__` (`str()`/`print()`), `__repr__` (unambiguous developer-facing representation, shown in a REPL or inside a list). Implementing these is how your own classes plug into Python's built-in syntax, rather than needing custom method names for every operation.

## 11. Step-by-step examples

**Easy — duck typing across genuinely unrelated classes:**

```python
class PDFExporter:
    def export(self):
        return "Exporting as PDF"

class CSVExporter:
    def export(self):
        return "Exporting as CSV"

for exporter in [PDFExporter(), CSVExporter()]:
    print(exporter.export())
```

**Medium — polymorphism through a proper inheritance hierarchy with method overriding:**

```python
class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def calculate_pay(self):
        return self.base_salary

class SalesEmployee(Employee):
    def __init__(self, name, base_salary, commission):
        super().__init__(name, base_salary)
        self.commission = commission

    def calculate_pay(self):
        return self.base_salary + self.commission

employees = [Employee("Alex", 50000), SalesEmployee("Sam", 40000, 15000)]
for emp in employees:
    print(f"{emp.name}: {emp.calculate_pay()}")
```

**Hard — operator overloading combined with polymorphic behavior in a single, realistic example:**

```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

    def __len__(self):
        return int((self.x ** 2 + self.y ** 2) ** 0.5)  # magnitude, truncated to an int

v1 = Vector(1, 2)
v2 = Vector(3, 4)
print(v1 + v2)          # Vector(4, 6) — uses __add__ and __repr__ together
print(v1 == Vector(1, 2))  # True — uses __eq__
print(len(Vector(3, 4)))    # 5 — uses __len__
```

## 12. Common mistakes

**Writing explicit `isinstance()` checks where polymorphism should be doing the work instead:**

```python
def process(item):
    if isinstance(item, Circle):
        return item.radius ** 2 * 3.14159
    elif isinstance(item, Square):
        return item.side ** 2
    # every new shape means another elif here
```

This defeats the entire purpose of building a shared interface. The fix is giving every shape its own correctly implemented `.area()` and calling it uniformly, exactly as shown throughout this lesson.

**Implementing `__eq__` without also implementing `__hash__`,** or vice versa inconsistently, which can produce objects that behave strangely when used in sets or as dictionary keys. If a class defines `__eq__`, and you also need instances to be hashable, `__hash__` needs to be defined consistently with it.

**Overloading operators in ways that don't match their conventional meaning.** Defining `__add__` to do something unrelated to addition, like triggering a database write, makes code that uses `+` deeply confusing to anyone reading it. Operator overloading should make code more intuitive, not less.

## 13. Debugging tips

If polymorphic behavior isn't working as expected, some objects seem to be using the wrong version of a method, check the actual MRO with `ClassName.__mro__` and confirm the method is genuinely overridden where you think it is, rather than accidentally inherited unchanged from a level higher up. If an operator like `+` raises a `TypeError` on your custom objects, the relevant magic method (`__add__`, in that case) either isn't defined or is returning something inconsistent with what the calling code expects.

## 14. Best practices

Favor polymorphism (a shared method each type implements correctly) over branching type checks whenever you're handling multiple related types uniformly. Use duck typing freely in idiomatic Python code, you don't need a formal shared base class just to treat two unrelated objects the same way, as long as they both expose the method you need. Only overload operators when the operation has an intuitive, conventional meaning for your class; don't overload `+` or `<` just because you technically can.

## 15. Performance considerations

Polymorphic method calls have effectively the same cost as any other method call in Python, there's no meaningful performance penalty for using polymorphism over manual type checking, and the resulting code is almost always more maintainable. This is a case where the "correct" design choice and the "fast" one are the same choice.

## 16. Code style

Keep overridden methods consistent with the parent's expected behavior and return type; a method that returns a number in the parent class shouldn't suddenly return a string in a subclass, since that breaks any code written to work polymorphically across the hierarchy. Implement `__repr__` on custom classes even when you don't strictly need `__str__`, since it makes debugging in a REPL or a debugger significantly easier.

## 17. Interview questions with model answers

**Q: What's the difference between inheritance and polymorphism?**

Inheritance is the structural relationship, a subclass taking on a parent's attributes and methods. Polymorphism is the behavioral payoff of that structure: the ability to call the same method on objects of different types and have each one respond correctly according to its own implementation, without the calling code needing to know which specific type it's dealing with. A strong answer makes clear that you can technically have inheritance without meaningfully using polymorphism, but polymorphism is what actually makes an inheritance hierarchy useful in practice.

**Q: What is duck typing, and why does Python rely on it so heavily?**

Duck typing means an object's suitability for an operation is determined by whether it has the right methods and attributes, not by its declared type or class hierarchy. Python leans on this because it's dynamically typed, there's no compiler enforcing a formal interface, so "does this object have a `.sound()` method" is checked at the moment it's actually called, not verified in advance. This gives Python significant flexibility, at the cost of catching a type mismatch only at runtime instead of ahead of time.

**Q: Give an example of operator overloading and explain why you'd implement it.**

A `Vector` or `Money` class implementing `__add__` so that `v1 + v2` behaves intuitively, exactly like `Vector` and `Money` in this lesson's examples, is a strong concrete answer. The interviewer is checking that you understand this makes calling code read naturally, `total = v1 + v2` instead of `total = v1.add(v2)`, while also understanding that overloading should only be used when the operator's conventional meaning genuinely applies.

## 18. Knowledge check

1. What's the practical difference between inheritance and polymorphism?
2. What is duck typing, and does it require a shared base class?
3. Which magic method controls what `+` does for a custom class?
4. Why is a long `isinstance()`/`elif` chain often a sign that polymorphism should be used instead?

## 19. Hands-on exercises

**Easy**

1. Create two unrelated classes, each with a `.describe()` method, and write a function that calls `.describe()` on either without checking their type, demonstrating duck typing.
2. Implement `__str__` on a `Book` class so that `print(my_book)` shows a nicely formatted title and author.
3. Create a small `Shape` hierarchy (reusing earlier lessons' examples is fine) and loop over a mixed list of shapes, calling `.area()` on each polymorphically.

**Medium**

4. Implement `__eq__` and `__lt__` on a `Money` class so that two `Money` objects can be compared directly with `==` and `<`, and sort a list of `Money` objects using the built-in `sorted()`.
5. Build a small `NotificationSender` set of classes (`EmailSender`, `SMSSender`), each with a `.send(message)` method, and write a function that accepts a list of mixed senders and calls `.send()` on each uniformly.
6. Implement `__add__` and `__repr__` on a `Vector` class (following this lesson's example), and demonstrate combining three separate vectors using `+` in a single expression.

**Hard**

7. Take the `PaymentMethod` hierarchy idea from the Enterprise Use Cases section and build it out fully, a base class and at least three subclasses, each with its own `.process(amount)` implementation, then write a function that processes a mixed list of payment methods and returns a total, entirely polymorphically.
8. Implement `__eq__` and `__hash__` consistently on a `Point` class (with `x` and `y` attributes) so that `Point` objects can be correctly used as elements of a `set`, and demonstrate that two separately created points with the same coordinates are correctly treated as duplicates when added to a set.

## 20. Stretch challenge

Design a small "plugin" style system: a base `Command` class with an `execute()` method that raises `NotImplementedError`, and at least three concrete command subclasses (for example, `CreateFileCommand`, `DeleteFileCommand`, `RenameFileCommand`), each implementing `execute()` differently. Write a `CommandRunner` that accepts a list of `Command` objects and runs them in sequence, entirely polymorphically, with no type checks anywhere in the runner. Then add a brand new command type without modifying `CommandRunner` at all, and confirm it slots in and works correctly. That last step, adding new behavior without touching existing, already-tested code, is the concrete payoff polymorphism is actually for.

## 21. Summary

Polymorphism is what makes an inheritance hierarchy, or even a loose collection of unrelated classes sharing a method name via duck typing, actually useful: calling code can treat different types uniformly and trust each one to behave correctly on its own terms. Python leans heavily on duck typing rather than requiring formal interfaces, which is a deliberate design philosophy, not a missing feature. Operator overloading via magic methods extends this same idea to Python's own built-in syntax, letting your classes feel like native, first-class citizens of the language rather than bolted-on data structures.

## 22. Additional resources

- [Python official docs: Data model, special method names](https://docs.python.org/3/reference/datamodel.html#special-method-names)
- [Python glossary: duck-typing](https://docs.python.org/3/glossary.html#term-duck-typing)
- [Real Python: Operator and Function Overloading in Custom Python Classes](https://realpython.com/operator-function-overloading/)

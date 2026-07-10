# Lesson 2: Classes and Objects

## 1. Learning objectives

By the end of this lesson you should be able to:

- Define a class and instantiate multiple independent objects from it
- Explain what `self` actually is, not just where to put it
- Distinguish object identity from object equality, and know which operator checks which
- Describe, roughly, what happens in memory when an object is created
- Design a class with a clear, single responsibility

## 2. Prerequisites

Lesson 1. You need the conceptual "class is a blueprint, object is a specific instance" framing before the mechanics here will click.

## 3. Introduction

This is where the concept from Lesson 1 becomes real code. You'll define your first proper classes, create multiple objects from the same class, and start noticing something that trips up almost everyone early on: two objects can look identical on the outside and still be two completely separate things underneath. Getting comfortable with that distinction now saves you from a specific category of confusing bug later.

## 4. Theory

A class definition describes what every object built from it will have: what attributes it starts with, and what methods it can call. Defining the class doesn't create any objects by itself, it just registers the blueprint.

```python
class Book:
    def __init__(self, title, author):
        self.title = title
        self.author = author

    def describe(self):
        return f"{self.title} by {self.author}"
```

Calling `Book("Dune", "Frank Herbert")` creates one specific object: a new, independent chunk of memory holding its own `title` and `author`, linked back to the `Book` class so it knows where to find `describe()`. Call it again with different arguments, and you get a second, entirely separate object. Neither one knows the other exists.

```python
book1 = Book("Dune", "Frank Herbert")
book2 = Book("1984", "George Orwell")
print(book1.describe())  # Dune by Frank Herbert
print(book2.describe())  # 1984 by George Orwell
```

## 5. Why this concept exists

Without a way to stamp out multiple independent instances of the same structure, you'd be back to manually managing separate dictionaries or variables for every book, every account, every customer, with no guarantee they all had a consistent shape or consistent behavior. Classes give you that guarantee for free: every `Book` object is built the same way and offers the same methods, no matter how many you create.

## 6. Internal behavior

When Python executes `Book("Dune", "Frank Herbert")`, it does two things in sequence. First, it calls a special method, `__new__`, which allocates a new, empty object in memory (you'll rarely touch `__new__` directly in this module, but it's worth knowing it's there, underneath `__init__`). Second, it calls `__init__` on that freshly created object, passing in the arguments you provided, which is where `self.title = title` actually happens, populating that specific object's own attribute dictionary.

`self` is simply the name, by convention, not by hard rule, for the parameter that refers to the specific object a method was called on. When you write `book1.describe()`, Python actually calls `Book.describe(book1)` behind the scenes; `self` inside `describe` is just `book1`. This is why every instance method needs `self` as its first parameter: it's how the method knows which object's data it's supposed to be working with.

## 7. Real-world analogy

Think of a class as a cookie cutter, and each object as an actual cookie. The cutter defines the shape, every cookie made from it has that same outline, but each cookie is its own physical thing. Frost one blue, and the others stay plain. They came from the same cutter, but they don't share a physical form once they're made. `self`, in this analogy, is just "this particular cookie," the one currently being decorated, as opposed to any of the others sitting on the tray.

## 8. Enterprise use cases

Any system managing a collection of similar entities, customer accounts, product listings, support tickets, creates many independent objects from the same class definition. A customer service platform might instantiate a `Ticket` object for every incoming support request; each one is independent, has its own status and history, and yet they all share exactly the same set of behaviors (assign, escalate, close) because they all come from the same `Ticket` class. That consistency, guaranteed by the class definition, is what lets a team build reliable tooling on top of "every ticket behaves the same way," even as the number of tickets grows into the millions.

## 9. UML-style explanation

```
┌───────────────────────────┐
│           Book              │
├───────────────────────────┤
│ - title: str                 │
│ - author: str                 │
├───────────────────────────┤
│ + describe(): str             │
└───────────────────────────┘

book1: Book ──────► { title: "Dune", author: "Frank Herbert" }
book2: Book ──────► { title: "1984", author: "George Orwell" }
```

One class box describes the shape. Two separate object instances, each with their own data, both conform to that shape. This is the visual version of "the class is the blueprint, the objects are the houses."

## 10. Syntax

```python
class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def age(self, current_year):
        return current_year - self.year

my_car = Car("Toyota", "Corolla", 2019)
print(my_car.age(2026))  # 7
```

Object identity versus equality:

```python
car_a = Car("Toyota", "Corolla", 2019)
car_b = Car("Toyota", "Corolla", 2019)
car_c = car_a

print(car_a == car_b)  # False by default — different objects, even with identical data
print(car_a is car_b)  # False — genuinely different objects in memory
print(car_a is car_c)  # True — car_c is just another name for the same object
```

That `car_a == car_b` result surprises almost everyone the first time. By default, Python compares objects by identity unless a class explicitly defines what equality should mean, which is a topic Lesson 8 (Polymorphism) picks up when it covers the `__eq__` magic method.

## 11. Step-by-step examples

**Easy — creating and using a simple object:**

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

p = Point(3, 4)
print(p.x, p.y)
```

**Medium — multiple independent objects from one class:**

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def give_raise(self, amount):
        self.salary += amount

alice = Employee("Alice", 65000)
bob = Employee("Bob", 58000)

alice.give_raise(5000)
print(alice.salary, bob.salary)  # 70000 58000 — bob is completely unaffected
```

**Hard — demonstrating that `self` is just a name for whichever object called the method:**

```python
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count += 1

a = Counter()
b = Counter()

a.increment()
a.increment()
b.increment()

print(a.count, b.count)  # 2 1
print(Counter.increment(a))  # calling it the "unbound" way, explicitly passing self
print(a.count)  # 3 — same effect as a.increment()
```

That last pair of lines is worth sitting with. `a.increment()` and `Counter.increment(a)` do exactly the same thing; the dot-call syntax is just Python automatically filling in `self` with `a` for you.

## 12. Common mistakes

**Forgetting `self` as the first parameter of an instance method:**

```python
class Broken:
    def greet():  # missing self
        return "hi"

Broken().greet()  # TypeError: greet() takes 0 positional arguments but 1 was given
```

Python still passes the calling object in automatically; if there's no parameter to catch it, you get an argument count mismatch.

**Assuming `==` compares data by default.** As shown above, two objects with identical attribute values are not equal unless the class defines `__eq__`. Assuming otherwise leads to bugs that look like "why doesn't this comparison work," especially when checking whether an object is already in a list.

**Mutating one object and being surprised a "different" one changed too,** which usually means both names actually point at the same object (see Lesson 1's variable-binding model from Module 1), not two independent ones.

## 13. Debugging tips

If a comparison between two seemingly identical objects returns `False` unexpectedly, check whether the class defines `__eq__`; if it doesn't, Python is comparing identity, not data, and that's almost certainly the source of the confusion. If a method call raises a "takes N positional arguments but M was given" error, check first whether `self` is missing from the method's parameter list.

## 14. Best practices

Keep `__init__` focused on setting up initial state, not performing heavy computation or I/O; a constructor that reaches out to a database or a file on every instantiation is a common source of hard-to-test code. Give every class a clear, narrow purpose that you can state in one sentence. Use `is` only when you genuinely mean identity (most often, checking against `None`), and `==` for everything else.

## 15. Performance considerations

Creating an object has a small, real cost: Python allocates memory for its instance dictionary and links it to the class. For most backend code this is completely negligible. It matters if you're creating enormous numbers of small objects in a tight loop, millions of them, where the cumulative overhead becomes measurable; at that point, `__slots__` or reconsidering whether you need full objects at all (a plain tuple or dictionary might do) becomes worth investigating, but that's well beyond the scale of anything in this module.

## 16. Code style

`self` should always be named `self`, never something else, even though Python doesn't technically enforce it; every experienced Python developer expects it, and naming it anything else will actively confuse readers. Keep `__init__` parameters in a sensible, predictable order, and match attribute names to parameter names where there's no reason for them to differ (`self.title = title`, not `self.title = t`).

## 17. Interview questions with model answers

**Q: What is `self`, really?**

`self` is simply the parameter that refers to the specific instance a method was called on. When you write `obj.method()`, Python translates that internally to `ClassName.method(obj)`, so `self` inside the method body is just another name for `obj`. It's a naming convention, not a keyword, but deviating from it will confuse anyone reading your code.

**Q: Why does `obj1 == obj2` return `False` for two objects with identical attribute values?**

By default, Python's `==` operator on custom objects falls back to identity comparison, the same thing `is` checks, unless the class explicitly overrides `__eq__` to define what equality should mean for that type of object. Without that override, two separately created objects are never equal, no matter how similar their data looks.

**Q: What actually happens in memory when you instantiate a class?**

A strong answer covers that Python allocates a new object with its own attribute storage, links it back to the class so it can find shared methods, and then runs `__init__` on that new object to populate its initial state. Every instance gets independent storage for its attributes, but all instances share the exact same method code, defined once on the class, not copied per instance.

## 18. Knowledge check

1. What's the difference between `is` and `==` for two custom objects, by default?
2. What does `self` actually refer to inside a method?
3. If you create two objects from the same class with identical constructor arguments, are they the same object? Why or why not?
4. What error do you get if you forget `self` as a method's first parameter, and why?

## 19. Hands-on exercises

**Easy**

1. Write a `Dog` class with `name` and `breed` attributes and a method `bark()` that returns a string including the dog's name.
2. Create two `Dog` objects with different names, call `bark()` on each, and print both results.
3. Demonstrate, with code, that two `Dog` objects with the same name and breed are not equal by default.

**Medium**

4. Write a `BankAccount` class with a `balance` attribute and `deposit`/`withdraw` methods, then create two separate accounts and show that operations on one don't affect the other.
5. Write a short script that assigns an existing object to a second variable name, mutates it through the second name, and shows the change is visible through the first name too, then explain why in a comment.
6. Write a class `Rectangle` with `width` and `height`, and a method `area()`. Create three rectangles and print which one has the largest area.

**Hard**

7. Write a `Playlist` class that holds a list of song titles as an attribute, with methods to add a song, remove a song, and return the total count. Create two separate playlists, add different songs to each, and confirm they don't interfere with each other.
8. Implement `__eq__` on a `Point` class (with `x` and `y` attributes) so that two `Point` objects with the same coordinates are considered equal, then demonstrate that `==` now returns `True` for two separately created points with matching coordinates, while `is` still returns `False`.

## 20. Stretch challenge

Write a `Fleet` class that manages a list of `Car` objects (reuse the `Car` class from this lesson). Give `Fleet` a method `add_car(car)`, a method `total_value()` that sums a `value` attribute across every car in the fleet, and a method `oldest_car()` that returns whichever car has the smallest `year`. This exercise is really about one class managing a collection of objects built from a different class, which is an extremely common shape in real backend code, and it's worth noticing that shape now, before Lesson 10 (Composition) names it formally.

## 21. Summary

A class defines a shape; an object is one specific instance of that shape, with its own independent data. `self` is just a name for whichever object a method was called on, filled in automatically by Python's dot-call syntax. Identity (`is`) and equality (`==`) are different checks, and by default, Python's equality check for custom objects is actually an identity check in disguise, until a class says otherwise. Every idea in the rest of this module builds directly on getting this distinction solid.

## 22. Additional resources

- [Python official docs: Classes](https://docs.python.org/3/tutorial/classes.html)
- [Python official docs: Special method names (`__init__`, `__eq__`, and others)](https://docs.python.org/3/reference/datamodel.html#special-method-names)
- [Python official docs: `is` operator and identity](https://docs.python.org/3/reference/expressions.html#is)

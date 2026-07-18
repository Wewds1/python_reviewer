# Module 2 Assessment

Same rule as Module 1's exam: work through this without your notes open first, then check yourself. This one adds a section Module 1 didn't need, class design exercises, since design judgment is the actual subject of this module, not just syntax recall.

---

## Section A: Multiple choice (50 questions)

1. What keyword is used to define a class in Python?
A) class B) def C) struct D) object

2. What does `self` refer to inside an instance method?
A) the class itself B) the specific instance the method was called on C) nothing, it's optional D) the parent class

3. Which of these correctly creates an object from a class `Car`?
A) `Car.new()` B) `new Car()` C) `Car()` D) `create Car()`

4. What is `__init__` primarily responsible for?
A) destroying an object B) initializing a new object's state C) comparing two objects D) printing an object

5. What does a class attribute have that an instance attribute doesn't?
A) it's shared across every instance unless shadowed B) it can't be changed C) it's always private D) it requires `@staticmethod`

6. What happens if you assign `self.attribute = value` for an attribute that started as a class attribute?
A) it changes the class attribute for every instance B) it raises an error C) it creates a new instance attribute, shadowing the class one D) nothing happens

7. Which decorator marks a method as not requiring `self` or `cls`?
A) `@classmethod` B) `@staticmethod` C) `@property` D) `@abstractmethod`

8. What does `cls` refer to inside a class method?
A) the specific instance B) the class itself C) the parent class only D) nothing

9. Which of the following correctly demonstrates method overriding?
A) defining `__init__` twice in one class B) a subclass redefining a method the parent also defines C) calling a method twice D) using `*args`

10. What is name mangling?
A) renaming a class B) Python's mechanism for making double-underscore attributes harder to access from outside the class C) a way to rename variables automatically D) a debugging tool

11. Which of these is the correct way to define a read-only property?
A) `@property` with no corresponding setter B) `@readonly` C) `def get_value(self):` D) `self.__value = value`

12. What does `super()` return?
A) a copy of the current object B) a proxy that lets you access the parent class's methods C) the class name as a string D) nothing, it's a keyword

13. In `class Dog(Animal):`, what is `Animal`?
A) an instance B) the parent (super) class C) an abstract method D) a decorator

14. What is the Method Resolution Order (MRO)?
A) the order methods are defined in a file B) the order Python searches classes when resolving an attribute or method C) the order objects are created D) the order exceptions are raised

15. Which of these best describes duck typing?
A) requiring a formal interface before calling a method B) an object's suitability being judged by whether it has the right methods, not its declared type C) a type of inheritance D) a Python syntax error

16. What decorator is required to make a class method act as an alternate constructor?
A) `@staticmethod` B) `@classmethod` C) `@abstractmethod` D) `@constructor`

17. Which magic method controls what happens when you use `+` on two custom objects?
A) `__plus__` B) `__sum__` C) `__add__` D) `__combine__`

18. What does the `abc` module's `ABC` class provide?
A) automatic method implementations B) enforcement that abstract methods must be implemented before instantiation C) faster performance D) automatic getters and setters

19. What happens if you try to instantiate a class with an unimplemented `@abstractmethod`?
A) it works, but the method returns None B) `TypeError` is raised C) a warning is printed D) nothing, Python ignores it

20. What best describes a "has-a" relationship?
A) inheritance B) composition C) polymorphism D) encapsulation

21. What's the key difference between composition and aggregation?
A) there is no difference B) ownership and lifecycle of the contained object C) aggregation is faster D) composition doesn't allow methods

22. Which of these is an example of multiple inheritance?
A) `class B(A):` B) `class C(A, B):` C) `class D(C(A)):` D) `class E(): pass`

23. In the diamond problem, what resolves which method actually gets called?
A) alphabetical order of class names B) the order classes were imported C) Python's MRO, computed via C3 linearization D) random selection

24. What does the Single Responsibility Principle state?
A) a class should have only one method B) a class should have only one attribute C) a class should have only one reason to change D) a class should never inherit from another

25. What does the Open/Closed Principle state?
A) classes should be open source B) classes should be open for extension, closed for modification C) all attributes should be public D) all methods should be private

26. Which of these is the best example of high cohesion?
A) a class handling five unrelated responsibilities B) a class focused on one clear responsibility C) a class with no methods D) a class with only static methods

27. What does tight coupling between two classes typically mean?
A) they're both abstract B) changing one frequently forces changes in the other C) they share a common ancestor D) they can't be tested

28. Which of these correctly defines an abstract method?
A) `def method(self): pass` inside a normal class B) `@abstractmethod` decorator inside a class inheriting from `ABC` C) `def __abstract_method__(self):` D) leaving a method undefined entirely

29. What is a mixin class typically used for?
A) as a standalone, independently instantiated class B) to be combined with other classes via multiple inheritance, adding a specific piece of reusable behavior C) to replace `__init__` D) to store class-level constants only

30. What's the output of comparing two separately created objects of the same class with `==`, if `__eq__` isn't defined?
A) always True B) always False, since it defaults to identity comparison C) raises an error D) compares all attributes automatically

31. Which is the correct syntax for a property setter?
A) `@property.setter` B) `@attributename.setter` where `attributename` matches the getter's name C) `@setter` D) `def set_attributename(self, value):`

32. What's the primary benefit of encapsulation?
A) faster code execution B) letting a class enforce its own rules by controlling access to its internal state C) automatic documentation D) removing the need for constructors

33. Which of these is a genuine "is-a" relationship?
A) Car has-a Engine B) SavingsAccount is-a Account C) Order has-a LineItem D) Team has-a Player

34. What does `Class.__mro__` return?
A) a list of every instance created B) a tuple showing the method resolution order C) a dictionary of all attributes D) the class's docstring

35. Which principle suggests favoring "has-a" over "is-a" relationships by default?
A) Single Responsibility Principle B) Open/Closed Principle C) Favor composition over inheritance D) Liskov Substitution Principle

36. What happens when a subclass doesn't override a parent method?
A) it raises an error B) it inherits and uses the parent's version unchanged C) the method is deleted D) it must be redefined manually

37. Which of these correctly demonstrates polymorphism?
A) two unrelated classes with completely different method names B) calling the same method name on different object types and getting type-appropriate behavior for each C) using `isinstance()` checks everywhere D) defining a method twice in the same class

38. What's the primary purpose of a UML class diagram's `-` and `+` prefixes?
A) mathematical operations B) indicating private and public visibility C) marking abstract vs concrete classes D) showing inheritance direction

39. Which of these would most likely cause the mutable class attribute bug?
A) `self.items = []` inside `__init__` B) `items = []` as a class attribute, then `.append()` through an instance C) using a tuple as a class attribute D) using `@property`

40. What does `@abstractmethod` do if the class doesn't also inherit from `ABC` (or use `ABCMeta`)?
A) it still enforces the requirement B) it has no enforcement effect at all C) it raises an error immediately D) it's a syntax error

41. In `class Diamond(Left, Right):`, if both parents override the same method, which one wins by default?
A) Right, always B) Left, because it's listed first, per MRO C) whichever was defined most recently D) it raises an error automatically

42. What is a "protected" attribute in Python, by convention?
A) `self.__x` B) `self._x` C) `self.x` D) there's no such thing in Python

43. What's the main risk of a deep inheritance chain (four or five levels)?
A) it runs slower B) it becomes hard to trace where behavior actually comes from C) Python doesn't allow it D) it requires multiple inheritance

44. Which of these is the correct way to call a parent class's `__init__` from a child class?
A) `Parent.__init__()` B) `self.__init__()` C) `super().__init__(...)` D) `init(self)`

45. What best distinguishes an abstract base class from a regular base class?
A) abstract base classes can't have any concrete methods B) abstract base classes can't be instantiated directly if they have unimplemented abstract methods C) abstract base classes can't be inherited from D) there is no real difference

46. Why is checking `isinstance()` repeatedly in a chain of `elif` statements often a design smell?
A) it's slower than a for loop B) it signals that polymorphism should be doing that work instead C) Python discourages `isinstance()` entirely D) it always causes bugs

47. What's the correct relationship type for `Order` containing a list of `LineItem` objects created specifically for that order?
A) inheritance B) composition C) polymorphism D) abstraction

48. Which of these is most likely to violate the Open/Closed Principle?
A) an abstract interface with multiple implementations B) a long `if/elif` chain that needs a new branch every time a new case is added C) a class using `@property` D) a class using composition

49. What does `cls(*args)` typically accomplish inside a `@classmethod` alternate constructor?
A) it creates a new instance of whichever class actually called the method B) it modifies the current instance C) it deletes the class D) it always creates a `Rectangle`, regardless of subclass

50. Which best summarizes the relationship between inheritance and polymorphism?
A) they're the same thing B) inheritance is the structure; polymorphism is the behavioral payoff of using that structure C) polymorphism requires no inheritance ever D) inheritance always requires polymorphism

---

## Section B: True or false (20 questions)

1. `self` must always be explicitly passed as the first argument when calling an instance method through an instance (`obj.method()`).
2. Class attributes are shared across all instances until an instance shadows them.
3. Python enforces private attribute access at the interpreter level, making it impossible to access from outside the class.
4. `super()` always refers to the immediate next class in the MRO, not necessarily the literal parent named in the class definition.
5. Abstract methods can have a concrete implementation body that a subclass can call via `super()`.
6. Composition implies the contained object cannot exist independently of its container.
7. Aggregation implies the contained object can exist independently of its container.
8. Python supports true method overloading, where the same method name can have multiple signatures.
9. Duck typing requires all objects involved to share a common base class.
10. The Open/Closed Principle suggests you should regularly go back and modify existing, tested classes to add new features.
11. A class can inherit from more than one parent class in Python.
12. The diamond problem in Python is resolved deterministically through MRO.
13. `@staticmethod` methods can access instance attributes directly through an implicit `self`.
14. High cohesion means a class is focused on one clear responsibility.
15. Tight coupling makes a codebase easier to change safely over time.
16. `__eq__` and `__hash__` should generally be defined consistently with each other.
17. An abstract class can contain fully implemented, concrete methods alongside its abstract ones.
18. Favoring composition over inheritance means inheritance should never be used.
19. A UML diagram's filled diamond typically represents composition.
20. Class methods and instance methods can be called using identical dot-call syntax.

---

## Section C: Identification (20 questions)

1. The method that runs automatically when a new object is instantiated.
2. The decorator marking a method that receives the class itself as its first argument.
3. The decorator marking a method that receives neither `self` nor `cls`.
4. The mechanism Python uses to make double-underscore attributes harder to access from outside their defining class.
5. The function/proxy used to call a parent class's methods without hardcoding its name.
6. The term for the order Python searches classes when resolving a method or attribute.
7. The module providing `ABC` and `@abstractmethod`.
8. The term for an object's suitability being judged by its methods and attributes rather than its declared type.
9. The magic method controlling what `str(obj)` or `print(obj)` displays.
10. The magic method controlling what `==` means for a custom class.
11. The relationship type where one class "is-a" specialized version of another.
12. The relationship type where one class "has-a" instance of another, with shared ownership and lifecycle.
13. The relationship type where one class "has-a" instance of another, without ownership over its lifecycle.
14. The design principle stating a class should have only one reason to change.
15. The design principle stating classes should be open for extension but closed for modification.
16. The term for how dependent one class is on another's internal details.
17. The term for how focused a single class is on one clear responsibility.
18. The classic ambiguity that arises when a class inherits from two classes that share a common ancestor.
19. The term for a class designed specifically to be combined with others via multiple inheritance, not used standalone.
20. The decorator used to turn a method into a controlled, attribute-like accessor.

---

## Section D: Short answer (15 questions)

1. Explain the difference between an instance method, a class method, and a static method, in your own words.
2. Why does `self.attribute = value` never modify a class attribute directly, even if an attribute of the same name exists at the class level?
3. Explain name mangling and why it exists.
4. What's the practical difference between composition and aggregation, and why does that difference matter in a real design?
5. Explain the diamond problem and how Python's MRO resolves it deterministically.
6. Why does Python enforce abstract methods at instantiation time rather than when the class is first defined?
7. What's the difference between abstraction and encapsulation?
8. Explain duck typing and why it's central to idiomatic Python.
9. Why is a long `isinstance()`/`elif` chain often considered a design smell?
10. Explain the Single Responsibility Principle with a concrete example.
11. Explain the Open/Closed Principle with a concrete example.
12. Why is "favor composition over inheritance" a general guideline rather than an absolute rule? Give an example where inheritance is genuinely the right choice.
13. What does high cohesion and low coupling actually cost a team when it's missing, in practical terms?
14. Why should `__eq__` and `__hash__` generally be defined together and consistently?
15. Explain what a mixin class is and how it differs from a normal parent class in intent.

---

## Section E: Code tracing (10 questions)

1.
```python
class A:
    def __init__(self):
        self.x = 1

class B(A):
    def __init__(self):
        super().__init__()
        self.x += 10

print(B().x)
```

2.
```python
class Counter:
    total = 0
    def __init__(self):
        Counter.total += 1
        self.id = Counter.total

a, b, c = Counter(), Counter(), Counter()
print(a.id, b.id, c.id, Counter.total)
```

3.
```python
class Shape:
    def area(self):
        return 0

class Circle(Shape):
    def __init__(self, r):
        self.r = r
    def area(self):
        return round(3.14159 * self.r ** 2, 2)

shapes = [Shape(), Circle(2)]
print([s.area() for s in shapes])
```

4.
```python
class A:
    def greet(self):
        return "A"

class B(A):
    pass

class C(B):
    def greet(self):
        return "C" + super().greet()

print(C().greet())
```

5.
```python
class Wallet:
    def __init__(self):
        self.__balance = 0
    @property
    def balance(self):
        return self.__balance
    def add(self, amount):
        self.__balance += amount

w = Wallet()
w.add(50)
print(w.balance)
```

6.
```python
class Base:
    def who(self): return "Base"

class Left(Base):
    def who(self): return "Left"

class Right(Base):
    def who(self): return "Right"

class D(Left, Right):
    pass

print(D().who())
print(D.__mro__[2])
```

7.
```python
class Animal:
    sound = "..."

a = Animal()
b = Animal()
a.sound = "Woof"
print(a.sound, b.sound, Animal.sound)
```

8.
```python
class Item:
    def __init__(self, price):
        self.price = price
    def __lt__(self, other):
        return self.price < other.price

items = [Item(30), Item(10), Item(20)]
print([i.price for i in sorted(items)])
```

9.
```python
class Config(ABC):
    @abstractmethod
    def load(self): ...
    def describe(self):
        return "A config object"

class JSONConfig(Config):
    def load(self):
        return "loaded json"

c = JSONConfig()
print(c.describe(), c.load())
```

10.
```python
class Node:
    def __init__(self, value):
        self.value = value
        self.children = []
    def add(self, child):
        self.children.append(child)

root = Node(1)
child = Node(2)
root.add(child)
print(len(root.children), root.children[0].value)
```

---

## Section F: Debugging tasks (10 questions)

1.
```python
class Dog:
    def __init__(name):
        self.name = name
```

2.
```python
class Account:
    balance = 0
    def deposit(self, amount):
        self.balance += amount

a = Account()
b = Account()
a.deposit(100)
print(a.balance, b.balance)  # not actually an error, but explain the surprising result
```

3.
```python
class Shape(ABC):
    @abstractmethod
    def area(self): pass

class Square(Shape):
    def __init__(self, side):
        self.side = side

s = Square(4)
```

4.
```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        self.breed = breed
```

5.
```python
class Money:
    def __init__(self, amount):
        self.amount = amount
    def __add__(self, other):
        return self.amount + other.amount

m = Money(5) + Money(10)
print(m.amount)
```

6.
```python
class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

class Point3D(Point):
    def __init__(self, x, y, z):
        super().__init__(x, y)
        self.z = z
    def show(self):
        return self.__x
```

7.
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary
    @property
    def salary(self):
        return self.__salary
```

8.
```python
class Cache:
    def __init__(self):
        self.data = {}
    def get(self, key):
        return self.data[key]
```

9.
```python
class Base:
    def __init__(self):
        print("Base")

class Child(Base):
    def __init__(self):
        print("Child")

Child()  # explain what does NOT get printed, and why
```

10.
```python
class Discount:
    def apply(self, price, kind):
        if kind == "flat":
            return price - 10
        elif kind == "percent":
            return price * 0.9
```
(Not a runtime bug. Identify the design principle this violates and explain why.)

---

## Section G: Class design exercises (5)

For each, sketch the class (or classes) you'd design: names, key attributes, key methods, and the relationships between them (inheritance, composition, or aggregation). Code isn't required, a clear written or UML-style sketch with reasoning is the actual deliverable.

1. Design a system for a university course registration platform: students, courses, and enrollments. Consider whether "enrollment" deserves to be its own class.

2. Design a system for a food delivery app: restaurants, menu items, orders, and delivery drivers. Identify which relationships are composition and which are aggregation, and justify each choice.

3. Design an abstraction for a notification system that needs to support email, SMS, and push notifications today, with the explicit expectation that more channels will be added later. Focus on what makes this design genuinely open for extension.

4. Design a small hierarchy for a media library: movies, TV shows, and music albums, all of which can be "played" and have a duration, but differ significantly in their other attributes. Decide what belongs in a shared base class versus what shouldn't be forced into one.

5. You're told a `Vehicle` class currently has `Car`, `Motorcycle`, and `Boat` as subclasses, and a new requirement means vehicles need an `ElectricEngine` or `GasEngine`, and some vehicles (hybrid cars) need both. Explain why this specific requirement is a strong signal to introduce composition (an `Engine` component) rather than trying to solve it with further inheritance, and sketch the resulting design.

---

## Practical exam (timed, approximately 2.5 hours)

Build the core of a small library management system, solo, documentation allowed, this course's own examples not allowed.

Requirements:

- A `Book` class and a `Member` class
- An abstract `LibraryItem` base if you decide `Book` should be one of potentially several item types (this decision, and your justification for it, is part of what's being evaluated)
- A `Library` class that composes/aggregates books and members appropriately, and provides `checkout(member, book)` and `return_item(member, book)`
- Custom exceptions for realistic failures: checking out an already-checked-out book, a member with too many books already checked out, returning a book that was never checked out
- At least one use of `@property` with real validation
- A simple CLI or a clear test script demonstrating the whole system working end to end

You'll be evaluated on:

- Correctness: does it work as specified
- Design judgment: are the relationships between classes (inheritance vs. composition vs. aggregation) genuinely justified, not just functional
- Encapsulation: is internal state actually protected, not just publicly exposed by convention
- Use of custom exceptions for real business rules, not generic ones
- Whether the design would survive a reasonable new requirement (a second item type, like a DVD) without a significant rewrite

## Mock technical interview

When you're ready, tell me, and I'll run a 45-minute OOP-focused technical screen: some rapid-fire concept questions, at least one live class design problem where you'll need to think out loud and justify your structure as you go, and at least one refactoring question where you'll be shown flawed code and asked to fix it, and explain why it was flawed. Expect pushback on any design decision that isn't justified, that's genuinely how a senior interviewer would run this. You'll get a scored evaluation at the end covering technical accuracy, design judgment specifically, and communication, plus an honest read on where you'd stand in a real screen.

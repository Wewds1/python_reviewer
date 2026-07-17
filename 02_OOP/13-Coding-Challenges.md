# Coding Challenges — Module 2

## How to use this file

Same rule as Module 1: attempt everything before checking any answer. OOP design problems especially punish looking at a solution too early, the value here is in the struggle of deciding how to structure the classes, not just in producing working code. If a problem doesn't specify exact attributes or methods, that's deliberate. Deciding the shape of a class is part of the exercise.

---

## Beginner (20)

1. Write a `Dog` class with `name` and `breed`, and a method `bark()`.
2. Write a `Rectangle` class with `width` and `height`, and methods for `area()` and `perimeter()`.
3. Write a `Person` class with `first_name` and `last_name`, and a method `full_name()`.
4. Write a `Book` class with `title`, `author`, and `pages`, and a method that reports whether it's a "long" book (over 400 pages).
5. Write a `Circle` class with `radius`, and methods `area()` and `circumference()`.
6. Write a `Car` class with `make`, `model`, and `year`, and a method `age(current_year)`.
7. Write a `BankAccount` class with a `balance`, and `deposit()`/`withdraw()` methods that prevent overdrawing.
8. Write a `Student` class with `name` and a list of `grades`, and a method `average()`.
9. Write a `Playlist` class that holds a list of song titles, with `add_song()` and `remove_song()` methods.
10. Write a `Temperature` class storing a value in Celsius, with a method `to_fahrenheit()`.
11. Write a class `Counter` with a method `increment()` and a method `reset()`.
12. Write a `Shape` class with a class attribute `sides` and an instance method that reports it.
13. Write a `Product` class with `name` and `price`, and a class method `on_sale(cls, name, original_price, discount_percent)` that returns a discounted product.
14. Write a `Timer` class with `start()` and `stop()` methods that report elapsed time (you can simulate elapsed time with a stored value rather than real timing).
15. Write a `Wallet` class with a balance, and `add_funds()`/`spend()` methods, raising an exception if spending exceeds the balance.
16. Write a `Movie` class with `title`, `genre`, and `rating`, and a static method that validates a rating is between 0 and 10.
17. Write a `Recipe` class with a list of ingredients and a method `ingredient_count()`.
18. Write an `Employee` class with `name` and `salary`, and a method `give_raise(percent)`.
19. Write a `Deck` class representing a deck of cards as a list of strings, with a method `shuffle()` (using `random.shuffle`) and a method `draw()`.
20. Write a `Thermostat` class with a `target_temperature` property that rejects values outside a sensible range (say, 50 to 90 degrees Fahrenheit).

## Intermediate (20)

1. Build a small `Vehicle` → `Car`/`Motorcycle` inheritance hierarchy, where each subclass overrides a `describe()` method.
2. Add `@property` getters and setters to a `Temperature` class so that setting Celsius automatically keeps a computed Fahrenheit value in sync.
3. Build an abstract `Shape` class with an abstract `area()` method, and at least three concrete subclasses.
4. Build a `Stack` class using composition (a private list attribute) with `push()`, `pop()`, and `peek()` methods, hiding the underlying list entirely from outside access.
5. Design a `Person`/`Student`/`Teacher` inheritance hierarchy where `Student` and `Teacher` both override a shared `role()` method.
6. Implement `__str__`, `__eq__`, and `__lt__` on a `Money` class so instances can be printed, compared for equality, and sorted.
7. Build a `Library` class composed of `Book` objects (aggregation, not composition, the books exist independently) with methods to check out and return a book by title.
8. Design a `Notification` abstract base class with concrete `EmailNotification` and `SMSNotification` subclasses, and a function that sends a mixed list of notifications polymorphically.
9. Build a `Team` class that aggregates `Player` objects, with a method that returns the player with the highest score.
10. Design a class hierarchy for `Animal` → `Mammal`/`Bird`, each overriding a `move()` method appropriately (`walk`, `fly`), and demonstrate polymorphic behavior over a mixed list.
11. Build an `Inventory` class with a private dictionary of item names to quantities, exposing controlled `add_item()`, `remove_item()`, and a read-only `total_items` property.
12. Implement a `Matrix` class (a list of lists) with `__add__` overloaded to add two matrices of the same dimensions element-wise.
13. Design a `PaymentMethod` abstract class with `CreditCard` and `PayPal` subclasses, each implementing `process(amount)` differently, and write a function that totals a mixed list of processed payments.
14. Build a `Garage` class composed of multiple `Car` objects, with a method `total_value()` summing a `value` attribute across every car.
15. Design a `Shape` hierarchy where `Square` inherits from `Rectangle` (a genuine "is-a" relationship, since a square is a rectangle with equal sides), overriding the constructor appropriately.
16. Build a `Logger` class using a class attribute to track total messages logged across every instance, alongside an instance-level list of that specific logger's own messages.
17. Design an abstract `Repository` class with `save()` and `find_by_id()`, and a concrete `InMemoryRepository` implementation backed by a dictionary.
18. Build a `Config` class using `@property` where a setter validates that a `max_connections` value is a positive integer, raising a clear exception otherwise.
19. Design a `Shape` class hierarchy where each subclass also implements `__str__` to describe itself, and write code that prints a mixed list of shapes uniformly.
20. Build an `Order` class composed of a list of `LineItem` objects (each with a `price` and `quantity`), with a method `total()` that sums across all line items.

## Advanced (15)

1. Design and implement a small plugin-style `DiscountEngine` following the Open/Closed Principle: an abstract `Discount` interface, at least four concrete discount types, and an `apply_all(discounts, price)` function that never needs modification as new discount types are added.
2. Build a `Cache` abstraction (abstract base class) with two concrete implementations, `InMemoryCache` and a simple `FileCache` that persists to JSON, and write test code proving both satisfy the same interface identically.
3. Design a multiple inheritance scenario using two legitimate mixins (`Loggable` and `Serializable`) combined into a concrete `Order` class, and demonstrate both mixin behaviors working correctly together.
4. Build a `StateMachine`-style `OrderStatus` system using an abstract base and concrete state classes (`Pending`, `Shipped`, `Delivered`), where invalid transitions raise a custom exception, tying this back to Module 1's exception handling.
5. Design a `Shape` hierarchy with at least four subclasses and implement `__eq__`, `__lt__` (by area), and `__repr__` consistently across all of them, then sort a mixed list of shapes by area using the built-in `sorted()`.
6. Build a small event system: an `EventEmitter` class that lets other objects `subscribe(event_name, handler)` and `emit(event_name, data)`, calling every subscribed handler polymorphically, no type checking on the handlers.
7. Refactor a deliberately tangled `UserManager` class (write the "before" version yourself, handling validation, persistence, and email all in one class) into properly separated, composed classes following SRP.
8. Design a `Vehicle` rental system with an abstract `Rentable` interface, concrete `Car`, `Bike`, and `Scooter` implementations each with different `calculate_rental_cost(hours)` logic, and a `RentalService` that processes a mixed list polymorphically.
9. Build a `Graph` class representing nodes and edges using composition (a `Node` class holding references to connected `Node` objects), with a method to check whether two nodes are connected via any path (breadth-first or depth-first traversal).
10. Design an abstract `Validator` interface with several concrete validators (`RequiredFieldValidator`, `EmailFormatValidator`, `RangeValidator`), and a `CompositeValidator` that runs a list of validators against a piece of data and collects every failure rather than stopping at the first one.
11. Build a `Employee` payroll hierarchy at least three levels deep (multilevel inheritance), where each level's `calculate_pay()` correctly calls `super()` to build on the level above, and demonstrate the full chain resolving correctly.
12. Design a `Shape` factory: a class method on an abstract `Shape` base that, given a type name string and parameters, constructs and returns the correct concrete subclass instance, without the calling code needing to import or reference the concrete classes directly.
13. Build a simple `ObserverPattern` example: a `StockPrice` subject class that notifies a list of subscribed `Investor` observer objects whenever its price changes, each observer reacting independently and polymorphically.
14. Design an `Account` hierarchy (`SavingsAccount`, `CheckingAccount`) exactly as shown in Lesson 11, then add a `PremiumCheckingAccount` that further specializes `CheckingAccount`, correctly chaining `super()` calls across all three levels.
15. Build a small dependency-injection-style `ReportService`, composed entirely of abstract interfaces (`DataSource`, `Formatter`, `Exporter`), and demonstrate assembling two functionally different `ReportService` instances from different concrete implementations, with zero changes to `ReportService` itself.

## Debugging exercises (10)

1.
```python
class Dog:
    def bark():  # missing self
        return "Woof"
```

2.
```python
class Account:
    balance = 0  # class attribute, not instance — bug waiting to happen
    def deposit(self, amount):
        self.balance += amount

a = Account()
b = Account()
a.deposit(100)
print(b.balance)
```

3.
```python
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

s = Shape()
```
(Explain what's missing from the import for this to even attempt to run, and what error occurs once it's fixed.)

4.
```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        self.breed = breed
        # missing super().__init__(name) call
```

5.
```python
class Base:
    def greet(self):
        return "Base"

class Left(Base):
    def greet(self):
        return "Left"

class Right(Base):
    def greet(self):
        return "Right"

class Child(Right, Left):
    pass

print(Child().greet())
```
(Not actually broken. Predict the exact output and explain why, referencing MRO.)

6.
```python
class Money:
    def __init__(self, amount):
        self.amount = amount
    def __add__(self, other):
        return self.amount + other.amount  # returns a plain number, not a Money
```

7.
```python
class Cart:
    items = []
    def add(self, item):
        self.items.append(item)
```

8.
```python
class Point:
    def __init__(self, x, y):
        self.__x = x
        self.__y = y

class Point3D(Point):
    def show(self):
        return self.__x  # AttributeError due to name mangling
```

9.
```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    @property
    def salary(self):
        return self.__salary
    # missing setter, but __init__ still tries self.salary = salary
```

10.
```python
class Config(ABC):
    @abstractmethod
    def load(self):
        pass

class JSONConfig(Config):
    pass  # forgot to implement load()

c = JSONConfig()
```

## Code reading exercises (10)

1.
```python
class A:
    def __init__(self):
        self.value = 10

class B(A):
    def __init__(self):
        super().__init__()
        self.value += 5

print(B().value)
```

2.
```python
class Base:
    count = 0
    def __init__(self):
        Base.count += 1

a, b, c = Base(), Base(), Base()
print(Base.count)
```

3.
```python
class Shape:
    def area(self):
        return 0

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side ** 2

shapes = [Shape(), Square(4)]
print(sum(s.area() for s in shapes))
```

4.
```python
class Vector:
    def __init__(self, x):
        self.x = x
    def __repr__(self):
        return f"Vector({self.x})"

print([Vector(1), Vector(2)])
```

5.
```python
class Node:
    def __init__(self, value, next_node=None):
        self.value = value
        self.next_node = next_node

n3 = Node(3)
n2 = Node(2, n3)
n1 = Node(1, n2)

current = n1
while current:
    print(current.value)
    current = current.next_node
```

6.
```python
class Meta(type):
    pass

class Foo(metaclass=Meta):
    pass

print(type(Foo))
```
(This is intentionally at the edge of the module's scope. Explain what you can, and note what's unfamiliar.)

7.
```python
class Config:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls._instance = Config()
        return cls._instance

a = Config.get_instance()
b = Config.get_instance()
print(a is b)
```

8.
```python
class Animal:
    def speak(self):
        return "..."

class Cat(Animal):
    def speak(self):
        return "Meow"

animals = [Animal(), Cat()]
for a in animals:
    print(a.speak())
```

9.
```python
class Wrapper:
    def __init__(self, value):
        self._value = value
    def __len__(self):
        return len(self._value)

w = Wrapper([1, 2, 3])
print(len(w))
```

10.
```python
class Base:
    def __init__(self, x):
        self.x = x

class Derived(Base):
    pass

d = Derived(5)
print(d.x)
```

## Output prediction exercises (10)

1.
```python
class Counter:
    total = 0
    def __init__(self):
        Counter.total += 1

Counter(); Counter(); Counter()
print(Counter.total)
```

2.
```python
class A:
    def hello(self):
        return "A"

class B(A):
    def hello(self):
        return super().hello() + "B"

print(B().hello())
```

3.
```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

p1 = Point(1, 2)
p2 = p1
p2.x = 99
print(p1.x)
```

4.
```python
class Shape(ABC):
    @abstractmethod
    def area(self): pass

class Square(Shape):
    def __init__(self, side): self.side = side
    def area(self): return self.side ** 2

print(Square(4).area())
```

5.
```python
class Animal:
    sound = "generic"

class Dog(Animal):
    pass

d = Dog()
d.sound = "bark"
print(d.sound, Animal.sound)
```

6.
```python
class A:
    def __eq__(self, other):
        return True

print(A() == A())
print(A() == 5)
```

7.
```python
class Bag:
    def __init__(self):
        self.items = []
    def __len__(self):
        return len(self.items)

b = Bag()
print(bool(b))
b.items.append("x")
print(bool(b))
```

8.
```python
class Base:
    def __init__(self):
        print("Base init")

class Child(Base):
    def __init__(self):
        print("Child init")
        super().__init__()

Child()
```

9.
```python
class A:
    def who(self): return "A"

class B(A):
    def who(self): return "B"

class C(A):
    def who(self): return "C"

class D(B, C):
    pass

print(D().who())
print(D.__mro__[1])
```

10.
```python
class Temp:
    def __init__(self, c):
        self._c = c
    @property
    def fahrenheit(self):
        return self._c * 9/5 + 32

t = Temp(0)
print(t.fahrenheit)
```

---

A separate answer key with full explanations for every problem walks through not just the correct implementation, but the specific design reasoning behind class boundaries, since that reasoning is the actual skill this module is building.

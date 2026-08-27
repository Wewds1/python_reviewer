# Coding Challenges - Module 2 (Intermediate)
# Written by a Junior Engineer

from abc import ABC, abstractmethod

# 1. Build a small Vehicle -> Car/Motorcycle inheritance hierarchy, where each subclass overrides a describe() method.
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def describe(self):
        return "This is a vehicle made by " + self.brand

class Car(Vehicle):
    def describe(self):
        return "This is a car made by " + self.brand

class Motorcycle(Vehicle):
    def describe(self):
        return "This is a motorcycle made by " + self.brand

# 2. Add @property getters and setters to a Temperature class so that setting Celsius automatically keeps a computed Fahrenheit value in sync.
class Temperature:
    def __init__(self, celsius):
        self._celsius = celsius
        self._fahrenheit = (celsius * 9/5) + 32

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        self._celsius = value
        # keep fahrenheit in sync
        self._fahrenheit = (value * 9/5) + 32

    @property
    def fahrenheit(self):
        return self._fahrenheit

# 3. Build an abstract Shape class with an abstract area() method, and at least three concrete subclasses.
class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Square(Shape):
    def __init__(self, side):
        self.side = side
    def area(self):
        return self.side * self.side

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        import math
        return math.pi * (self.radius ** 2)

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height
    def area(self):
        return 0.5 * self.base * self.height

# 4. Build a Stack class using composition (a private list attribute) with push(), pop(), and peek() methods, hiding the underlying list entirely from outside access.
class Stack:
    def __init__(self):
        self.__items = [] # private list

    def push(self, item):
        self.__items.append(item)

    def pop(self):
        if len(self.__items) == 0:
            return "Stack is empty"
        return self.__items.pop()

    def peek(self):
        if len(self.__items) == 0:
            return "Stack is empty"
        return self.__items[-1]

# 5. Design a Person/Student/Teacher inheritance hierarchy where Student and Teacher both override a shared role() method.
class Person:
    def __init__(self, name):
        self.name = name
    def role(self):
        return "General Person"

class Student(Person):
    def role(self):
        return "Student"

class Teacher(Person):
    def role(self):
        return "Teacher"

# 6. Implement __str__, __eq__, and __lt__ on a Money class so instances can be printed, compared for equality, and sorted.
class Money:
    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency

    def __str__(self):
        return str(self.amount) + " " + self.currency

    def __eq__(self, other):
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount and self.currency == other.currency

    def __lt__(self, other):
        if not isinstance(other, Money):
            return NotImplemented
        return self.amount < other.amount

# 7. Build a Library class composed of Book objects (aggregation, not composition, the books exist independently) with methods to check out and return a book by title.
class Book:
    def __init__(self, title):
        self.title = title
        self.is_checked_out = False

class Library:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        self.books.append(book)

    def checkout_book(self, title):
        for book in self.books:
            if book.title == title and not book.is_checked_out:
                book.is_checked_out = True
                return "You checked out " + title
        return "Book not available"

    def return_book(self, title):
        for book in self.books:
            if book.title == title and book.is_checked_out:
                book.is_checked_out = False
                return "You returned " + title
        return "Book was not checked out"

# 8. Design a Notification abstract base class with concrete EmailNotification and SMSNotification subclasses, and a function that sends a mixed list of notifications polymorphically.
class Notification(ABC):
    @abstractmethod
    def send(self, message):
        pass

class EmailNotification(Notification):
    def send(self, message):
        return "Sending Email: " + message

class SMSNotification(Notification):
    def send(self, message):
        return "Sending SMS: " + message

def send_notifications(notifications, msg):
    results = []
    for n in notifications:
        results.append(n.send(msg))
    return results

# 9. Build a Team class that aggregates Player objects, with a method that returns the player with the highest score.
class Player:
    def __init__(self, name, score):
        self.name = name
        self.score = score

class Team:
    def __init__(self, team_name):
        self.team_name = team_name
        self.players = []

    def add_player(self, player):
        self.players.append(player)

    def get_top_player(self):
        if not self.players:
            return None
        top_player = self.players[0]
        for p in self.players:
            if p.score > top_player.score:
                top_player = p
        return top_player

# 10. Design a class hierarchy for Animal -> Mammal/Bird, each overriding a move() method appropriately (walk, fly), and demonstrate polymorphic behavior over a mixed list.
class Animal(ABC):
    @abstractmethod
    def move(self):
        pass

class Mammal(Animal):
    def move(self):
        return "walking on four legs"

class Bird(Animal):
    def move(self):
        return "flying through the air"

# 11. Build an Inventory class with a private dictionary of item names to quantities, exposing controlled add_item(), remove_item(), and a read-only total_items property.
class Inventory:
    def __init__(self):
        self.__items = {} # private dict

    def add_item(self, name, qty):
        if name in self.__items:
            self.__items[name] = self.__items[name] + qty
        else:
            self.__items[name] = qty

    def remove_item(self, name, qty):
        if name in self.__items and self.__items[name] >= qty:
            self.__items[name] = self.__items[name] - qty
        else:
            print("Not enough items to remove")

    @property
    def total_items(self):
        total = 0
        for qty in self.__items.values():
            total = total + qty
        return total

# 12. Implement a Matrix class (a list of lists) with __add__ overloaded to add two matrices of the same dimensions element-wise.
class Matrix:
    def __init__(self, rows):
        self.rows = rows # list of lists

    def __add__(self, other):
        # check dimensions
        if len(self.rows) != len(other.rows) or len(self.rows[0]) != len(other.rows[0]):
            raise ValueError("Matrix dimensions must match")

        new_rows = []
        for i in range(len(self.rows)):
            row = []
            for j in range(len(self.rows[0])):
                row.append(self.rows[i][j] + other.rows[i][j])
            new_rows.append(row)
        return Matrix(new_rows)

# 13. Design a PaymentMethod abstract class with CreditCard and PayPal subclasses, each implementing process(amount) differently, and write a function that totals a mixed list of processed payments.
class PaymentMethod(ABC):
    @abstractmethod
    def process(self, amount):
        pass

class CreditCard(PaymentMethod):
    def process(self, amount):
        return amount * 1.03 # simulate 3% fee

class PayPal(PaymentMethod):
    def process(self, amount):
        return amount * 1.02 # simulate 2% fee

def total_payments(methods, amount):
    total = 0
    for m in methods:
        total = total + m.process(amount)
    return total

# 14. Build a Garage class composed of multiple Car objects, with a method total_value() summing a value attribute across every car.
class GarageCar:
    def __init__(self, model, value):
        self.model = model
        self.value = value

class Garage:
    def __init__(self):
        self.cars = []

    def add_car(self, car):
        self.cars.append(car)

    def total_value(self):
        total = 0
        for c in self.cars:
            total = total + c.value
        return total

# 15. Design a Shape hierarchy where Square inherits from Rectangle (a genuine "is-a" relationship, since a square is a rectangle with equal sides), overriding the constructor appropriately.
class RectangleBase:
    def __init__(self, width, height):
        self.width = width
        self.height = height
    def area(self):
        return self.width * self.height

class SquareBase(RectangleBase):
    def __init__(self, side):
        # a square is just a rectangle where width and height are the same
        super().__init__(side, side)

# 16. Build a Logger class using a class attribute to track total messages logged across every instance, alongside an instance-level list of that specific logger's own messages.
class Logger:
    total_logs = 0 # class attribute

    def __init__(self):
        self.my_logs = [] # instance list

    def log(self, message):
        Logger.total_logs = Logger.total_logs + 1
        self.my_logs.append(message)

# 17. Design an abstract Repository class with save() and find_by_id(), and a concrete InMemoryRepository implementation backed by a dictionary.
class Repository(ABC):
    @abstractmethod
    def save(self, item_id, data):
        pass
    @abstractmethod
    def find_by_id(self, item_id):
        pass

class InMemoryRepository(Repository):
    def __init__(self):
        self.data = {}

    def save(self, item_id, data):
        self.data[item_id] = data

    def find_by_id(self, item_id):
        return self.data.get(item_id)

# 18. Build a Config class using @property where a setter validates that a max_connections value is a positive integer, raising a clear exception otherwise.
class Config:
    def __init__(self):
        self._max_connections = 10

    @property
    def max_connections(self):
        return self._max_connections

    @max_connections.setter
    def max_connections(self, value):
        if not isinstance(value, int) or value <= 0:
            raise ValueError("max_connections must be a positive integer")
        self._max_connections = value

# 19. Design a Shape hierarchy where each subclass also implements __str__ to describe itself, and write code that prints a mixed list of shapes uniformly.
class ShapeStr(ABC):
    @abstractmethod
    def __str__(self):
        pass

class CircleStr(ShapeStr):
    def __str__(self):
        return "I am a Circle"

class SquareStr(ShapeStr):
    def __str__(self):
        return "I am a Square"

# 20. Build an Order class composed of a list of LineItem objects (each with a price and quantity), with a method total() that sums across all line items.
class LineItem:
    def __init__(self, name, price, qty):
        self.name = name
        self.price = price
        self.qty = qty

class Order:
    def __init__(self):
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def total(self):
        sum_total = 0
        for i in self.items:
            sum_total = sum_total + (i.price * i.qty)
        return sum_total

# --- Testing Intermediate Challenges ---
if __name__ == "__main__":
    print("--- Testing OOP Intermediate Challenges ---")

    v1 = Car("Toyota")
    v2 = Motorcycle("Yamaha")
    print("Task 1:", v1.describe(), "|", v2.describe())

    t = Temperature(20)
    t.celsius = 25
    print("Task 2 Fahr:", t.fahrenheit)

    s1 = Square(4)
    s2 = Circle(3)
    print("Task 3 Areas:", s1.area(), s2.area())

    st = Stack()
    st.push(10)
    st.push(20)
    print("Task 4 Peek:", st.peek(), "Pop:", st.pop())

    p1 = Student("Alice")
    p2 = Teacher("Mr. Bob")
    print("Task 5 Roles:", p1.role(), p2.role())

    m1 = Money(10, "USD")
    m2 = Money(20, "USD")
    print("Task 6:", m1, " == ", m2, "is", m1 == m2, "|", m1 < m2)

    lib = Library()
    b1 = Book("Python 101")
    lib.add_book(b1)
    print("Task 7 Checkout:", lib.checkout_book("Python 101"))
    print("Task 7 Return:", lib.return_book("Python 101"))

    notifs = [EmailNotification(), SMSNotification()]
    print("Task 8:", send_notifications(notifs, "Hello!"))

    tm = Team("Warriors")
    tm.add_player(Player("Stephen", 100))
    tm.add_player(Player("Klay", 80))
    print("Task 9 Top:", tm.get_top_player().name)

    animals = [Mammal(), Bird()]
    for a in animals:
        print("Task 10 Animal moves by:", a.move())

    inv = Inventory()
    inv.add_item("Apple", 10)
    inv.add_item("Apple", 5)
    inv.remove_item("Apple", 2)
    print("Task 11 Total:", inv.total_items)

    mat1 = Matrix([[1, 2], [3, 4]])
    mat2 = Matrix([[5, 6], [7, 8]])
    res = mat1 + mat2
    print("Task 12 Result:", res.rows)

    pay = [CreditCard(), PayPal()]
    print("Task 13 Total:", total_payments(pay, 100))

    gar = Garage()
    gar.add_car(GarageCar("Tesla", 50000))
    gar.add_car(GarageCar("Ford", 20000))
    print("Task 14 Value:", gar.total_value())

    sq = SquareBase(5)
    print("Task 15 Area:", sq.area())

    l1 = Logger()
    l2 = Logger()
    l1.log("msg 1")
    l2.log("msg 2")
    print("Task 16 Total logs:", Logger.total_logs)

    repo = InMemoryRepository()
    repo.save(1, "User A")
    print("Task 17 Find 1:", repo.find_by_id(1))

    cfg = Config()
    try:
        cfg.max_connections = -1
    except ValueError as e:
        print("Task 18 Error:", e)

    shapes_str = [CircleStr(), SquareStr()]
    for s in shapes_str:
        print("Task 19:", str(s))

    ord1 = Order()
    ord1.add_item(LineItem("Apple", 1.0, 5))
    ord1.add_item(LineItem("Banana", 0.5, 10))
    print("Task 20 Total:", ord1.total())

    print("--- Tests Finished ---")

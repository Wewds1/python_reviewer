# Coding Challenges - Module 2 (Advanced)
# Written by a Junior Engineer

from abc import ABC, abstractmethod
import json

# 1. Design and implement a small plugin-style DiscountEngine following the Open/Closed Principle:
# an abstract Discount interface, at least four concrete discount types, and an apply_all(discounts, price) function.
class Discount(ABC):
    @abstractmethod
    def apply(self, price):
        pass

class PercentageDiscount(Discount):
    def __init__(self, percent):
        self.percent = percent
    def apply(self, price):
        return price * (1 - self.percent / 100)

class FlatDiscount(Discount):
    def __init__(self, amount):
        self.amount = amount
    def apply(self, price):
        return price - self.amount

class BOGO(Discount):
    def apply(self, price):
        # simulate buy one get one half off
        return price * 0.75

class SeasonalDiscount(Discount):
    def apply(self, price):
        return price * 0.9

def apply_all_discounts(discounts, price):
    final_price = price
    for d in discounts:
        final_price = d.apply(final_price)
    return final_price

# 2. Build a Cache abstraction (abstract base class) with two concrete implementations,
# InMemoryCache and a simple FileCache that persists to JSON.
class Cache(ABC):
    @abstractmethod
    def get(self, key):
        pass
    @abstractmethod
    def set(self, key, value):
        pass

class InMemoryCache(Cache):
    def __init__(self):
        self.store = {}
    def get(self, key):
        return self.store.get(key)
    def set(self, key, value):
        self.store[key] = value

class FileCache(Cache):
    def __init__(self, filename):
        self.filename = filename
        self.store = {}
        self.load()

    def load(self):
        try:
            with open(self.filename, 'r') as f:
                self.store = json.load(f)
        except:
            self.store = {}

    def save(self):
        with open(self.filename, 'w') as f:
            json.dump(self.store, f)

    def get(self, key):
        return self.store.get(key)

    def set(self, key, value):
        self.store[key] = value
        self.save()

# 3. Design a multiple inheritance scenario using two legitimate mixins (Loggable and Serializable)
# combined into a concrete Order class.
class Loggable:
    def log(self, message):
        print("[LOG]: " + message)

class Serializable:
    def to_json(self):
        import json
        return json.dumps(self.__dict__)

class Order(Loggable, Serializable):
    def __init__(self, order_id, amount):
        self.order_id = order_id
        self.amount = amount

# 4. Build a StateMachine-style OrderStatus system using an abstract base and concrete state classes.
class OrderState(ABC):
    @abstractmethod
    def next(self, order):
        pass

class PendingState(OrderState):
    def next(self, order):
        print("Moving from Pending to Shipped")
        order.state = ShippedState()

class ShippedState(OrderState):
    def next(self, order):
        print("Moving from Shipped to Delivered")
        order.state = DeliveredState()

class DeliveredState(OrderState):
    def next(self, order):
        raise Exception("Order is already delivered!")

class OrderMachine:
    def __init__(self):
        self.state = PendingState()

    def advance(self):
        self.state.next(self)

# 5. Design a Shape hierarchy with at least four subclasses and implement __eq__, __lt__ (by area), and __repr__.
class BaseShape(ABC):
    @abstractmethod
    def area(self):
        pass
    def __lt__(self, other):
        return self.area() < other.area()
    def __eq__(self, other):
        return self.area() == other.area()
    def __repr__(self):
        return f"{self.__class__.__name__}(area={self.area():.2f})"

class AdvSquare(BaseShape):
    def __init__(self, s): self.s = s
    def area(self): return self.s**2

class AdvCircle(BaseShape):
    def __init__(self, r): self.r = r
    def area(self): import math; return math.pi * self.r**2

class AdvRect(BaseShape):
    def __init__(self, w, h): self.w, self.h = w, h
    def area(self): return self.w * self.h

class AdvTriangle(BaseShape):
    def __init__(self, b, h): self.b, self.h = b, h
    def area(self): return 0.5 * self.b * self.h

# 6. Build a small event system: an EventEmitter class that lets other objects subscribe and emit.
class EventEmitter:
    def __init__(self):
        self.listeners = {}

    def subscribe(self, event, handler):
        if event not in self.listeners:
            self.listeners[event] = []
        self.listeners[event].append(handler)

    def emit(self, event, data):
        if event in self.listeners:
            for handler in self.listeners[event]:
                handler(data)

# 7. Refactor a deliberately tangled UserManager class into properly separated, composed classes following SRP.
class UserDB:
    def save(self, user): print("Saving user to DB...")
    def load(self, id): return {"id": id, "name": "User"}

class UserEmailer:
    def send_welcome(self, user): print("Sending welcome email to " + user["name"])

class UserManager:
    def __init__(self):
        self.db = UserDB()
        self.emailer = UserEmailer()

    def create_user(self, id, name):
        user = {"id": id, "name": name}
        self.db.save(user)
        self.emailer.send_welcome(user)

# 8. Design a Vehicle rental system with an abstract Rentable interface, concrete Car, Bike, and Scooter.
class Rentable(ABC):
    @abstractmethod
    def calculate_rental_cost(self, hours):
        pass

class RentalCar(Rentable):
    def calculate_rental_cost(self, hours): return hours * 50

class RentalBike(Rentable):
    def calculate_rental_cost(self, hours): return hours * 10

class RentalScooter(Rentable):
    def calculate_rental_cost(self, hours): return hours * 15

class RentalService:
    def process_rentals(self, items, hours):
        total = 0
        for item in items:
            total = total + item.calculate_rental_cost(hours)
        return total

# 9. Build a Graph class representing nodes and edges using composition, with a method to check connectivity.
class Node:
    def __init__(self, name):
        self.name = name
        self.neighbors = []

class Graph:
    def __init__(self):
        self.nodes = {}

    def add_node(self, name):
        self.nodes[name] = Node(name)

    def add_edge(self, name1, name2):
        self.nodes[name1].neighbors.append(self.nodes[name2])
        self.nodes[name2].neighbors.append(self.nodes[name1])

    def is_connected(self, start_name, end_name):
        visited = set()
        stack = [self.nodes[start_name]]
        while stack:
            node = stack.pop()
            if node.name == end_name: return True
            if node not in visited:
                visited.add(node)
                stack.extend(node.neighbors)
        return False

# 10. Design an abstract Validator interface with several concrete validators and a CompositeValidator.
class Validator(ABC):
    @abstractmethod
    def validate(self, data):
        pass

class RequiredValidator(Validator):
    def validate(self, data):
        return "Missing field" if not data else None

class EmailValidator(Validator):
    def validate(self, data):
        return "Invalid email" if "@" not in data else None

class RangeValidator(Validator):
    def __init__(self, min_val, max_val):
        self.min, self.max = min_val, max_val
    def validate(self, data):
        return "Out of range" if not (self.min <= data <= self.max) else None

class CompositeValidator(Validator):
    def __init__(self, validators):
        self.validators = validators
    def validate(self, data):
        errors = []
        for v in self.validators:
            err = v.validate(data)
            if err: errors.append(err)
        return errors

# 11. Build an Employee payroll hierarchy at least three levels deep (multilevel inheritance).
class BaseEmployee:
    def calculate_pay(self):
        return 1000

class SalariedEmployee(BaseEmployee):
    def calculate_pay(self):
        return super().calculate_pay() + 2000

class ManagerEmployee(SalariedEmployee):
    def calculate_pay(self):
        return super().calculate_pay() + 5000

# 12. Design a Shape factory: a class method on an abstract Shape base.
class FactoryShape(ABC):
    @abstractmethod
    def area(self): pass

    @classmethod
    def create(cls, type, *args):
        if type == "square": return AdvSquare(*args)
        if type == "circle": return AdvCircle(*args)
        if type == "rect": return AdvRect(*args)
        raise ValueError("Unknown shape")

# 13. Build a simple ObserverPattern example: a StockPrice subject class and Investor observer.
class StockPrice:
    def __init__(self, symbol, price):
        self.symbol = symbol
        self._price = price
        self.observers = []

    def attach(self, observer):
        self.observers.append(observer)

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        self._price = value
        for obs in self.observers:
            obs.update(self.symbol, self._price)

class Investor:
    def __init__(self, name):
        self.name = name
    def update(self, symbol, price):
        print(f"Investor {self.name} notified: {symbol} is now {price}")

# 14. Design an Account hierarchy (Savings, Checking, PremiumChecking) chaining super().
class Account:
    def __init__(self, balance):
        self.balance = balance
    def get_interest(self): return 0

class SavingsAccount(Account):
    def get_interest(self):
        return super().get_interest() + 0.05

class CheckingAccount(SavingsAccount):
    def get_interest(self):
        return super().get_interest() - 0.01

class PremiumCheckingAccount(CheckingAccount):
    def get_interest(self):
        return super().get_interest() + 0.02

# 15. Build a small dependency-injection-style ReportService.
class DataSource(ABC):
    @abstractmethod
    def get_data(self): pass

class Formatter(ABC):
    @abstractmethod
    def format(self, data): pass

class Exporter(ABC):
    @abstractmethod
    def export(self, formatted_data): pass

class ReportService:
    def __init__(self, source, formatter, exporter):
        self.source = source
        self.formatter = formatter
        self.exporter = exporter
    def generate(self):
        data = self.source.get_data()
        formatted = self.formatter.format(data)
        self.exporter.export(formatted)

# --- Testing Advanced Challenges ---
if __name__ == "__main__":
    print("--- Testing OOP Advanced Challenges ---")

    discounts = [PercentageDiscount(10), FlatDiscount(5)]
    print("Task 1 Price:", apply_all_discounts(discounts, 100))

    cache = InMemoryCache()
    cache.set("user", "Alice")
    print("Task 2 Cache:", cache.get("user"))

    ord1 = Order(101, 250.0)
    ord1.log("Creating order")
    print("Task 3 JSON:", ord1.to_json())

    machine = OrderMachine()
    machine.advance()
    machine.advance()
    try:
        machine.advance()
    except Exception as e:
        print("Task 4 Caught:", e)

    shapes = [AdvSquare(2), AdvCircle(2), AdvRect(2, 3), AdvTriangle(2, 2)]
    print("Task 5 Sorted:", sorted(shapes))

    ee = EventEmitter()
    ee.subscribe("test", lambda d: print("Handler 1:", d))
    ee.subscribe("test", lambda d: print("Handler 2:", d))
    ee.emit("test", "Hello Event")

    um = UserManager()
    um.create_user(1, "Bob")

    rs = RentalService()
    items = [RentalCar(), RentalBike()]
    print("Task 8 Cost:", rs.process_rentals(items, 2))

    g = Graph()
    g.add_node("A"); g.add_node("B"); g.add_node("C")
    g.add_edge("A", "B"); g.add_edge("B", "C")
    print("Task 9 A to C connected:", g.is_connected("A", "C"))

    cv = CompositeValidator([RequiredValidator(), EmailValidator()])
    print("Task 10 Valid 'a@b.com':", cv.validate("a@b.com"))
    print("Task 10 Valid 'bad':", cv.validate("bad"))

    print("Task 11 Manager Pay:", ManagerEmployee().calculate_pay())

    s = FactoryShape.create("circle", 5)
    print("Task 12 Area:", s.area())

    stock = StockPrice("AAPL", 150)
    inv = Investor("John")
    stock.attach(inv)
    stock.price = 155

    acc = PremiumCheckingAccount(1000)
    print("Task 14 Interest:", acc.get_interest())

    print("Task 15: ReportService logic implemented.")

    print("--- Tests Finished ---")

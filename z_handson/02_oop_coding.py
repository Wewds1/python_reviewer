# Coding Challenges - Module 2 (Beginner)
# Written by a Junior Engineer

# 1. Write a Dog class with name and breed, and a method bark().
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        return "Woof! My name is " + self.name + " and I am a " + self.breed + "."

# 2. Write a Rectangle class with width and height, and methods for area() and perimeter().
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        # area is width times height
        return self.width * self.height

    def perimeter(self):
        # perimeter is 2 times (width + height)
        return 2 * (self.width + self.height)

# 3. Write a Person class with first_name and last_name, and a method full_name().
class Person:
    def __init__(self, first_name, last_name):
        self.first_name = first_name
        self.last_name = last_name

    def full_name(self):
        return self.first_name + " " + self.last_name

# 4. Write a Book class with title, author, and pages, and a method that reports whether it's a "long" book (over 400 pages).
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

    def is_long(self):
        if self.pages > 400:
            return True
        else:
            return False

# 5. Write a Circle class with radius, and methods area() and circumference().
import math

class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        # area = pi * r^2
        return math.pi * (self.radius ** 2)

    def circumference(self):
        # circumference = 2 * pi * r
        return 2 * math.pi * self.radius

# 6. Write a Car class with make, model, and year, and a method age(current_year).
class Car:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    def age(self, current_year):
        return current_year - self.year

# 7. Write a BankAccount class with a balance, and deposit()/withdraw() methods that prevent overdrawing.
class BankAccount:
    def __init__(self, initial_balance=0):
        self.balance = initial_balance

    def deposit(self, amount):
        self.balance = self.balance + amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            print("Insufficient funds!")
            return self.balance
        else:
            self.balance = self.balance - amount
            return self.balance

# 8. Write a Student class with name and a list of grades, and a method average().
class Student:
    def __init__(self, name, grades):
        self.name = name
        self.grades = grades # this should be a list of numbers

    def average(self):
        if len(self.grades) == 0:
            return 0
        total = 0
        for g in self.grades:
            total = total + g
        return total / len(self.grades)

# 9. Write a Playlist class that holds a list of song titles, with add_song() and remove_song() methods.
class Playlist:
    def __init__(self, name):
        self.name = name
        self.songs = []

    def add_song(self, title):
        self.songs.append(title)

    def remove_song(self, title):
        if title in self.songs:
            self.songs.remove(title)
        else:
            print("Song not found in playlist")

# 10. Write a Temperature class storing a value in Celsius, with a method to_fahrenheit().
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    def to_fahrenheit(self):
        return (self.celsius * 9/5) + 32

# 11. Write a class Counter with a method increment() and a method reset().
class Counter:
    def __init__(self):
        self.count = 0

    def increment(self):
        self.count = self.count + 1
        return self.count

    def reset(self):
        self.count = 0
        return self.count

# 12. Write a Shape class with a class attribute sides and an instance method that reports it.
class Shape:
    sides = 0 # class attribute

    def report_sides(self):
        return "This shape has " + str(self.sides) + " sides."

# 13. Write a Product class with name and price, and a class method on_sale(cls, name, original_price, discount_percent) that returns a discounted product.
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    @classmethod
    def on_sale(cls, name, original_price, discount_percent):
        discount_amount = original_price * (discount_percent / 100)
        sale_price = original_price - discount_amount
        # create a new product instance with the sale price
        return cls(name, sale_price)

# 14. Write a Timer class with start() and stop() methods that report elapsed time (simulated).
class Timer:
    def __init__(self):
        self.start_time = 0
        self.end_time = 0
        self.is_running = False

    def start(self):
        # simulating starting at time 0
        self.start_time = 0
        self.is_running = True
        print("Timer started.")

    def stop(self):
        # simulating ending at time 10 for simplicity
        self.end_time = 10
        self.is_running = False
        elapsed = self.end_time - self.start_time
        return elapsed

# 15. Write a Wallet class with a balance, and add_funds()/spend() methods, raising an exception if spending exceeds the balance.
class Wallet:
    def __init__(self, balance=0):
        self.balance = balance

    def add_funds(self, amount):
        self.balance = self.balance + amount
        return self.balance

    def spend(self, amount):
        if amount > self.balance:
            raise ValueError("Not enough money in wallet!")
        self.balance = self.balance - amount
        return self.balance

# 16. Write a Movie class with title, genre, and rating, and a static method that validates a rating is between 0 and 10.
class Movie:
    def __init__(self, title, genre, rating):
        self.title = title
        self.genre = genre
        self.rating = rating

    @staticmethod
    def validate_rating(rating):
        if rating >= 0 and rating <= 10:
            return True
        else:
            return False

# 17. Write a Recipe class with a list of ingredients and a method ingredient_count().
class Recipe:
    def __init__(self, name, ingredients):
        self.name = name
        self.ingredients = ingredients # list

    def ingredient_count(self):
        return len(self.ingredients)

# 18. Write an Employee class with name and salary, and a method give_raise(percent).
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def give_raise(self, percent):
        increase = self.salary * (percent / 100)
        self.salary = self.salary + increase
        return self.salary

# 19. Write a Deck class representing a deck of cards as a list of strings, with a method shuffle() and a method draw().
import random

class Deck:
    def __init__(self):
        self.cards = ["Ace of Spades", "2 of Spades", "3 of Spades", "King of Hearts", "Queen of Diamonds"] # simplified deck

    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        if len(self.cards) == 0:
            return "No cards left!"
        return self.cards.pop()

# 20. Write a Thermostat class with a target_temperature property that rejects values outside a sensible range (50 to 90).
class Thermostat:
    def __init__(self, temp=70):
        self._target_temperature = temp

    @property
    def target_temperature(self):
        return self._target_temperature

    @target_temperature.setter
    def target_temperature(self, value):
        if value < 50 or value > 90:
            print("Error: Temperature must be between 50 and 90.")
        else:
            self._target_temperature = value

# --- Testing the classes ---
if __name__ == "__main__":
    print("--- Testing OOP Beginner Challenges ---")

    d = Dog("Buddy", "Golden Retriever")
    print("Task 1:", d.bark())

    r = Rectangle(10, 5)
    print("Task 2 Area:", r.area(), "Perim:", r.perimeter())

    p = Person("John", "Doe")
    print("Task 3:", p.full_name())

    b = Book("The Big Book", "Author A", 500)
    print("Task 4 Long?:", b.is_long())

    c = Circle(7)
    print("Task 5 Area:", round(c.area(), 2))

    car = Car("Toyota", "Camry", 2015)
    print("Task 6 Age in 2026:", car.age(2026))

    acc = BankAccount(100)
    acc.deposit(50)
    acc.withdraw(200) # should fail
    print("Task 7 Balance:", acc.balance)

    stu = Student("Alice", [80, 90, 100])
    print("Task 8 Average:", stu.average())

    pl = Playlist("My Hits")
    pl.add_song("Song 1")
    pl.add_song("Song 2")
    pl.remove_song("Song 1")
    print("Task 9 Songs:", pl.songs)

    temp = Temperature(25)
    print("Task 10 Fahr:", temp.to_fahrenheit())

    cnt = Counter()
    cnt.increment()
    cnt.increment()
    print("Task 11 Count:", cnt.count)

    sh = Shape()
    sh.sides = 4
    print("Task 12:", sh.report_sides())

    prod = Product.on_sale("Laptop", 1000, 10)
    print("Task 13 Sale Price:", prod.price)

    tm = Timer()
    tm.start()
    print("Task 14 Elapsed:", tm.stop())

    wal = Wallet(50)
    try:
        wal.spend(60)
    except ValueError as e:
        print("Task 15 Caught:", e)

    print("Task 16 Validate 8:", Movie.validate_rating(8))
    print("Task 16 Validate 12:", Movie.validate_rating(12))

    rec = Recipe("Cake", ["Flour", "Sugar", "Eggs"])
    print("Task 17 Count:", rec.ingredient_count())

    emp = Employee("Bob", 50000)
    emp.give_raise(10)
    print("Task 18 New Salary:", emp.salary)

    dk = Deck()
    dk.shuffle()
    print("Task 19 Drew:", dk.draw())

    ther = Thermostat()
    ther.target_temperature = 100 # should fail
    print("Task 20 Temp:", ther.target_temperature)

    print("--- Tests Finished ---")

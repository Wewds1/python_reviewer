# Lesson 5: Methods

## 1. Learning objectives

By the end of this lesson you should be able to:

- Distinguish instance methods, class methods, and static methods, and know exactly when each is the right tool
- Explain what `cls` is and how it differs from `self`
- Recognize the handful of magic methods you'll use constantly, and understand the protocol they plug into
- Explain how Python handles "overloading" and "overriding" differently from languages that support true method overloading

## 2. Prerequisites

Lessons 1 through 4. You've been using instance methods informally throughout; this lesson makes the full picture explicit.

## 3. Introduction

Not every method on a class needs access to a specific instance. Some belong to the class as a whole, and some don't need any class or instance context at all, they're just related utility logic that makes sense to keep bundled with the class for organizational reasons. Python gives you three distinct method types for these three situations, and picking the right one is a small design decision that shows up constantly in real code and in interviews.

## 4. Theory

**Instance methods** are what you've used throughout this module: they take `self` as their first parameter and operate on one specific object's data.

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    def area(self):  # instance method
        return 3.14159 * self.radius ** 2
```

**Class methods** take `cls` (the class itself) instead of `self`, and operate on class-level data or serve as alternate constructors, as previewed in Lesson 3.

```python
class Circle:
    unit = "cm"

    @classmethod
    def describe_unit(cls):  # class method
        return f"Measured in {cls.unit}"
```

**Static methods** take neither `self` nor `cls`. They're regular functions that happen to live inside a class because they're conceptually related to it, even though they don't need any instance or class data to do their job.

```python
class Circle:
    @staticmethod
    def is_valid_radius(value):  # static method
        return value > 0
```

## 5. Why this concept exists

Not every operation related to a class needs the same kind of access. An instance method needs a specific object's data (calculating one circle's area). A class method needs shared, class-level context, or needs to construct new instances without yet having one to work from. A static method needs neither, it's just a helper that's thematically grouped with the class for readability, rather than scattered as a loose function elsewhere. Having three distinct tools, instead of forcing everything through `self`, lets a class's method signatures honestly communicate what each method actually needs.

## 6. Internal behavior

Under the hood, `@classmethod` and `@staticmethod` are descriptors, a mechanism Python uses to control what happens when an attribute is accessed through a class or instance. When you call `circle.area()`, Python's normal method-binding behavior automatically supplies `self` as `circle`. The `@classmethod` decorator changes that binding behavior so that `cls` gets supplied as the class itself, `Circle`, regardless of whether you call it through the class (`Circle.describe_unit()`) or through an instance (`circle.describe_unit()`), always the class. The `@staticmethod` decorator disables automatic binding entirely, so the method behaves exactly like a plain function that just happens to be namespaced inside the class.

## 7. Real-world analogy

Picture a car manufacturing plant. An instance method is like adjusting the seat position on one specific car, it only makes sense in the context of that particular vehicle. A class method is like updating the factory's standard paint color for every future car rolling off the line, it operates on something shared across the whole production line, not any one existing car. A static method is like the plant's parking validation stamp machine, it doesn't care about any specific car or the factory's shared settings, it's just a utility that happens to live at the plant because that's where it's used.

## 8. Enterprise use cases

Alternate constructors (`User.from_json(data)`, `Order.from_database_row(row)`) are almost always class methods, since they need to build new instances without an existing `self` to work from. Utility validation logic (`Email.is_valid_format(text)`) that doesn't depend on any particular instance's data is a natural static method, kept inside the class purely for discoverability and organization rather than scattered as an unrelated free function. Shared counters or registries tracked across every instance of a type (how many active database connections currently exist) are typically managed through class methods operating on class attributes.

## 9. UML-style explanation

```
┌─────────────────────────────────────┐
│                Circle                   │
├─────────────────────────────────────┤
│ - radius: float                          │
│ - unit: str  {class-level}                │
├─────────────────────────────────────┤
│ + area(): float                            │
│ + describe_unit(): str  {classmethod}       │
│ + is_valid_radius(value): bool {static}      │
└─────────────────────────────────────┘
```

Some UML tooling marks static and class methods with distinct annotations, since a reader scanning the class needs to know at a glance which methods need an actual instance to call meaningfully and which don't.

## 10. Syntax

```python
class Order:
    tax_rate = 0.08  # class attribute

    def __init__(self, subtotal):
        self.subtotal = subtotal

    def total(self):  # instance method
        return self.subtotal * (1 + Order.tax_rate)

    @classmethod
    def set_tax_rate(cls, new_rate):  # class method
        cls.tax_rate = new_rate

    @staticmethod
    def is_valid_amount(amount):  # static method
        return amount >= 0

order = Order(100)
print(order.total())            # uses the current tax rate

Order.set_tax_rate(0.10)         # changes the tax rate for every Order
print(order.total())             # reflects the updated rate

print(Order.is_valid_amount(-5)) # False — doesn't need any Order instance at all
```

**A first look at magic methods.** These are the double-underscore methods (`__init__`, `__eq__`, `__str__`, `__len__`, and others) that let your custom classes plug into Python's built-in syntax and behavior. This lesson introduces the concept; Lesson 8 (Polymorphism) covers operator overloading with magic methods in depth.

```python
class Money:
    def __init__(self, amount):
        self.amount = amount

    def __str__(self):  # controls what print(obj) and str(obj) show
        return f"${self.amount:.2f}"

    def __eq__(self, other):  # controls what == means for this class
        return self.amount == other.amount

m1 = Money(19.99)
print(m1)              # $19.99 — uses __str__ automatically
print(m1 == Money(19.99))  # True — uses __eq__ automatically
```

## 11. Step-by-step examples

**Easy — instance vs. static method side by side:**

```python
class TemperatureConverter:
    def __init__(self, celsius):
        self.celsius = celsius

    def to_fahrenheit(self):  # needs this specific object's data
        return self.celsius * 9 / 5 + 32

    @staticmethod
    def is_freezing(celsius):  # doesn't need any specific instance
        return celsius <= 0

t = TemperatureConverter(-5)
print(t.to_fahrenheit())
print(TemperatureConverter.is_freezing(-5))
```

**Medium — a class method used as an alternate constructor, alongside a regular instance method:**

```python
class Pizza:
    def __init__(self, toppings):
        self.toppings = toppings

    @classmethod
    def margherita(cls):
        return cls(["tomato", "mozzarella", "basil"])

    def describe(self):
        return f"Pizza with: {', '.join(self.toppings)}"

custom = Pizza(["pepperoni", "mushroom"])
classic = Pizza.margherita()

print(custom.describe())
print(classic.describe())
```

**Hard — class method modifying shared state, and every instance reflecting the change immediately:**

```python
class FeatureFlag:
    enabled_globally = False

    def __init__(self, name):
        self.name = name

    def is_active(self):
        return FeatureFlag.enabled_globally

    @classmethod
    def enable_all(cls):
        cls.enabled_globally = True

flag_a = FeatureFlag("dark_mode")
flag_b = FeatureFlag("beta_search")

print(flag_a.is_active(), flag_b.is_active())  # False False

FeatureFlag.enable_all()

print(flag_a.is_active(), flag_b.is_active())  # True True — both instances see the shared change
```

## 12. Common mistakes

**Using `self` where `cls` was intended, or vice versa.** Writing an instance method when you meant a class method (or forgetting the `@classmethod` decorator entirely) means `cls` won't be automatically supplied, and the method will misbehave or error out.

**Making everything a static method "to be safe."** If a method genuinely needs instance data, forcing it to be static means manually threading that data through as a parameter every time, instead of letting Python hand it to you automatically via `self`. Static methods should be reserved for logic that truly has no dependency on instance or class state.

**Forgetting that class methods affect every instance simultaneously,** which is exactly the intended behavior when you want it, and exactly the source of confusing bugs when you didn't realize a method was a class method and expected it to only affect one object.

## 13. Debugging tips

If a method call raises an unexpected `TypeError` about argument counts, check whether it's missing its `@classmethod` or `@staticmethod` decorator, or has one it shouldn't. If a change through one instance is unexpectedly visible on every other instance, check whether the method making that change is a class method modifying class-level state, rather than an instance method you assumed was scoped to just one object.

## 14. Best practices

Default to instance methods; only reach for `@classmethod` when you specifically need class-level context or you're building an alternate constructor, and only reach for `@staticmethod` when a method genuinely doesn't need any instance or class data at all. Name alternate constructors built with `@classmethod` descriptively (`from_json`, `from_csv_row`, `square`), so the call site reads clearly.

## 15. Performance considerations

The difference in raw execution speed between instance, class, and static methods is negligible for virtually all real code; this is a design decision, not a performance one. Choosing the right method type primarily affects readability and correctness, not runtime speed.

## 16. Code style

Always include the `@classmethod` or `@staticmethod` decorator explicitly, never rely on positional convention alone. Name the first parameter of a class method `cls`, exactly as consistently as `self` is used for instance methods, since deviating from either convention will confuse any experienced Python reader.

## 17. Interview questions with model answers

**Q: What's the difference between a class method and a static method?**

A class method receives the class itself as its first argument (`cls`), giving it access to class-level attributes and the ability to construct new instances. A static method receives neither `self` nor `cls`, it behaves like a regular function that's just organizationally grouped inside the class. The interviewer is checking whether you understand this is about what context each method type receives automatically, not just a stylistic difference.

**Q: When would you use a class method as an alternate constructor?**

When there's a meaningfully different, clearly named way to build an instance that doesn't map cleanly onto the primary `__init__` signature, for example building a `User` from a raw dictionary pulled out of an API response versus building one from individually provided fields. A strong answer references something like `datetime.fromtimestamp()` from the standard library as a familiar real-world example of this exact pattern.

**Q: Does Python support method overloading the way Java does?**

Not in the traditional sense of defining the same method name multiple times with different signatures, a later definition simply replaces an earlier one with the same name. Python handles the same use cases through default arguments, `*args`/`**kwargs`, or, for construction specifically, alternate `@classmethod` constructors. Method overriding, redefining a method in a subclass, is different from overloading and is fully supported, covered in depth in Lesson 7.

## 18. Knowledge check

1. What's the first parameter of a class method called, by convention, and what does it receive?
2. When would a static method be the right choice over an instance method?
3. Why doesn't Python support true method overloading the way some other languages do?
4. What's a common real-world use case for a class method?

## 19. Hands-on exercises

**Easy**

1. Write a `Square` class with an instance method `area()` and a static method `is_valid_side(value)` that checks the value is positive.
2. Write a class method on a `Book` class that acts as an alternate constructor, `Book.untitled()`, returning a book with the title set to `"Untitled"`.
3. Add a `__str__` method to any class from a previous lesson and demonstrate that `print()` now uses it automatically.

**Medium**

4. Write a `Language` class with a class-level attribute tracking the total number of `Language` objects created, updated through a class method, and an instance method that reports each language's name alongside the current total count.
5. Write a `Discount` class with a class method `set_global_rate(cls, rate)` that changes a shared discount rate affecting every instance, and demonstrate the change propagating across two separately created instances.
6. Write a static method `Validator.is_strong_password(password)` that checks a password is at least 8 characters and contains both a letter and a number, with no dependency on any instance or class data.

**Hard**

7. Build a `Logger` class where a class method tracks and exposes a running count of how many log messages have been recorded across every `Logger` instance combined, while each instance also tracks its own individual message count separately, demonstrating both the shared and independent counts staying correct simultaneously.
8. Design a `Shape` class (in preparation for inheritance in the next lesson) with an instance method `area()` that raises `NotImplementedError` by default, a class method `unit_square(cls)` alternate constructor, and a static method `validate_dimension(value)`, and write test code exercising all three method types correctly.

## 20. Stretch challenge

Build a small `Registry` pattern: a class method that maintains a class-level dictionary mapping names to instances as they're created, so that any instance can be looked up later by name through a class method like `Registry.find("some_name")`, without needing to keep a separate reference to it yourself. Be deliberate about where the shared dictionary lives (class attribute, initialized carefully, not as a mutable default trap) and write test code proving that instances really can be retrieved by name after creation, from anywhere, using only the class method.

## 21. Summary

Instance methods operate on one object's data via `self`. Class methods operate on the class itself via `cls`, most commonly as alternate constructors or to manage shared state. Static methods are ordinary functions organizationally grouped inside a class, needing neither. Python doesn't support true method overloading, defaults and alternate constructors cover that ground instead, but it fully supports overriding, which the next lesson, on inheritance, builds on directly.

## 22. Additional resources

- [Python official docs: classmethod](https://docs.python.org/3/library/functions.html#classmethod)
- [Python official docs: staticmethod](https://docs.python.org/3/library/functions.html#staticmethod)
- [Python official docs: Special method names](https://docs.python.org/3/reference/datamodel.html#special-method-names)

# Lesson 4: Instance Variables vs. Class Variables

## 1. Learning objectives

By the end of this lesson you should be able to:

- Explain the difference between an instance attribute and a class attribute, precisely
- Predict, without running the code, when a change to a class attribute is visible across every instance and when it isn't
- Identify shadowing when it happens and explain why it happens
- Choose correctly between an instance and a class attribute when designing a class
- Avoid the mutable-class-attribute bug, which is the class-level cousin of Module 1's mutable default argument bug

## 2. Prerequisites

Lessons 1 through 3. You need constructors solid before this lesson's distinctions will make sense.

## 3. Introduction

Every attribute you've written so far in this module has been an instance attribute, something set inside `__init__` via `self.something = value`, unique to each object. There's a second kind: a class attribute, defined directly on the class itself, shared by every instance unless something intervenes. The two look almost identical when you read from them, and behave completely differently when you write to them, which is exactly the gap where bugs live.

## 4. Theory

```python
class Employee:
    company = "Acme Corp"  # class attribute — shared by all instances

    def __init__(self, name):
        self.name = name  # instance attribute — unique per object

alice = Employee("Alice")
bob = Employee("Bob")

print(alice.company, bob.company)  # Acme Corp Acme Corp — both see the same class attribute
```

Reading `alice.company` works because Python, when it can't find `company` directly on the instance, falls back to checking the class. Both `alice` and `bob` share the exact same `company` value, stored once, on the class, not duplicated per object.

## 5. Why this concept exists

Some data genuinely belongs to every instance of a class collectively, a company name shared by every employee object, a tax rate shared by every transaction, a running count of how many objects have been created, rather than to any one instance individually. Without class attributes, you'd have to duplicate that shared value into every single instance's own storage, wasting memory and creating a coordination nightmare the moment that shared value needs to change everywhere at once.

## 6. Internal behavior

A class attribute lives in the class object's own namespace, created once when the class is defined. An instance attribute lives in the individual object's own `__dict__`, created when `self.something = value` runs, typically inside `__init__`. When you read `instance.attribute`, Python checks the instance's own `__dict__` first; if it's not found there, it checks the class's namespace next. This lookup order is exactly why reading a class attribute through an instance works transparently, and it's also exactly the mechanism behind shadowing, covered below.

## 7. Real-world analogy

Think of a class attribute as the company handbook, one shared document that applies to every employee unless a specific employee's contract explicitly overrides a clause. An instance attribute is that individual's personal contract details, their own salary, their own start date, which belongs to them alone. If the company updates the handbook (changes the class attribute), every employee who hasn't been given a personal override sees the update immediately. But the moment an employee gets an individually negotiated clause (an instance attribute of the same name), that personal version takes precedence for them specifically, and further changes to the handbook no longer affect that one employee's copy.

## 8. Enterprise use cases

Class attributes are the natural home for configuration values shared across every instance of a type: a default currency for every `Invoice`, a shared connection pool reference for every `DatabaseRecord` subclass, a running total of how many `Session` objects have been created for monitoring purposes. Instance attributes hold everything specific to one particular record: this invoice's amount, this session's user id. Mixing the two up, putting genuinely per-object data on the class, is a design mistake that tends to surface as bizarre, hard-to-explain cross-contamination between what should be independent objects.

## 9. UML-style explanation

```
┌───────────────────────────────┐
│            Employee              │
├───────────────────────────────┤
│ - company: str  {class-level}     │
│ - name: str      {instance-level}  │
├───────────────────────────────┤
│ + __init__(name)                   │
└───────────────────────────────┘
```

Some UML conventions underline class-level attributes and methods to visually distinguish them from instance-level ones. That underline is doing real work: it's telling you, at a glance, whether a given piece of data is shared or individual, which is exactly the distinction this lesson is about.

## 10. Syntax

```python
class Counter:
    total_created = 0  # class attribute

    def __init__(self):
        Counter.total_created += 1  # modifying the class attribute explicitly
        self.id = Counter.total_created  # instance attribute, unique per object

a = Counter()
b = Counter()
c = Counter()
print(a.id, b.id, c.id)          # 1 2 3
print(Counter.total_created)      # 3
```

Note the deliberate `Counter.total_created += 1`, referencing the class explicitly, rather than `self.total_created += 1`. That distinction is the entire subject of the next section.

## 11. Step-by-step examples

**Easy — reading a shared class attribute through multiple instances:**

```python
class Robot:
    manufacturer = "Cyberdyne"

    def __init__(self, model):
        self.model = model

r1 = Robot("T-800")
r2 = Robot("T-1000")
print(r1.manufacturer, r2.manufacturer)  # both show Cyberdyne
```

**Medium — shadowing: what happens when you assign to `self.attribute` for something that started as a class attribute:**

```python
class Robot:
    manufacturer = "Cyberdyne"

    def __init__(self, model):
        self.model = model

r1 = Robot("T-800")
r2 = Robot("T-1000")

r1.manufacturer = "Skynet Industries"  # this does NOT change the class attribute

print(r1.manufacturer)  # Skynet Industries — r1 now has its own instance attribute
print(r2.manufacturer)  # Cyberdyne — completely unaffected
print(Robot.manufacturer)  # Cyberdyne — the class attribute itself never changed
```

`r1.manufacturer = "Skynet Industries"` doesn't modify the shared class attribute at all. It creates a brand new instance attribute on `r1` specifically, one that happens to share the same name, which then shadows the class attribute whenever you look it up through `r1`. `r2` and the class itself are completely untouched.

**Hard — the mutable class attribute trap, the class-level sibling of Module 1's mutable default argument bug:**

```python
class ShoppingCart:
    items = []  # DANGER — shared across every instance

    def add_item(self, item):
        self.items.append(item)

cart1 = ShoppingCart()
cart2 = ShoppingCart()

cart1.add_item("apple")
print(cart2.items)  # ['apple'] — surprise! cart2 sees cart1's item
```

Because `items` is a class attribute pointing at a single mutable list, `.append()` mutates that one shared list in place, and every instance sees the change, since none of them ever created their own `items` list. The fix is the same shape as the mutable default argument fix from Module 1: move the mutable data into `__init__` as an instance attribute instead.

```python
class ShoppingCart:
    def __init__(self):
        self.items = []  # each instance now gets its own independent list

    def add_item(self, item):
        self.items.append(item)
```

## 12. Common mistakes

**Using a mutable class attribute (a list, dict, or set) for data that should be per-instance,** exactly the bug shown above. This is genuinely one of the most common OOP mistakes in Python, and it's a direct cousin of a mistake you already learned to avoid in Module 1.

**Confusing shadowing with mutation.** `self.attribute = new_value` never changes the class attribute, it always creates or overwrites an instance attribute. Only `ClassName.attribute = new_value`, referencing the class directly, actually changes the shared value.

**Assuming a class attribute updates automatically across all instances after shadowing has already occurred.** Once an instance has its own shadowing attribute, it's permanently disconnected from future changes to the class attribute of the same name, until that instance attribute is explicitly deleted.

## 13. Debugging tips

If instances of the same class seem to be mysteriously sharing data they shouldn't, check whether the attribute in question is defined at the class level with a mutable default (a list, dict, or set) rather than being set fresh inside `__init__`. If a change to a class attribute isn't showing up on an instance you expect it to affect, check whether that instance has already shadowed it with its own instance attribute of the same name.

## 14. Best practices

Default to instance attributes, set inside `__init__`, for anything that's conceptually per-object. Reserve class attributes for genuinely shared, ideally immutable, data: configuration constants, default values that aren't mutable containers, or counters that are deliberately meant to track something across all instances. Never use a mutable object as a class attribute unless you specifically intend for every instance to share and mutate the exact same object, and even then, document that intention clearly, since it'll surprise the next person who reads the class.

## 15. Performance considerations

Class attributes are stored once and shared, so they're marginally more memory-efficient than duplicating the same immutable value onto every single instance, an advantage that only becomes meaningful at very large object counts. This is a minor consideration; correctness (avoiding the mutable-sharing trap) matters far more than the small memory savings for the vast majority of real code.

## 16. Code style

Reference class attributes through the class name (`ClassName.attribute`) when you specifically intend to modify the shared value, and through `self` only when reading, to make the distinction visually clear to whoever reads the code later. Keep class-level attributes near the top of the class body, before `__init__`, which is where Python convention expects to find them.

## 17. Interview questions with model answers

**Q: What's the difference between an instance attribute and a class attribute?**

An instance attribute belongs to one specific object and is typically set inside `__init__` via `self.attribute = value`. A class attribute is defined directly on the class body and is shared across every instance of that class unless a specific instance shadows it with its own attribute of the same name. The interviewer is listening for the word "shadow" or an equivalent explanation, since that's the part that trips people up in practice.

**Q: Why is a mutable class attribute, like a list, considered dangerous?**

Because every instance that hasn't explicitly created its own version shares that exact same list object. Calling `.append()` through one instance mutates the shared list, and that change becomes visible through every other instance too, which is almost never the intended behavior. The fix is to initialize that kind of data inside `__init__` as an instance attribute instead, giving each object its own independent copy.

**Q: If you set `instance.attribute = value` for an attribute that started as a class attribute, what actually happens?**

It creates a new instance attribute on that specific object, shadowing the class attribute of the same name for that instance going forward. It does not modify the class attribute itself, and every other instance, along with the class, remains unaffected. A candidate who can walk through this with a concrete example, not just the definition, is demonstrating real understanding rather than memorized terminology.

## 18. Knowledge check

1. If a class attribute is changed via `ClassName.attribute = new_value`, do existing instances that haven't shadowed it see the change?
2. What specifically causes the mutable class attribute bug?
3. What's the fix for a class using a mutable list as a class attribute meant to hold per-instance data?
4. Does `self.attribute = value` ever modify a class attribute directly?

## 19. Hands-on exercises

**Easy**

1. Write a `Car` class with a class attribute `wheels = 4` and an instance attribute `color`, and print both for two different car instances.
2. Demonstrate shadowing: create an instance, override its `wheels` value individually, and show that a second instance still reports the class default.
3. Write a class attribute `species = "Homo sapiens"` on a `Person` class and confirm it's shared across three different instances by printing all three.

**Medium**

4. Write a `Counter` class that uses a class attribute to track how many instances have been created in total, giving each instance a unique instance-level `id` based on that count, matching the pattern shown in this lesson.
5. Deliberately write a class with a mutable class attribute bug (a shared list or dict), demonstrate the bug with two instances, then fix it.
6. Write a `Config` class with class-level settings (like `max_retries = 3`) that every instance reads by default, but allow one specific instance to override `max_retries` for itself without affecting the class-wide default.

**Hard**

7. Design a `Student` class where `school_name` is a class attribute shared by all students, but a specific transfer student needs a different, individually assigned school name, without affecting any other student object or the class-level default, and write code proving both behaviors work correctly.
8. Write a `GameSession` class that uses a class attribute to enforce a maximum number of concurrent sessions (raise a custom exception if a new session would exceed the limit), correctly incrementing and decrementing that shared counter as sessions are created and explicitly closed.

## 20. Stretch challenge

Design a small `Employee` class hierarchy (you haven't formally covered inheritance yet, so for now just build one `Employee` class) that uses a class attribute to track total payroll across every employee ever created, updated correctly in `__init__` when a new employee is added and in a `give_raise` method when an existing employee's salary changes. Make sure the total stays accurate under both situations, adding new employees and raising existing ones, and write test code that creates several employees, gives a few of them raises, and confirms the class-level total matches the sum of all individual salaries at the end.

## 21. Summary

Instance attributes belong to one object; class attributes are shared across every instance unless something shadows them. Reading either looks the same through `self`, but writing through `self` always creates or overwrites an instance attribute, never the shared class-level one. The single most important practical takeaway from this lesson is the mutable class attribute trap: never use a mutable object as a class attribute for data that's supposed to be independent per instance, initialize it in `__init__` instead.

## 22. Additional resources

- [Python official docs: Class and Instance Variables](https://docs.python.org/3/tutorial/classes.html#class-and-instance-variables)
- [Python official docs: Attribute lookup order](https://docs.python.org/3/reference/datamodel.html#object.__getattribute__)
- [Real Python: Class vs. Instance Attributes](https://realpython.com/python-class-attributes/)

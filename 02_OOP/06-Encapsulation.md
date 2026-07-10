# Lesson 6: Encapsulation

## 1. Learning objectives

By the end of this lesson you should be able to:

- Explain what encapsulation actually protects against, not just recite "information hiding"
- Use Python's public, protected, and private naming conventions correctly, and understand that they're conventions, not enforcement
- Explain name mangling and why Python implements privacy the way it does
- Write clean getters and setters using `@property`, instead of Java-style `get_x()`/`set_x()` methods
- Use property setters and deleters to validate and control attribute access

## 2. Prerequisites

Lessons 1 through 5. Encapsulation is really about controlling access to instance attributes and methods you've already been building.

## 3. Introduction

So far, every attribute in this module has been freely readable and writable from outside the class: `account.balance = -500` would work without complaint, even though it's nonsensical. Encapsulation is about closing that gap, controlling how an object's internal state can be read or changed from the outside, so that an object can actually enforce its own rules instead of relying on every caller to behave responsibly.

## 4. Theory

Encapsulation bundles data with the methods that operate on it (which you've already been doing since Lesson 2) and restricts direct access to that data from outside the class, funneling changes through controlled methods instead. Python's approach is different from languages like Java, which enforce access restrictions at the compiler level. Python uses naming conventions, backed by a small amount of actual language mechanics for the strictest level, and largely trusts developers to respect them.

- **Public** (`self.name`): no restriction, accessible from anywhere. The default.
- **Protected** (`self._name`, single leading underscore): a convention signaling "internal use, subclasses may access this, but outside code shouldn't." Python does nothing to actually enforce this.
- **Private** (`self.__name`, double leading underscore): triggers name mangling, a real mechanic that makes accidental external access meaningfully harder, though not strictly impossible.

## 5. Why this concept exists

Without any access control, any code anywhere can reach directly into an object and set it into an invalid state, `account.balance = -9999`, bypassing every validation rule the class's methods were designed to enforce. Encapsulation exists so a class can guarantee its own invariants: as long as external code is forced to go through controlled methods (or properties) to change internal state, the class can validate every change and reject the ones that don't make sense, keeping every object it manages in a consistent, trustworthy state.

## 6. Internal behavior

Single-underscore attributes (`self._balance`) are stored and accessed completely normally, Python treats the underscore as just another character in the name; it's a pure convention with zero enforcement. Double-underscore attributes (`self.__balance`) trigger name mangling: Python internally rewrites the name to `_ClassName__balance`, which makes it awkward, though not impossible, to access accidentally from outside the class or from an unrelated subclass. This is why `self.__balance` inside a class works exactly as expected internally, but `obj.__balance` from outside raises an `AttributeError`, the attribute genuinely isn't stored under that literal name anymore.

```python
class Account:
    def __init__(self, balance):
        self.__balance = balance

acc = Account(100)
print(acc._Account__balance)  # 100 — the mangled name, technically still reachable
```

## 7. Real-world analogy

Think of a car's engine. As a driver, you interact with a small, controlled interface: the accelerator pedal, the brake, the steering wheel. You don't reach directly into the engine block and manually adjust the fuel injection timing while driving, not because it's physically impossible, but because the entire system is designed to funnel your intent through a safe, validated interface. Public attributes are the dashboard controls. Private attributes are the engine internals: technically reachable if you really wanted to pop the hood, but not something the design intends or expects you to touch directly.

## 8. Enterprise use cases

Encapsulation is what makes a class's internal implementation changeable without breaking every piece of code that uses it. If a `BankAccount`'s balance is exposed as a raw public attribute, any code anywhere in a large system could be silently setting it directly, and refactoring how balances are stored later (adding an audit log on every change, say) means hunting down every single place that touched `.balance` directly. If access was always funneled through a `deposit()`/`withdraw()` method or a `@property`, that refactor happens in one place, the class itself, with zero changes needed anywhere else in the codebase. This is precisely the property that makes large, long-lived enterprise systems survivable to maintain.

## 9. UML-style explanation

```
┌─────────────────────────────────┐
│              Account                │
├─────────────────────────────────┤
│ - __balance: float  (private)         │
├─────────────────────────────────┤
│ + deposit(amount): None                │
│ + withdraw(amount): None                │
│ + balance: float  (property, read-only)  │
└─────────────────────────────────┘
```

UML's `-` prefix (private) and `+` prefix (public), introduced back in Lesson 1, are exactly encapsulation's visibility levels made visual. A well-designed UML diagram should make it immediately obvious which parts of a class are meant to be touched from outside and which aren't.

## 10. Syntax

**Naming conventions:**

```python
class Account:
    def __init__(self, balance):
        self.owner = owner if False else None  # public, unrestricted (illustrative only)
        self._internal_note = "audit pending"    # protected, convention only
        self.__balance = balance                  # private, name-mangled
```

**Getters and setters, the old, non-idiomatic way (shown so you recognize it, not so you write it):**

```python
class Account:
    def __init__(self, balance):
        self.__balance = balance

    def get_balance(self):
        return self.__balance

    def set_balance(self, value):
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self.__balance = value
```

This works, but it's not idiomatic Python, and `account.get_balance()` everywhere instead of `account.balance` is exactly the kind of thing that marks code as translated from Java rather than written natively in Python.

**The idiomatic way, using `@property`:**

```python
class Account:
    def __init__(self, balance):
        self.__balance = balance

    @property
    def balance(self):  # the getter
        return self.__balance

    @balance.setter
    def balance(self, value):  # the setter, same name, different decorator
        if value < 0:
            raise ValueError("Balance cannot be negative")
        self.__balance = value

    @balance.deleter
    def balance(self):  # the deleter
        print("Clearing balance")
        del self.__balance

acc = Account(100)
print(acc.balance)      # reads like a plain attribute, but calls the getter
acc.balance = 250        # reads like a plain assignment, but calls the setter and validates
# acc.balance = -50      # would raise ValueError
del acc.balance          # calls the deleter
```

This is the pattern worth internalizing: from the outside, `acc.balance` looks exactly like a normal attribute, clean and Pythonic, but every read and write is quietly funneled through your controlled methods underneath.

## 11. Step-by-step examples

**Easy — a read-only property, no setter defined:**

```python
class Circle:
    def __init__(self, radius):
        self.radius = radius

    @property
    def area(self):
        return 3.14159 * self.radius ** 2

c = Circle(5)
print(c.area)     # computed on access, reads like an attribute
# c.area = 100     # AttributeError — no setter defined, so it's genuinely read-only
```

**Medium — a property with validation in its setter:**

```python
class Person:
    def __init__(self, age):
        self.age = age  # goes through the setter immediately, even in __init__

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("Age cannot be negative")
        self.__age = value

p = Person(30)
p.age = 31
try:
    p.age = -5
except ValueError as e:
    print(f"Rejected: {e}")
```

Notice that even the constructor's `self.age = age` goes through the property setter, since `self.age = ...` always triggers the setter once a property is defined. This means validation applies consistently, whether the value came in through `__init__` or through a later assignment.

**Hard — a private attribute, name mangling in action, and why protected is often the more practical choice for subclassing:**

```python
class Base:
    def __init__(self):
        self.__secret = "base secret"      # name-mangled to _Base__secret
        self._shared = "protected value"    # accessible to subclasses by convention

class Child(Base):
    def reveal(self):
        # print(self.__secret)  # would raise AttributeError — mangled to _Child__secret, not _Base__secret
        print(self._shared)     # works fine — protected is accessible by convention

c = Child()
c.reveal()
```

This is a genuinely important, often-missed detail: double-underscore privacy doesn't just block outside code, it also blocks subclasses from directly accessing the parent's private attribute under that name, because mangling is based on whichever class the code is defined in. This is exactly why single-underscore protected is the more commonly used convention for anything a subclass might legitimately need to touch, private is reserved for attributes that genuinely should never be touched outside the defining class, subclasses included.

## 12. Common mistakes

**Writing Java-style `get_x()`/`set_x()` methods in Python** instead of using `@property`. It works, but it's not idiomatic, and it makes simple attribute access look like a method call for no real benefit, when Python gives you a cleaner tool for exactly this.

**Assuming double-underscore privacy is real security.** It isn't. Name mangling is a convenience to avoid accidental name collisions, primarily in inheritance hierarchies, not a genuine access control mechanism; the mangled name is still fully discoverable and reachable if someone wants to reach it. Treat it as "makes accidental misuse harder," not "makes misuse impossible."

**Overusing private (`__`) when protected (`_`) would serve better,** especially for attributes a subclass will legitimately need. As shown above, private attributes actively get in the way of straightforward subclassing.

**Adding a property setter that doesn't validate anything,** which provides no actual benefit over a plain public attribute while adding unnecessary code. A property is worth its complexity when it's actually enforcing a rule or computing something; if it's just a pass-through, a public attribute is simpler and equally correct.

## 13. Debugging tips

If you get an unexpected `AttributeError` trying to access `self.__something` from a subclass, that's very likely name mangling, the attribute exists under a different mangled name tied to the class where it was originally defined, not the subclass. If a property setter's validation doesn't seem to be running, check whether the assignment is actually going through the property (`self.balance = x`) rather than accidentally bypassing it by touching the underlying private attribute directly (`self.__balance = x` from within the same class, which does skip the setter, since it's a direct attribute assignment, not a property call).

## 14. Best practices

Default to public attributes for genuinely simple data with no rules to enforce; not everything needs a property. Reach for `@property` when you need validation, computed values, or the ability to change the internal implementation later without breaking the external interface. Use single-underscore protected as your default "internal, not part of the public interface" marker, reserving double-underscore private specifically for cases where you want to actively prevent subclasses from colliding with or overriding an attribute by name.

## 15. Performance considerations

Property access has a small overhead compared to a raw attribute read, since it's actually a method call under the hood, dressed up to look like attribute access. This overhead is negligible for the vast majority of code and is never a reason to avoid a property where one is genuinely warranted; correctness and maintainability should drive this decision, not micro-optimization.

## 16. Code style

Name the property the same as the underlying private attribute, minus the underscore prefix (`__balance` backing a `balance` property), which is the convention shown throughout this lesson and the one most Python developers expect. Keep property getters simple and fast, ideally free of side effects, since callers reasonably expect attribute-like access to be cheap and safe to repeat.

## 17. Interview questions with model answers

**Q: How does Python implement private attributes, and how "private" are they really?**

Double-underscore attributes trigger name mangling, Python rewrites `self.__x` internally to `self._ClassName__x`. This makes accidental external access unlikely, but it's not a hard security boundary; the mangled name is still fully accessible if someone specifically looks for it. A strong answer explicitly contrasts this with a language like Java, where private is enforced at compile time, and frames Python's approach as convention-plus-a-small-mechanic, rather than a true access control system.

**Q: Why use `@property` instead of traditional `get_x()`/`set_x()` methods?**

`@property` lets attribute access stay clean at the call site, `obj.value` instead of `obj.get_value()`, while still giving the class full control to validate, compute, or restrict that access underneath. It also means a class can start with a plain public attribute and later add validation via a property without breaking any code that was already using `obj.value` directly, since the syntax at the call site never has to change.

**Q: Why might you choose protected (`_x`) over private (`__x`) for an attribute a subclass needs to use?**

Because private attributes get name-mangled per defining class, a subclass can't directly access a parent's private attribute under the same simple name it would expect, which actively interferes with legitimate subclassing. Protected signals "internal, respect this boundary" without that mechanical obstruction, making it the more practical choice whenever a subclass is expected to interact with the attribute.

## 18. Knowledge check

1. What's the practical difference between single-underscore and double-underscore prefixed attributes in Python?
2. Does Python enforce private attribute access the way Java does?
3. Why does `self.age = age` inside `__init__` trigger a property's setter, if `age` is defined as a property?
4. Why can double-underscore privacy actively get in the way of subclassing?

## 19. Hands-on exercises

**Easy**

1. Write a `Temperature` class with a private `__celsius` attribute and a `celsius` property with both a getter and a setter that rejects values below -273.15.
2. Write a class with a protected `_notes` attribute and a subclass that accesses it directly, demonstrating that protected access works across the inheritance boundary.
3. Add a read-only property `full_name` to a `Person` class that combines separate `first_name` and `last_name` attributes, with no setter defined.

**Medium**

4. Write a `Product` class where `price` is a property that rejects negative values in its setter, and demonstrate both a successful update and a rejected one.
5. Demonstrate name mangling directly: create a class with a `__secret` private attribute, then access it from outside the class using its mangled name, and explain in a comment why that access works despite the double underscore.
6. Write an `Inventory` class where `quantity` is a property whose setter prevents the value from ever going negative, and add a `deleter` that resets it to zero instead of actually deleting the underlying attribute.

**Hard**

7. Build a `Password` class where the raw password is stored privately and is never directly readable from outside (no getter for the raw value at all), but exposes a method `matches(attempt)` that checks a provided string against the stored value without ever exposing what's actually stored.
8. Design a small class hierarchy where a base class has a protected `_config` dictionary that subclasses are expected to read and extend, and demonstrate at least one subclass successfully doing so, while also demonstrating that a fully private version of the same attribute would have blocked that subclass from accessing it under the expected name.

## 20. Stretch challenge

Take the `BankAccount` class you've built across earlier lessons in this module and redesign it properly using everything from this lesson: a private `__balance`, a read-only `balance` property (no public setter at all, since balance should only ever change through `deposit`/`withdraw`, never direct assignment), and a protected `_transaction_log` list that a hypothetical subclass could extend but outside code shouldn't touch directly. Write test code proving that `account.balance = 1000000` is now rejected outright (no setter exists), while `account.deposit(500)` still works exactly as expected. This is the shape the Banking System capstone project will expect by the time you reach it.

## 21. Summary

Encapsulation controls how an object's internal state can be accessed and changed from outside, which is what lets a class actually enforce its own rules instead of trusting every caller to behave. Python implements this mostly through convention, a single underscore for protected, a double underscore for private with real name mangling behind it, rather than hard compiler-level enforcement. `@property` is the idiomatic way to add validation or computed behavior to attribute access without sacrificing the clean, attribute-like syntax at the call site, and it's a tool you'll reach for constantly from this point forward.

## 22. Additional resources

- [Python official docs: Private Variables](https://docs.python.org/3/tutorial/classes.html#private-variables)
- [Python official docs: property()](https://docs.python.org/3/library/functions.html#property)
- [Real Python: Python's property(): Add Managed Attributes to Your Classes](https://realpython.com/python-property/)

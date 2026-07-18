# Module 2 Assessment — Answer Key

Don't open this until you've genuinely attempted the exam first.

---

## Section A: Multiple choice

1. A — `class`
2. B — the specific instance the method was called on
3. C — `Car()`
4. B — initializing a new object's state
5. A — shared across every instance unless shadowed
6. C — creates a new instance attribute, shadowing the class one
7. B — `@staticmethod`
8. B — the class itself
9. B — a subclass redefining a method the parent also defines
10. B — Python rewrites `__x` to `_ClassName__x`, making accidental external access harder
11. A — `@property` with no corresponding setter defined
12. B — a proxy that lets you access the parent class's methods
13. B — the parent (super) class
14. B — the order Python searches classes when resolving an attribute or method
15. B — an object's suitability being judged by whether it has the right methods
16. B — `@classmethod`
17. C — `__add__`
18. B — enforcement that abstract methods must be implemented before instantiation
19. B — `TypeError` is raised
20. B — composition
21. B — ownership and lifecycle of the contained object
22. B — `class C(A, B):`
23. C — Python's MRO, computed via C3 linearization
24. C — a class should have only one reason to change
25. B — open for extension, closed for modification
26. B — a class focused on one clear responsibility
27. B — changing one frequently forces changes in the other
28. B — `@abstractmethod` inside a class inheriting from `ABC`
29. B — combined with other classes via multiple inheritance, adding reusable behavior
30. B — always False, defaults to identity comparison without `__eq__`
31. B — `@attributename.setter` where `attributename` matches the getter's name
32. B — letting a class enforce its own rules by controlling access to its internal state
33. B — `SavingsAccount` is-a `Account`
34. B — a tuple showing the method resolution order
35. C — Favor composition over inheritance
36. B — it inherits and uses the parent's version unchanged
37. B — calling the same method name on different object types and getting type-appropriate behavior
38. B — indicating private (`-`) and public (`+`) visibility
39. B — `items = []` as a class attribute, then `.append()` through an instance
40. B — `@abstractmethod` alone has no enforcement effect without `ABC` or `ABCMeta`
41. B — Left, because it's listed first, per MRO
42. B — `self._x`
43. B — it becomes hard to trace where behavior actually comes from
44. C — `super().__init__(...)`
45. B — abstract base classes can't be instantiated directly if they have unimplemented abstract methods
46. B — it signals that polymorphism should be doing that work instead
47. B — composition
48. B — a long `if/elif` chain that needs a new branch every time a new case is added
49. A — creates a new instance of whichever class actually called the method
50. B — inheritance is the structure; polymorphism is the behavioral payoff

---

## Section B: True or false

1. False — Python fills in `self` automatically via the dot-call syntax; the caller never passes it explicitly.
2. True.
3. False — Python uses name mangling, which makes accidental access harder but doesn't enforce a hard wall; the mangled name is still reachable.
4. True — `super()` follows the MRO, which may not be the literal named parent if multiple inheritance is involved.
5. True — an abstract method can have a body that a subclass calls explicitly via `super().method()`.
6. True — in true composition, the contained object is created by and typically doesn't outlive its container.
7. True — in aggregation, the contained object exists independently and can outlive or be shared across containers.
8. False — Python does not support true method overloading; a second definition of the same name simply replaces the first.
9. False — duck typing explicitly does not require a shared base class; suitability is judged by the presence of the right methods.
10. False — OCP says you should extend behavior by adding new code, not by modifying existing tested classes.
11. True — Python supports multiple inheritance via `class C(A, B):`.
12. True — Python's C3 linearization produces a single, deterministic MRO.
13. False — `@staticmethod` methods receive neither `self` nor `cls`; they have no implicit access to instance state.
14. True.
15. False — tight coupling makes a codebase harder and riskier to change, not easier.
16. True — defining `__eq__` makes the default `__hash__` inconsistent; they should be kept in sync.
17. True — abstract base classes can freely mix concrete and abstract methods.
18. False — favoring composition is a general default, not an absolute rule; there are genuine, defensible uses of inheritance.
19. True — a filled diamond in UML represents composition.
20. True — both are called using `instance.method()` syntax from the outside.

---

## Section C: Identification

1. `__init__`
2. `@classmethod`
3. `@staticmethod`
4. Name mangling
5. `super()`
6. Method Resolution Order (MRO)
7. `abc`
8. Duck typing
9. `__str__`
10. `__eq__`
11. Inheritance
12. Composition
13. Aggregation
14. Single Responsibility Principle (SRP)
15. Open/Closed Principle (OCP)
16. Coupling
17. Cohesion
18. The diamond problem
19. Mixin
20. `@property`

---

## Section D: Short answer, key points to hit

1. Instance methods receive `self` (the specific object) and operate on per-instance data. Class methods receive `cls` (the class itself) and operate on class-level data or serve as alternate constructors. Static methods receive neither, they're ordinary functions grouped inside the class for organizational reasons, with no automatic access to instance or class state.

2. Assigning through `self.attribute = value` always creates or overwrites an attribute on the instance's own `__dict__`. Python's attribute-setting protocol (`__setattr__`) goes directly to the instance, never up to the class; only `ClassName.attribute = value`, referencing the class explicitly, actually modifies the class-level attribute. This is why instance assignment always shadows the class attribute rather than changing it.

3. Python rewrites `self.__x` inside a class's definition to `self._ClassName__x`, making the attribute name class-specific. This prevents accidental name collisions in deep inheritance hierarchies (where a subclass and parent might otherwise both try to use the same private name), and makes unintentional external access harder (though not impossible). It exists as a convenience to protect private state from accidental interference, not as a security mechanism.

4. Composition implies ownership and a shared lifecycle: the contained object is typically created by its container and has no independent purpose beyond it. Aggregation implies "has-a" without that ownership: the contained object exists independently, can predate its container, and can outlive or be reassigned to a different container. This matters in real design because it affects how objects are created, destroyed, and potentially shared: a `Transaction` record (composition) should never be reassigned to a different account, while an `Employee` in a `Department` (aggregation) absolutely can be.

5. The diamond problem occurs when a class inherits from two classes that both inherit from a common ancestor, creating ambiguity about which version of an overridden method should apply. Python computes a single, deterministic Method Resolution Order using C3 linearization, which produces an ordered tuple of classes that Python checks in sequence; the first class in the MRO that has the method wins. The order depends on how the class lists its parents, `class D(Left, Right)` puts Left first in the MRO, so Left's version wins over Right's.

6. Because the incompleteness only becomes a real problem when code actually tries to create and use an instance of the incomplete class. A class definition can exist in an abstract, incomplete state as an intermediate step in a hierarchy, and that's valid and intentional. Checking at instantiation time catches the mistake exactly where it would cause real harm, immediately during development, rather than silently creating an unusable object that only fails the first time a specific code path exercises the missing method, potentially in production.

7. Encapsulation controls access to an object's internal state, protecting data behind properties and methods that enforce rules. Abstraction defines what something must be able to do (a required interface) without specifying how. A class can be well-encapsulated (data fully protected, only changed through controlled methods) without being abstract (it's a fully concrete implementation). An abstract base class defines a required interface without any (or much) actual implementation. They're complementary tools solving different design problems.

8. Duck typing means an object's suitability for an operation is determined by whether it has the right attributes and methods, not its declared class or inheritance hierarchy, "if it walks like a duck and quacks like a duck." It's central to Python because Python is dynamically typed and has no compiler enforcing formal interfaces, so the check happens at runtime when the method is actually called, not ahead of time. This lets code work uniformly with completely unrelated types as long as they support the needed interface, without any formal inheritance relationship being required.

9. A long `isinstance()`/`elif` chain is a sign that the type-checking logic doesn't belong in the calling code at all: it belongs inside each type itself, as a correctly implemented shared method. Every time a new type is added, every one of those scattered chains has to be found and updated, which is exactly the kind of fragility the Open/Closed Principle and polymorphism both exist to prevent. A chain that grows every time a new subtype is introduced is practically the definition of a design that's closed to extension and forced open for modification.

10. SRP: a class should have only one reason to change. Example: a class that both calculates order totals and sends email confirmations violates SRP because changes to email formatting should never risk destabilizing pricing logic. Splitting them into `OrderPricer` and `OrderNotifier` means each class changes for only one reason, and a change in one has zero risk of breaking the other.

11. OCP: open for extension, closed for modification. Example: an `apply_discount` function with `if/elif` for each discount type must be edited every time a new type is added, touching already-tested code. Replacing it with an abstract `Discount` interface and concrete subclasses means a new discount type is a new file only; the applying logic never changes.

12. Composition is a general default because it produces more loosely coupled, more testable, more easily changed code in the majority of real-world "has-a" design situations. Inheritance remains the right call when the relationship is genuinely and stably "is-a": `SavingsAccount extends Account` is a legitimate use because a savings account really is a kind of account, sharing real structural identity (a balance, deposit logic), not just incidentally borrowing some methods. The deciding question is always: is this a stable specialization of something, or just code reuse dressed up as a relationship?

13. Without high cohesion and low coupling, a small change to one requirement touches five or six classes that were all tangled together, each change carries a real risk of breaking unrelated behavior that happened to live in the same class, testing becomes practically impossible without standing up the entire system at once, and the codebase becomes progressively more expensive and slower to change safely, which is the dominant cost of enterprise software over its lifetime.

14. Python's default `__hash__` is based on object identity. Defining `__eq__` without also defining `__hash__` makes objects that are "equal" by your definition hash differently, which breaks set membership and dictionary key lookups in subtle, hard-to-debug ways: two "equal" objects might both be stored in a set as separate items, or a dictionary lookup might fail to find a key it "should" match. Keeping them consistent ensures objects behave correctly anywhere Python uses both equality and hashing together.

15. A mixin is a class designed specifically to be combined with other classes through multiple inheritance, adding one focused, reusable piece of behavior (like logging, or serialization) to any class that needs it, without representing a standalone concept on its own. Unlike a normal parent class, a mixin isn't meant to be instantiated directly, and it isn't modeling a genuine "is-a" relationship; it's more like a capability you bolt onto a class selectively. A `Loggable` mixin adds logging behavior; it doesn't make `Order` "a kind of Loggable" in any meaningful sense.

---

## Section E: Code tracing

1. `11` — `B.__init__` calls `super().__init__()`, which sets `self.x = 1`, then adds 10.
2. `1 2 3 3` — each `Counter()` increments the shared `Counter.total`, and each instance gets its own `id` from that counter at construction time.
3. `[0, 12.57]` — `Shape.area()` returns `0`; `Circle.area()` computes `3.14159 * 4`, rounded to 2 places.
4. `"CA"` — `C.greet()` calls `super().greet()`, which resolves to `B`, which has no `greet()`, so it goes to `A`, returning `"A"`, and `C` prepends `"C"`.
5. `50` — `add()` modifies `self.__balance`; the property getter returns it. No setter exists, so `w.balance` is read-only; `w.add(50)` is the only path to change it.
6. `"Left"` then `<class 'Left'>` — MRO is `D, Left, Right, Base, object`; `Left` wins. `D.__mro__[2]` is `Right` (index 0 is `D`, 1 is `Left`, 2 is `Right`). Wait: index 2 is `Right`. Print confirms `<class '__main__.Right'>`.
7. `"Woof" "..." "..."` — `a.sound = "Woof"` creates an instance attribute on `a`, shadowing the class attribute. `b` and `Animal` are unaffected.
8. `[10, 20, 30]` — `__lt__` allows `sorted()` to compare by price; result is ascending order.
9. `"A config object" "loaded json"` — `JSONConfig` correctly implements `load()`, so it instantiates fine. `describe()` is a concrete method inherited from `Config` (which must be imported from `abc` for this to work). Output: `A config object loaded json`.
10. `1` then `2` — `root.children` has one element (the `child` node); `root.children[0].value` is `2`.

---

## Section F: Debugging tasks

1. `__init__` is missing `self` as its first parameter. Fix: `def __init__(self, name):`.
2. Not a crash, but a design bug: `balance` is a class attribute. `a.deposit(100)` does `self.balance += amount`, which creates an instance attribute on `a` specifically (shadowing the class one at `0`), so `b.balance` still reads the class attribute, `0`. This is the mutable class attribute bug from Lesson 4. Fix: initialize `self.balance = 0` inside `__init__`.
3. `Square` doesn't implement `area()`, so `Square(4)` raises `TypeError`. Fix: add `def area(self): return self.side ** 2` to `Square`.
4. `Dog.__init__` doesn't call `super().__init__(name)`, so `self.name` never gets set. Fix: add `super().__init__(name)` as the first line of `Dog.__init__`.
5. `__add__` returns a plain `int` (`self.amount + other.amount`), not a `Money` object, so `m.amount` raises `AttributeError`. Fix: `return Money(self.amount + other.amount)`.
6. `Point3D.show` tries to access `self.__x`, which is name-mangled to `self._Point__x` (because `__x` was defined in `Point`), not `self._Point3D__x`. Fix: use `self._Point__x` explicitly, or expose it via a property on `Point` instead of using double-underscore privacy.
7. `__init__` runs `self.salary = salary`, which triggers the property setter, but the property setter doesn't exist yet (only the getter is defined). Fix: add a `@salary.setter` method, or define the private `__salary` directly inside `__init__` via `self.__salary = salary` before the property is defined.
8. `get()` calls `self.data[key]` directly, which raises `KeyError` if the key isn't present. Fix: use `return self.data.get(key)` or wrap in a `try/except KeyError`.
9. `"Base"` is NOT printed. `Child.__init__` overrides and prints `"Child"`, then calls `super().__init__()` which prints `"Base"`. Both print. The bug is the expectation only one prints; both run. Correct output: `Child` then `Base`.
10. This violates the Open/Closed Principle. Every time a new discount kind is needed, this method has to be edited, touching already-tested code. Fix: define an abstract `Discount` base with a concrete `apply(price)` method on each subclass, and reduce this method to simply `return discount.apply(price)`.

---

## Section G: Class design exercises, guidance notes

**1. University course registration**

`Student` and `Course` are clearly separate entities. `Enrollment` deserves to be its own class because it represents the relationship between a specific student and a specific course, and it may need to carry its own data (enrollment date, grade, completion status) that belongs to neither `Student` nor `Course` individually. `Student` to `Enrollment` is aggregation (a student exists independently of any enrollment), `Course` to `Enrollment` similarly. This is the classic "join entity" pattern.

**2. Food delivery app**

`Restaurant` aggregates `MenuItem` objects (menu items exist independently and could belong to multiple restaurants in a real system). `Order` composes `LineItem` objects (a line item is created specifically for an order and has no meaning outside it). `Order` aggregates `Driver` (a driver exists independently of any one order). `Restaurant` aggregates `Order` loosely (orders outlive individual delivery sessions). The key design test: which objects would still exist if the containing object was deleted?

**3. Notification system**

Abstract `NotificationChannel` base (or interface) with `send(recipient, message)` as an abstract method, concrete `EmailChannel`, `SMSChannel`, `PushChannel` subclasses. A `NotificationService` composes a list of channels (or a single one, injected at construction time). The OCP angle: a new channel is a new class only, and `NotificationService` never changes. Abstraction (Lesson 9) and polymorphism (Lesson 8) working together is the entire design here.

**4. Media library hierarchy**

A `MediaItem` abstract base with abstract `play()` and concrete `duration` property makes sense. `Movie`, `TVShow`, and `MusicAlbum` all inherit from it. What doesn't belong in the base: episode count (TV only), director (film-specific in many designs), artist (music only). A strong answer identifies which attributes are genuinely universal across all media types and which should stay on the subclass, and doesn't force things that aren't shared into the base just for tidiness.

**5. Vehicle and Engine requirement**

Adding `ElectricEngine` and `GasEngine` via further inheritance would require combinations like `ElectricCar`, `GasCar`, `ElectricMotorcycle`, `GasMotorcycle`, `ElectricBoat`, `GasBoat`, and then `HybridCar` needing two parents, a combinatorial explosion with no clean solution in a pure inheritance hierarchy. The right answer is composition: `Vehicle` has an `engine` attribute (or a list for hybrids), accepting any `Engine` object (abstract base or duck-typed). New engine types require one new class; no existing vehicle class changes. This is exactly the fragility inheritance introduces when variation is better modeled as a component.

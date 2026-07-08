# Lesson 1: Introduction to Object-Oriented Programming

## 1. Learning objectives

By the end of this lesson you should be able to:

- Explain the difference between procedural and object-oriented programming in your own words, not just by definition
- Articulate the actual problems OOP was designed to solve, not just list its four pillars from memory
- Recognize real situations where OOP genuinely helps, and just as importantly, where it's overkill
- Speak to the tradeoffs of OOP in a way that shows judgment rather than blind allegiance to the paradigm

## 2. Prerequisites

All of Module 1. This lesson doesn't introduce new syntax yet, it introduces a new way of organizing the syntax you already know.

## 3. Introduction

Every program you wrote in Module 1 was procedural: a sequence of steps, organized into functions, operating on data that got passed around between them. That approach works fine for scripts. It starts to strain the moment your program needs to model something with both data and behavior that belong together, a bank account that has a balance and knows how to validate a withdrawal, a client record that has fields and knows how to check its own completeness. Object-oriented programming is a response to that specific strain, not a replacement for everything you already know.

## 4. Theory

Procedural programming organizes a program around functions that act on data. The data and the functions that operate on it are separate; a function like `calculate_interest(balance, rate)` takes data in, does something, and hands a result back, with no lasting relationship between the function and the data it touched.

Object-oriented programming organizes a program around objects: bundles that combine data (called attributes) and the behavior that operates on that data (called methods) into a single unit. Instead of a free-floating function `withdraw(account, amount)`, you have `account.withdraw(amount)`, where the account itself is responsible for validating and executing its own withdrawal.

```python
# Procedural style
def withdraw(balance, amount):
    if amount > balance:
        raise ValueError("Insufficient funds")
    return balance - amount

balance = 100
balance = withdraw(balance, 30)

# Object-oriented style
class Account:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount

account = Account(100)
account.withdraw(30)
```

Neither version is "more correct." The procedural version is perfectly fine for a one-off script. The object-oriented version starts paying off the moment you have many accounts, each needing to track its own state independently, and many operations that only make sense in the context of a specific account's data.

## 5. Why this concept exists

As programs grow, procedural code tends to accumulate two problems. First, data gets passed through long chains of functions, and it becomes unclear which functions are allowed to modify it, or what state it's supposed to be in at any given point. Second, related data and behavior end up scattered: a "customer" might be represented as a dictionary in one function, a tuple in another, and validated by a function that lives in a completely different file, with nothing tying them together except convention. OOP exists to fix both problems at once, by giving data and its associated behavior a single home, and by giving that home a name that represents a real concept in the problem you're solving.

## 6. Internal behavior

At the interpreter level, a Python class is itself an object, an instance of a built-in type called `type`. When you write `class Account:`, Python builds a class object and stores its methods and class-level attributes inside it. When you call `Account(100)`, Python creates a new, separate object in memory, links it back to the `Account` class (so it knows where to find its methods), and runs `__init__` to set up that specific instance's own data. Every instance shares the same methods (they live once, on the class) but has its own independent attributes (which live on the instance). This split, shared behavior on the class, independent state on the instance, is the foundation everything else in this module builds on.

## 7. Real-world analogy

A blueprint for a house isn't a house. It's a specification: this many bedrooms, this floor plan, these electrical outlets in these locations. A class is the blueprint. Building an actual house from that blueprint, one with its own address, its own current temperature, its own specific residents, is creating an object. You can build a hundred houses from one blueprint, and painting one of them blue doesn't repaint the others, because each house has its own independent state, even though they all share the same underlying design.

## 8. Enterprise use cases

Nearly every non-trivial backend system models real business concepts as classes: a `Customer`, an `Order`, an `Invoice`, a `PaymentMethod`. This isn't decoration, it's what makes a codebase navigable to a new engineer. If a business analyst describes a workflow in terms of orders, invoices, and payments, and the code has classes named `Order`, `Invoice`, and `Payment` with methods that mirror the business logic, then the distance between "how the business thinks about this" and "how the code is structured" shrinks dramatically, and that distance is exactly what makes systems expensive to maintain when it's large.

## 9. UML-style explanation

A simple UML class box for the `Account` example above looks like this:

```
┌─────────────────────────┐
│         Account          │
├─────────────────────────┤
│ - balance: float          │
├─────────────────────────┤
│ + withdraw(amount): None  │
│ + deposit(amount): None   │
└─────────────────────────┘
```

Three sections, top to bottom: the class name, its attributes (data), and its methods (behavior). The `-` prefix conventionally marks something private, `+` marks something public, a convention this module will use consistently from the Encapsulation lesson onward. You'll see boxes like this throughout the rest of Module 2, and building the habit of sketching one before writing code is worth adopting now.

## 10. Syntax

This lesson is conceptual, so there's minimal new syntax, but here's the shape you'll be using for the rest of the module, shown without the deep explanation that Lesson 2 will provide:

```python
class ClassName:
    def __init__(self, param):
        self.attribute = param

    def method_name(self):
        return self.attribute
```

## 11. Step-by-step examples

**Comparing the same small problem, both styles, side by side:**

Procedural:

```python
def create_student(name, grade):
    return {"name": name, "grade": grade}

def is_passing(student):
    return student["grade"] >= 60

alex = create_student("Alex", 75)
print(is_passing(alex))
```

Object-oriented:

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def is_passing(self):
        return self.grade >= 60

alex = Student("Alex", 75)
print(alex.is_passing())
```

Both print the same result. The second version keeps `is_passing` permanently attached to the data it operates on; there's no way to accidentally call it with the wrong kind of dictionary, because it only ever operates on `self`.

## 12. Common mistakes

**Reaching for a class when a function would do.** Not every piece of logic needs to become an object. A stateless calculation, `def calculate_tax(amount, rate)`, doesn't benefit from being wrapped in a class with one method; that's added ceremony with no payoff. OOP earns its keep when there's meaningful state to manage and behavior that naturally belongs with that state.

**Treating OOP as strictly "better" than procedural code.** Both are tools. A one-off data-cleaning script is often clearer written procedurally. This module will spend a lot of time teaching OOP well, which can create the impression it's always the right call; it isn't.

**Modeling classes after database tables instead of behavior.** A class with a dozen attributes and no meaningful methods is really just a data container wearing a class's clothing. That's not automatically wrong (dataclasses exist for exactly this), but if you're reaching for a full class, make sure it's actually doing something, not just holding fields.

## 13. Debugging tips

If you're not sure whether something should be a class, ask what state it needs to track between calls, and what behavior operates specifically on that state. If the answer to either is "none," a function is probably the right tool, and forcing it into a class will make the code harder to read, not easier.

## 14. Best practices

Model classes around real nouns in the problem domain, not around technical implementation details. Give a class a single, clear responsibility; if you can't describe what a class does in one sentence without using "and," it's likely trying to do too much. Don't convert existing working procedural code to OOP just because this module exists, convert it when there's a genuine state-and-behavior pairing that would benefit.

## 15. Performance considerations

Object creation in Python has a small overhead compared to using plain dictionaries or tuples, since each instance carries its own `__dict__` for attributes by default. For the vast majority of backend code, this overhead is irrelevant next to the maintainability gains. It only becomes a real consideration in extremely high-throughput, performance-critical code, at which point `__slots__` (a later, more advanced topic) can reduce that overhead, but that's not a concern for this module.

## 16. Code style

Class names use `PascalCase` (`Account`, `StudentRecord`), while everything else, methods, attributes, variables, stays in `snake_case`. This distinction is enforced by convention (PEP 8), not by the interpreter, but breaking it will make your code look unfamiliar to any Python developer reading it.

## 17. Interview questions with model answers

**Q: What problem does object-oriented programming actually solve?**

A strong answer goes beyond reciting "encapsulation, inheritance, polymorphism, abstraction" and instead explains that OOP keeps related data and behavior bundled together in one place, instead of scattered across functions that all have to agree on the shape of some external data. That bundling reduces the surface area for bugs, since fewer things can quietly mutate an object's state in unexpected ways, and it maps more directly onto how people naturally describe real-world business processes.

**Q: When would you choose not to use OOP?**

For small, stateless scripts, data transformation pipelines, or simple utility functions where there's no meaningful ongoing state to manage. Forcing a class structure onto something that's fundamentally "take input, produce output, done" adds ceremony without benefit. The interviewer is checking whether you treat OOP as a default reflex or as a deliberate choice.

**Q: Give a real-world example of when OOP makes a codebase easier to maintain.**

A good answer picks something concrete: a system that manages many independent accounts, orders, or users, each with its own internal state and rules. Because each object owns its own data and the logic that operates on it, a change to how withdrawals are validated lives in exactly one place, the `Account` class, rather than being duplicated across every function that happens to touch a balance.

## 18. Knowledge check

1. What's the core difference between procedural and object-oriented programming?
2. Name one situation where a plain function is a better choice than a class.
3. What two things does an object bundle together that a procedural function keeps separate?
4. Why might modeling every dictionary in a program as a class be a mistake?

## 19. Hands-on exercises

**Easy**

1. Write a short paragraph, in your own words, describing the difference between a class and an object, using an analogy that isn't the blueprint/house one from this lesson.
2. Take a procedural function `def describe_book(title, author, pages)` that returns a formatted string, and identify what a `Book` class version of it would need to hold as attributes.
3. List three real-world nouns from a hypothetical online store (not code, just the concepts) that would make reasonable classes.

**Medium**

4. Take the procedural `Student` example from this lesson, add a second function `average_grade(students)` that operates on a list of student dictionaries, and then rewrite the whole thing in an object-oriented style, deciding where `average_grade` should live (on the class, or as a separate function operating on a list of `Student` objects).
5. Sketch a UML-style class box, by hand or in a text file, for a `Book` class with a title, author, and a method to check if the book is overdue.

**Hard**

6. Identify a piece of procedural code you wrote in Module 1's capstone project, and write a short analysis (a few sentences) of whether converting it to an object-oriented design would actually help, and why or why not. Not every answer should be "yes."

## 20. Stretch challenge

Take the Module 1 capstone CLI application (or any procedural script you've written) and pick one specific piece of it, not the whole thing, where you think an object-oriented redesign would genuinely improve it. Write out, in comments or plain English, what class or classes you'd introduce, what attributes and methods they'd have, and specifically what problem that redesign solves that the procedural version didn't handle well. Resist the urge to convert the entire script; the point of this exercise is learning to spot where OOP earns its keep, not applying it everywhere reflexively.

## 21. Summary

Object-oriented programming bundles data and the behavior that operates on it into a single unit, an object, built from a class that acts as its blueprint. It exists to solve a specific problem procedural code runs into at scale: data and the logic that's supposed to manage it drifting apart across a growing codebase. It's a tool with real tradeoffs, not a universal upgrade, and the judgment of when to reach for it is at least as important as knowing the syntax, which the rest of this module will cover in depth.

## 22. Additional resources

- [Python official docs: A First Look at Classes](https://docs.python.org/3/tutorial/classes.html)
- [PEP 8 — Style Guide, class naming conventions](https://peps.python.org/pep-0008/#class-names)
- [Real Python: Object-Oriented Programming in Python 3](https://realpython.com/python3-object-oriented-programming/)

# Module 1 Assessment

This is the exam. Everything before this file was practice; this is where you find out what actually stuck. Work through it without your notes open the first time, then go back and check yourself against the answer key at the end of each section. Being honest with yourself here is worth more than a good score you didn't actually earn.

---

## Section A: Multiple choice (50 questions)

1. What does `type(5.0)` return?
A) int B) float C) str D) complex

2. Which of these is immutable?
A) list B) dict C) tuple D) set

3. What is the output of `print(2 ** 3)`?
A) 6 B) 8 C) 9 D) 5

4. Which keyword creates a function in Python?
A) function B) def C) func D) define

5. What does `len("hello")` return?
A) 4 B) 5 C) 6 D) Error

6. What is the result of `10 // 3`?
A) 3.33 B) 3 C) 4 D) 1

7. Which of these correctly checks if a variable `x` is None?
A) `x = None` B) `x == None` C) `x is None` D) `x.isNone()`

8. What does the `range(5)` function generate?
A) 1 to 5 B) 0 to 5 C) 0 to 4 D) 1 to 4

9. Which data type would you use to store a fixed collection of coordinates that should never change?
A) list B) tuple C) set D) dict

10. What is the output of `"abc" + "def"`?
A) abcdef B) abc def C) Error D) None

11. What does `**kwargs` collect inside a function?
A) a list of positional args B) a dictionary of keyword args C) a tuple of all args D) nothing, it's invalid syntax

12. Which of these will raise a `TypeError`?
A) `"5" + "5"` B) `5 + 5` C) `"5" + 5` D) `5.0 + 5`

13. What does `break` do inside a loop?
A) skips the current iteration B) exits the loop entirely C) pauses the loop D) restarts the loop

14. What's the correct way to open a file safely in Python?
A) `f = open("file.txt")` B) `with open("file.txt") as f:` C) `file.read("file.txt")` D) `import file.txt`

15. What does `dict.get("key", "default")` do if `"key"` isn't present?
A) raises KeyError B) returns None always C) returns "default" D) creates the key with value None

16. What is the scope of a variable defined inside a function, by default?
A) global B) local C) enclosing D) built-in

17. Which exception is raised by dividing by zero?
A) ValueError B) TypeError C) ZeroDivisionError D) ArithmeticError

18. What does `list.append()` do?
A) adds an item to the end B) adds an item to the start C) removes the last item D) sorts the list

19. Which of the following creates an empty set?
A) `{}` B) `set()` C) `[]` D) `()`

20) What is the output of `bool(0)`?
A) True B) False C) 0 D) Error

21. What is the correct file mode to append to an existing file?
A) "r" B) "w" C) "a" D) "x"

22. Which statement about tuples is true?
A) They can be modified after creation B) They can be used as dictionary keys C) They only store numbers D) They are the same as lists

23. What does the `enumerate()` function return?
A) only the index B) only the value C) pairs of index and value D) a sorted list

24. What is the result of `5 == 5.0`?
A) True B) False C) Error D) None

25. What does `import module as m` do?
A) copies the module's code into your file B) creates an alias `m` for the module C) is invalid syntax D) imports only the `m` function

26. Which loop construct is best when the number of iterations isn't known in advance?
A) for B) while C) range D) enumerate

27. What is a docstring?
A) a string that documents a function, placed as the first statement in its body B) a special type of comment using `#` C) a required part of every variable D) a string used only for error messages

28. What does `except Exception as e:` capture in `e`?
A) nothing, it's a syntax error B) the exception object C) only the exception's message as a string D) the line number of the error

29. Which of these correctly defines a function with a default argument?
A) `def f(x=5):` B) `def f(x:=5):` C) `def f(x==5):` D) `def f(default x=5):`

30. What's the time complexity of checking membership (`in`) in a Python set, on average?
A) O(n) B) O(log n) C) O(1) D) O(n²)

31. Which of these is the correct way to raise a custom exception?
A) `raise "Custom error"` B) `throw CustomError()` C) `raise CustomError("message")` D) `error CustomError`

32. What does `json.load(f)` do?
A) writes a Python object to a file as JSON B) parses a JSON file into a Python object C) validates a JSON file D) converts JSON to CSV

33. What is the output of the following?
```python
x = [1, 2, 3]
y = x
y.append(4)
print(x)
```
A) [1, 2, 3] B) [1, 2, 3, 4] C) Error D) None

34. Which keyword is used to handle cleanup code that always runs, regardless of an exception?
A) except B) else C) finally D) cleanup

35. What does `str.strip()` do by default?
A) removes all whitespace inside a string B) removes leading and trailing whitespace C) splits a string into words D) converts a string to lowercase

36. Which of these correctly imports the `sqrt` function from the `math` module?
A) `import math.sqrt` B) `from math import sqrt` C) `import sqrt from math` D) `include math.sqrt`

37. What is the result of `"Hello"[1:4]`?
A) "Hell" B) "ello" C) "ell" D) "Hello"

38. What does `pip freeze` output?
A) a list of Python keywords B) the currently installed packages and their versions C) the current Python version D) a frozen copy of your source code

39. What is the correct way to check multiple conditions where either could be true?
A) `if a and b:` B) `if a or b:` C) `if a & b:` D) `if a, b:`

40. Which built-in function converts a string to an integer?
A) `str()` B) `float()` C) `int()` D) `num()`

41. What happens when you call a function that has no `return` statement?
A) it raises an error B) it returns `None` C) it returns `0` D) it returns an empty string

42. Which of these is the correct match-case wildcard pattern?
A) `case default:` B) `case any:` C) `case _:` D) `case *:`

43. What is the output of `list(range(3, 0, -1))`?
A) [3, 2, 1] B) [1, 2, 3] C) [3, 2, 1, 0] D) []

44. Which module would you use to work with dates and times?
A) time_module B) datetime C) calendar_tools D) pydate

45. What does `a, b = b, a` accomplish?
A) it's invalid syntax B) swaps the values of a and b C) creates a tuple D) deletes both variables

46. What's the correct way to catch both `ValueError` and `TypeError` in one except clause?
A) `except ValueError, TypeError:` B) `except [ValueError, TypeError]:` C) `except (ValueError, TypeError):` D) `except ValueError or TypeError:`

47. What does `__init__.py` do in a folder?
A) nothing, it's optional metadata B) marks the folder as a Python package C) initializes all variables in the folder D) runs automatically every time Python starts

48. What is the result of `"3" == 3`?
A) True B) False C) Error D) None

49. Which statement about lambda functions is correct?
A) they can contain multiple statements B) they can only take one argument C) they're limited to a single expression D) they must be assigned to a variable

50. What is the safest way to provide a default for a function argument that should be an empty list?
A) `def f(x=[]):` B) `def f(x=list()):` C) `def f(x=None): x = x or []` D) `def f(x=[None]):`

---

## Section B: True or false (20 questions)

1. Python variables must be declared with a specific type before use.
2. Lists are immutable in Python.
3. `==` checks for value equality, while `is` checks for identity.
4. A `while` loop always executes at least once.
5. `except:` with no exception type specified catches every possible exception.
6. Dictionaries in Python 3.7+ maintain insertion order.
7. Tuples can be used as dictionary keys.
8. `*args` collects extra keyword arguments into a dictionary.
9. A function without an explicit `return` statement returns `None`.
10. `with open(...)` automatically closes the file even if an exception occurs.
11. Sets allow duplicate values.
12. String concatenation with `+` modifies the original string in place.
13. `range(5)` includes the number 5.
14. A `for` loop's `else` clause runs even if the loop was exited with `break`.
15. `pip` is used to manage Python packages.
16. A virtual environment is required for Python to run at all.
17. `json.dump()` writes a Python object to a file as JSON text.
18. Custom exceptions must inherit from `Exception` or one of its subclasses.
19. In Python, `0.1 + 0.2` is exactly equal to `0.3`.
20. Mutable default arguments are evaluated once, at function definition time.

---

## Section C: Identification (20 questions)

Name the exact Python concept, keyword, or built-in function being described.

1. The function used to determine the type of an object.
2. The keyword that halts execution of a loop entirely.
3. The data structure that stores unique, unordered elements.
4. The keyword used to define a function.
5. The built-in module used to work with file system paths in a cross-platform way.
6. The exception raised when dividing by zero.
7. The clause in a try/except block that runs only if no exception occurred.
8. The parameter-collecting syntax that gathers extra positional arguments into a tuple.
9. The rule governing the order Python searches for a variable name across scopes.
10. The file that marks a directory as an importable Python package.
11. The built-in function used to get user input from the terminal.
12. The string formatting method introduced in Python 3.6 using an `f` prefix.
13. The command used to install a Python package from the terminal.
14. The keyword used to raise an exception deliberately.
15. The method used to add a single item to the end of a list.
16. The data type representing the absence of a value.
17. The built-in function that returns the number of items in a collection.
18. The loop construct best suited for iterating over a known collection.
19. The keyword used to import only a specific function or class from a module, rather than the whole module.
20. The clause that runs no matter what happens in a try block, success or failure.

---

## Section D: Short answer (15 questions)

1. Explain the difference between a parameter and an argument.
2. Why is `0.1 + 0.2 == 0.3` `False` in Python?
3. Explain why mutable default arguments cause bugs, with a short example.
4. What's the practical difference between a list and a tuple, beyond just "one can change and one can't"?
5. Why does Python prefer `with open(...)` over manual `open()`/`close()`?
6. Explain the LEGB rule in your own words.
7. What's the difference between `except Exception:` and a bare `except:`?
8. Why would you create a custom exception class instead of always raising a built-in one like `ValueError`?
9. Explain why checking membership in a set is faster than checking membership in a list.
10. What's the difference between `import module` and `from module import thing`?
11. Explain what a virtual environment is and why it matters on a team project.
12. Why does `for x in my_list: my_list.remove(x)` behave unpredictably?
13. Explain the difference between `json.load()` and `json.loads()`.
14. What does it mean for a function to be "pure," and why does that matter for testing?
15. Explain, with an example, what happens differently between `a = b = []` and `a = []; b = []`.

---

## Section E: Code tracing (10 questions)

Trace through each one by hand and write down the exact final output.

1.
```python
x = 5
y = x
x = x + 1
print(x, y)
```

2.
```python
total = 0
for i in range(1, 5):
    total += i
print(total)
```

3.
```python
def f(a, b=10):
    return a + b
print(f(5), f(5, 20))
```

4.
```python
data = [1, 2, 3]
data2 = data[:]
data2.append(4)
print(data, data2)
```

5.
```python
result = []
for i in range(3):
    for j in range(3):
        if i == j:
            result.append((i, j))
print(result)
```

6.
```python
d = {"a": 1}
d["b"] = d.get("b", 0) + 1
print(d)
```

7.
```python
def counter():
    n = 0
    def inc():
        nonlocal n
        n += 1
        return n
    return inc

c = counter()
print(c(), c(), c())
```

8.
```python
try:
    x = [1, 2][5]
except IndexError:
    x = -1
finally:
    print("checked")
print(x)
```

9.
```python
words = ["apple", "Banana", "cherry"]
print(sorted(words))
print(sorted(words, key=str.lower))
```

10.
```python
a = {1, 2, 3}
b = {2, 3, 4}
print(a & b, a | b, a - b)
```

---

## Section F: Debugging tasks (10 questions)

Each snippet has exactly one bug. Identify it and write the corrected version.

1.
```python
def area(radius):
    return 3.14 * radius * radius

print(area(5)
```

2.
```python
scores = {"Alex": 90, "Sam": 85}
print(scores["Jordan"])
```

3.
```python
for i in range(10):
if i % 2 == 0:
    print(i)
```

4.
```python
def total(items = []):
    items.append(1)
    return items
```

5.
```python
name = "Alex"
age = 30
print("Name: " + name + " Age: " + age)
```

6.
```python
with open("data.txt", "r") as f
    content = f.read()
```

7.
```python
def is_adult(age):
    if age >= 18
        return True
    return False
```

8.
```python
class InvalidAgeError(Exception)
    pass
```

9.
```python
values = [1, 2, 3]
print(values[3])
```

10.
```python
import Math
print(Math.sqrt(16))
```

---

## Practical exam (timed, approximately 2 hours)

Build a small command-line inventory tracker, working solo, without referring back to the lessons unless you're genuinely stuck (open-book on documentation like the official Python docs is fine, that's realistic; open-book on this course's own worked examples defeats the point).

Requirements:

- Load starting inventory from a CSV file (`name`, `quantity`, `price`)
- Support adding new items, updating quantity, and removing items
- Save changes back to the CSV after every operation
- Handle a missing or malformed CSV file without crashing
- Include at least one custom exception for a business rule of your choosing (for example, quantity can't go negative)
- Provide a simple menu-driven CLI

You'll be evaluated on:

- Correctness: does it actually do what's asked
- Efficiency: no obviously wasteful approaches, like reloading the entire file from disk on every single read
- Readability: would another developer understand this without you explaining it out loud
- Maintainability: is it organized into functions with clear responsibilities, not one long block
- Naming: are variables and functions named for what they represent
- Logic: are edge cases (empty file, duplicate item names, invalid input) actually handled, not just the happy path

## Mock technical interview

For this final piece, come back and tell me you're ready, and I'll switch into interviewer mode: a PwC-style senior engineer conducting a real 45-minute technical screen. Expect questions pulled from everything in this module, asked one at a time, with follow-ups if your first answer is vague. I'll push back on hand-wavy answers the way a real interviewer would, not to be difficult, but because that's genuinely what the screen is for. At the end, you'll get a scored evaluation covering technical accuracy, communication clarity, and how you handled the questions you didn't immediately know, plus an honest read on whether you'd have passed.

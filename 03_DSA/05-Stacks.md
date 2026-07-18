# Lesson 5: Stacks

## 1. Learning objectives

By the end of this lesson you should be able to:

- Explain the LIFO principle precisely and identify real situations where it's the right model
- Implement a stack using Python's list and using a custom class with proper encapsulation
- Use a stack to solve the canonical stack problems: balanced parentheses, undo/redo, expression evaluation
- Explain when a stack is the right tool and when it's being reached for out of habit
- Recognize the call stack as a concrete, always-running example of stack behavior

## 2. Prerequisites

Lesson 3 (Lists). A stack is built on top of list operations, so you need list complexity solid.

## 3. Introduction

A stack is the data structure behind undo buttons, browser back navigation, recursive function calls, and expression parsers. It's simple in concept — the last thing added is the first thing removed — but that specific ordering property is what makes it exactly right for problems where you need to "remember where you came from" or "reverse the order of operations." Understanding stacks well enough to reach for them naturally, rather than only after being told "use a stack here," is the actual goal of this lesson.

## 4. Theory

A stack is a linear data structure that follows the **Last In, First Out (LIFO)** principle: the last element pushed onto the stack is the first element popped off. The two core operations are:

- **Push:** add an element to the top of the stack
- **Pop:** remove and return the element at the top

Additional operations:
- **Peek (or Top):** look at the top element without removing it
- **isEmpty:** check whether the stack has any elements

```
Push 1:  [1]
Push 2:  [1, 2]
Push 3:  [1, 2, 3]
Pop:     [1, 2]  → returns 3
Pop:     [1]     → returns 2
Peek:    [1]     → returns 1 (stack unchanged)
```

The right side of this diagram is the "top" of the stack — the last element pushed, and the first that would be popped.

## 5. Why this concept exists

Some problems are inherently LIFO in structure. The most common pattern: you're processing a sequence of items and need to "undo" or "go back" in the exact reverse order of how you went forward. Function calls follow this pattern: the most recently called function must return before any earlier function can continue. Parsing nested structures (brackets, HTML tags, directory paths) follows this pattern too: the most recently opened bracket must be the next one closed. A stack makes both of these feel natural rather than requiring careful manual index management.

## 6. Internal implementation

Python's list is a perfectly valid stack implementation, because `.append()` (push) and `.pop()` (pop from end) are both O(1) amortized. The "top" of the stack is the last element of the list:

```
Stack top → lst[-1]
Push x   → lst.append(x)
Pop      → lst.pop()
Peek     → lst[-1]
isEmpty  → len(lst) == 0
```

Alternatively, `collections.deque` can be used, though for pure stack operations (push and pop from the same end) a list is entirely appropriate and idiomatic.

## 7. Real-world analogy

A stack of dinner plates. You add plates to the top (push) and remove plates from the top (pop). You can't take the bottom plate without first removing every plate above it. The plate most recently placed is the first one used. When a kitchen runs out of clean plates and gets a fresh stack from the dishwasher, the last plate placed on the stack gets used first (assuming they dry off sequentially). That LIFO behavior is the defining property.

## 8. Enterprise use cases

**Undo/redo functionality:** Every action is pushed onto an undo stack. Ctrl+Z pops the most recent action and reverses it; Ctrl+Y pushes it onto a redo stack. The LIFO ordering is what makes "undo the most recent thing first" work naturally.

**Browser back navigation:** Each visited URL is pushed onto a history stack. Clicking "Back" pops the current URL, revealing the previous one.

**Call stack:** Python's own execution model is a stack. Each function call pushes a frame; each return pops it. When a function calls another function, the new call is on top. This is what the traceback is showing you — the current state of the call stack at the moment of an error.

**Expression evaluation and parsing:** Compilers and interpreters use stacks to parse and evaluate nested expressions: `((3 + 4) * (2 - 1))`. Open parentheses are pushed; when a close parenthesis is encountered, the most recent open parenthesis is popped and the subexpression evaluated.

**Depth-first search:** Graph traversal algorithms often use an explicit stack (or the call stack via recursion) to track which nodes to visit next, always visiting the most recently discovered node first.

## 9. Complexity analysis

| Operation | Complexity | Notes |
|---|---|---|
| Push (`append`) | O(1) amortized | Same as list append |
| Pop (`pop()`) | O(1) amortized | Removes from end of list |
| Peek (`lst[-1]`) | O(1) | No modification |
| isEmpty (`len == 0`) | O(1) | |
| Search | O(n) | Not a primary stack operation |

All core stack operations are O(1). This is what makes stacks efficient: the LIFO constraint means every operation always happens at the top, so no shifting or scanning is ever needed.

## 10. Step-by-step visual walkthrough

**Balanced parentheses checker — the canonical stack problem:**

Input: `"({[]})"` — should return `True`
Input: `"({[})"` — should return `False`

```
Process '('  → push → stack: ['(']
Process '{'  → push → stack: ['(', '{']
Process '['  → push → stack: ['(', '{', '[']
Process ']'  → closing bracket
             → pop top: '[' — does '[' match ']'? YES
             → stack: ['(', '{']
Process '}'  → closing bracket
             → pop top: '{' — does '{' match '}'? YES
             → stack: ['(']
Process ')'  → closing bracket
             → pop top: '(' — does '(' match ')'? YES
             → stack: []
End of string → stack is empty → BALANCED ✓

---

Process '('  → push → stack: ['(']
Process '{'  → push → stack: ['(', '{']
Process '['  → push → stack: ['(', '{', '[']
Process '}'  → closing bracket
             → pop top: '[' — does '[' match '}'? NO → UNBALANCED ✗
```

The stack naturally tracks which opening bracket is "most recently unmatched," which is exactly what you need to correctly pair nested brackets.

## 11. Syntax

**Using Python's list as a stack:**

```python
stack = []

# Push
stack.append(1)
stack.append(2)
stack.append(3)

# Peek
top = stack[-1]           # 3 — doesn't modify the stack
print(f"Top: {top}")

# Pop
item = stack.pop()        # removes and returns 3
print(f"Popped: {item}")

# Check empty
if not stack:
    print("Stack is empty")

print(stack)  # [1, 2]
```

**Encapsulated stack class:**

```python
class Stack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek at empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items})"
```

**Balanced parentheses — complete implementation:**

```python
def is_balanced(expression):
    stack = []
    matching = {')': '(', ']': '[', '}': '{'}

    for char in expression:
        if char in '([{':
            stack.append(char)
        elif char in ')]}':
            if not stack or stack[-1] != matching[char]:
                return False
            stack.pop()

    return len(stack) == 0

print(is_balanced("({[]})"))   # True
print(is_balanced("({[})"))    # False
print(is_balanced("((()))"))   # True
print(is_balanced("("))         # False — unclosed bracket remains on stack
```

## 12. Common mistakes

**Not checking for an empty stack before popping.** `stack.pop()` on an empty list raises `IndexError`. Always guard with `if not stack:` or `if stack.is_empty():` before popping.

**Using `pop(0)` instead of `pop()`.** `pop(0)` removes from the front (queue behavior, O(n) due to shifting), not the end. A stack always pops from the end (`pop()`, O(1)).

**Forgetting that a non-empty stack at the end of a balanced-check means unbalanced.** Even if every closing bracket matched correctly, a remaining open bracket on the stack means the input was not balanced.

**Using a stack where a queue is needed.** LIFO and FIFO are different. If the problem requires "process in the order received," that's a queue (Lesson 6), not a stack.

## 13. Debugging tips

If a recursive function is raising a `RecursionError`, that's the call stack overflowing — a real stack overflow. The fix is either to increase Python's recursion limit (rarely the right answer) or to convert the recursion to an explicit loop using your own stack, which removes the depth constraint.

If a parentheses checker is producing wrong results, print the stack state after each character to trace exactly where the first mismatch occurs.

## 14. Best practices

For simple stack usage in a single function, using a plain list directly is idiomatic and clear. For a stack that's passed around, used across methods, or needs controlled access (preventing callers from doing arbitrary list operations), wrap it in a class with named `push()`, `pop()`, and `peek()` methods. Always handle the empty stack case explicitly rather than letting an `IndexError` propagate unexpectedly.

## 15. Performance considerations

All core stack operations are O(1) amortized when using a Python list. The only scenario where a list-based stack has a performance consideration is the occasional O(n) resize, which is the same amortized-O(1) story as list append. For extremely high-throughput stack operations where even amortized cost matters, `collections.deque` provides guaranteed O(1) append and pop from both ends, though for pure stack behavior (one end only), the list is fine.

## 16. Code style

Use the encapsulated `Stack` class in production code so the stack's interface is explicit and the internal list can't be accidentally accessed via list methods that don't make semantic sense for a stack (like `.insert()` or `.sort()`). Use raw list stack operations (`append`/`pop`/`[-1]`) only in small, self-contained algorithms where the stack behavior is obvious from context.

## 17. Interview questions with model answers

**Q: Explain the LIFO principle and give a real-world example.**

LIFO means Last In, First Out: the most recently added element is the first to be removed. A real example: Python's call stack. When function A calls function B, B's stack frame is pushed on top of A's. B must complete and its frame must be popped before A can continue. The most recent function call is always the first to finish.

**Q: How would you implement a stack in Python?**

The simplest implementation uses a Python list: `append()` for push, `pop()` for pop, and `[-1]` for peek. All operations are O(1) amortized. For production use, I'd wrap it in a class with named `push`, `pop`, and `peek` methods, adding an `is_empty()` guard and a descriptive error message if pop is called on an empty stack, rather than letting a raw `IndexError` propagate.

**Q: Write a function to check whether a string of brackets is balanced.**

Walk through the balanced-parentheses solution: open brackets push to the stack, close brackets check the top for a matching open bracket and pop if matched. At the end, an empty stack means balanced. The key insight is that the stack naturally tracks the most recently unmatched open bracket, which is always the one that must be matched next, exactly what the LIFO property provides.

## 18. Knowledge check

1. What does LIFO stand for, and which stack operation implements each letter?
2. Why is `pop()` O(1) for a Python list but `pop(0)` is O(n)?
3. In the balanced parentheses problem, what does a non-empty stack at the end of the string indicate?
4. Name two real software features that use a stack as their underlying model.

## 19. Hands-on exercises

**Easy**

1. Using a plain list as a stack, push the numbers 1 through 5 and then pop them one at a time, printing each popped value.
2. Implement the `Stack` class from this lesson's syntax section, including the `is_empty()` guard on `pop()` and `peek()`.
3. Write a function that uses a stack to reverse a string.

**Medium**

4. Implement the `is_balanced()` function from this lesson's walkthrough, then test it on at least five different strings including at least one true edge case.
5. Write a function that uses a stack to evaluate a sequence of operations: given `[5, 3, '+', 2, '*']` (Reverse Polish Notation), push numbers onto the stack and when you encounter an operator, pop two values, apply the operation, and push the result.
6. Implement a `MinStack` class that supports standard `push()`, `pop()`, and `peek()`, plus a `get_min()` method that returns the current minimum value in O(1) time (hint: use a second stack to track minimums).

**Hard**

7. Implement an undo/redo system: a `TextEditor` class that supports `write(text)`, `undo()`, and `redo()` operations, using two stacks. Calling `undo()` should restore the previous state; calling `redo()` after an undo should restore the undone state. Writing after an undo should clear the redo history.
8. Write a function that evaluates a mathematical expression string like `"3 + 4 * 2"` using two stacks — one for values and one for operators — handling operator precedence correctly.

## 20. Stretch challenge

Implement a `CallStack` simulator that mimics Python's actual call stack behavior. Define a `FunctionCall` namedtuple with `name` and `local_vars` fields. Your `CallStack` class should support `call(function_name, **local_vars)` (which pushes a new frame), `return_from()` (which pops the current frame and returns its local vars), and `current_frame()` (peek). Write a short program that simulates the call stack state during a simple multi-function call sequence: `main()` calls `process()`, which calls `validate()`, which returns, then `process()` returns, then `main()` returns. Print the stack state at each step.

## 21. Summary

A stack is a LIFO data structure where all operations happen at the top. Push and pop are both O(1) with a Python list. Stacks appear naturally in problems where you need to reverse a sequence, track "where you came from," or process nested structures where the most recently opened context must be the next one closed. Python's own call stack is the most concrete example running at all times. Recognize stack-shaped problems by asking: "does the most recently added item need to come out first?" If yes, a stack is the right tool.

## 22. Additional resources

- [Python official docs: collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)
- [Wikipedia: Stack (abstract data type)](https://en.wikipedia.org/wiki/Stack_(abstract_data_type))
- [Visualgo: Stack visualization](https://visualgo.net/en/list)

# Lesson 6: Queues

## 1. Learning objectives

By the end of this lesson you should be able to:

- Explain the FIFO principle and identify problems where it's the correct model
- Implement a queue using `collections.deque` and explain why a plain list is the wrong choice for a queue
- Explain the concept of a circular queue and why it exists
- Use `queue.PriorityQueue` for priority-based processing
- Recognize queue-shaped problems in real backend engineering scenarios

## 2. Prerequisites

Lesson 5 (Stacks). Queues are the natural counterpart to stacks — same linear structure, opposite ordering — so having the stack mental model solid makes the contrast clearer.

## 3. Introduction

If a stack is about reversing order (the last thing in is the first thing out), a queue is about preserving it. The first thing in is the first thing out — exactly how a line at a ticket counter works, exactly how an email server processes messages, exactly how a task scheduler dispatches jobs to workers. Queues are everywhere in backend systems, and understanding when FIFO ordering is the right model, and how to implement it efficiently, is a core backend engineering skill.

## 4. Theory

A queue is a linear data structure that follows the **First In, First Out (FIFO)** principle: elements are added at one end (the **rear** or **back**) and removed from the other end (the **front**).

Core operations:
- **Enqueue:** add an element to the rear
- **Dequeue:** remove and return the element at the front
- **Peek (Front):** inspect the front element without removing it
- **isEmpty:** check whether the queue has any elements

```
Initial:          []
Enqueue "A":      [A]
Enqueue "B":      [A, B]
Enqueue "C":      [A, B, C]
Dequeue:          [B, C]     → returns "A"
Dequeue:          [C]        → returns "B"
Enqueue "D":      [C, D]
Dequeue:          [D]        → returns "C"
```

The left side is the front (next to be dequeued); the right side is the rear (where new items arrive).

## 5. Why this concept exists

Many real-world processes are inherently fair: whoever arrived first gets served first. A queue models this fairness guarantee precisely. Without it, you'd need complex bookkeeping to track arrival order. The queue data structure makes "serve in arrival order" the default behavior of every operation, with no additional logic required. It also decouples producers (things that add work) from consumers (things that do work), a pattern that appears constantly in distributed backend systems.

## 6. Internal implementation

**Why a plain list is the wrong choice for a queue:**

```python
# Naive queue using a list
queue = []
queue.append("A")    # enqueue — O(1) amortized ✓
queue.append("B")
queue.pop(0)          # dequeue — O(n) ✗ — shifts every element left
```

`list.pop(0)` is O(n) because every remaining element must shift one position left to fill the gap. For a queue processing 1 million messages, every dequeue operation triggers 999,999 shifts, making the whole operation O(n²).

**The right tool: `collections.deque`**

`deque` (double-ended queue) is implemented as a doubly-linked list of fixed-size blocks. It provides O(1) append and pop from **both ends**, making it the correct Python queue implementation:

```python
from collections import deque

queue = deque()
queue.append("A")       # enqueue at rear — O(1)
queue.append("B")
queue.popleft()          # dequeue from front — O(1)
```

`deque.popleft()` is O(1) because it simply advances the front pointer rather than shifting elements.

## 7. Real-world analogy

A queue is a line of customers at a bank. The first customer in line is the first served (FIFO). New customers join at the back. The teller serves whoever is at the front. Nobody cuts in line (assuming fair queuing). The bank doesn't care how many people are behind the current customer — serving the front is always O(1), regardless of queue length.

A priority queue (covered below) is like a hospital emergency department: patients are not served strictly in arrival order but in order of medical urgency. A critical patient who arrives after three minor cases still gets seen first.

## 8. Enterprise use cases

**Message queues:** Systems like RabbitMQ and AWS SQS are literally queues at scale: producers publish messages at the rear, consumers read them from the front, in order, ensuring every message is processed exactly once in arrival order.

**Task schedulers:** A background job system (Celery, RQ) queues tasks for worker processes. Tasks submitted first are picked up first, ensuring fair ordering.

**Rate limiting:** API rate limiters track the timestamps of recent requests in a queue. When a new request arrives, expired timestamps are dequeued from the front, and the queue length determines whether the rate limit has been exceeded.

**Breadth-first search:** Graph traversal algorithms use a queue to visit nodes level by level — visit all nodes at distance 1 before any at distance 2. BFS produces the shortest path in an unweighted graph precisely because of FIFO ordering.

**Print spoolers:** Documents sent to a printer are queued. The first document sent prints first.

## 9. Complexity analysis

| Operation | list | deque | Notes |
|---|---|---|---|
| Enqueue (add to rear) | O(1) amortized | O(1) | `append()` on both |
| Dequeue (remove from front) | O(n) | O(1) | `pop(0)` vs `popleft()` |
| Peek front | O(1) | O(1) | `lst[0]` vs `dq[0]` |
| isEmpty | O(1) | O(1) | `len() == 0` |
| Size | O(1) | O(1) | `len()` |

The critical difference is dequeue from the front: O(n) for a list, O(1) for a deque. For any real queue workload, use `deque`.

## 10. Step-by-step visual walkthrough

**Rate limiter using a queue — a real backend pattern:**

Scenario: Allow at most 5 API requests per 10-second window. Track request timestamps in a deque.

```
Window = 10 seconds, Limit = 5 requests

Request at t=1:   queue=[1]           len=1 ≤ 5 → ALLOWED
Request at t=3:   queue=[1,3]         len=2 ≤ 5 → ALLOWED
Request at t=5:   queue=[1,3,5]       len=3 ≤ 5 → ALLOWED
Request at t=7:   queue=[1,3,5,7]     len=4 ≤ 5 → ALLOWED
Request at t=9:   queue=[1,3,5,7,9]   len=5 ≤ 5 → ALLOWED
Request at t=10:
  → Remove expired: t=1 is ≤ (10-10)=0? No, t=1 > 0, keep it
  → queue=[1,3,5,7,9,10]  len=6 > 5 → DENIED
Request at t=12:
  → Remove expired: t=1 ≤ (12-10)=2? Yes, dequeue t=1
  → t=3 ≤ 2? No, stop.
  → queue=[3,5,7,9,12]  len=5 ≤ 5 → ALLOWED
```

The queue's FIFO property means the oldest timestamps are always at the front, ready to be expired. This is a pattern you'll implement in real backend systems.

## 11. Syntax

**Basic queue with `collections.deque`:**

```python
from collections import deque

queue = deque()

# Enqueue
queue.append("task_1")
queue.append("task_2")
queue.append("task_3")

print(queue)          # deque(['task_1', 'task_2', 'task_3'])
print(queue[0])       # 'task_1' — peek front

# Dequeue
task = queue.popleft()
print(task)           # 'task_1'
print(queue)          # deque(['task_2', 'task_3'])

# isEmpty
print(len(queue) == 0)  # False
```

**Bounded deque (maxlen):**

```python
from collections import deque

# A sliding window of the last 5 items — automatically discards oldest
recent = deque(maxlen=5)
for i in range(10):
    recent.append(i)
    print(list(recent))
# Once full, appending to a maxlen deque drops from the opposite end automatically
# Final state: deque([5, 6, 7, 8, 9])
```

**Encapsulated Queue class:**

```python
from collections import deque

class Queue:
    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self._items.popleft()

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek at empty queue")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)

    def __repr__(self):
        return f"Queue({list(self._items)})"
```

**Priority Queue:**

```python
import queue

pq = queue.PriorityQueue()

# Items are tuples: (priority, data) — lower number = higher priority
pq.put((3, "low priority task"))
pq.put((1, "critical task"))
pq.put((2, "medium task"))

while not pq.empty():
    priority, task = pq.get()
    print(f"Processing ({priority}): {task}")

# Output:
# Processing (1): critical task
# Processing (2): medium task
# Processing (3): low priority task
```

**Circular queue concept:**

A circular queue (ring buffer) uses a fixed-size array with `front` and `rear` pointers that wrap around when they reach the end. This avoids the wasted space of a naive array-based queue where the front of the array stays empty after dequeuing.

```python
class CircularQueue:
    def __init__(self, capacity):
        self.capacity = capacity
        self._items = [None] * capacity
        self._front = 0
        self._rear = 0
        self._size = 0

    def enqueue(self, item):
        if self._size == self.capacity:
            raise OverflowError("Queue is full")
        self._items[self._rear] = item
        self._rear = (self._rear + 1) % self.capacity
        self._size += 1

    def dequeue(self):
        if self._size == 0:
            raise IndexError("Dequeue from empty queue")
        item = self._items[self._front]
        self._items[self._front] = None
        self._front = (self._front + 1) % self.capacity
        self._size -= 1
        return item

    def peek(self):
        if self._size == 0:
            raise IndexError("Empty queue")
        return self._items[self._front]

    def is_empty(self):
        return self._size == 0

    def is_full(self):
        return self._size == self.capacity
```

## 12. Common mistakes

**Using `list.pop(0)` for dequeue.** This is O(n) and degrades badly at scale. Always use `deque.popleft()` for queue dequeue operations.

**Confusing a queue with a stack.** A queue is FIFO (serve in arrival order); a stack is LIFO (serve most recently added first). Mixing them up produces reversed ordering, which is usually a subtle bug.

**Not handling the empty queue case before dequeuing.** `deque.popleft()` on an empty deque raises `IndexError`. Guard with `if not queue:` before dequeuing.

**Using a simple queue when priority ordering is needed.** If tasks have different urgencies, a simple FIFO queue will process low-priority tasks before urgent ones if they arrived first. Use `queue.PriorityQueue` when priority matters.

## 13. Debugging tips

If items are coming out in the wrong order, verify which end you're adding to and removing from. Adding and removing from the same end is a stack; adding to one end and removing from the other is a queue. If a queue is growing unboundedly in a long-running system, check whether consumers are keeping up with producers, or whether a dequeue condition is never being triggered.

## 14. Best practices

Always use `collections.deque` for queue implementations, never a plain list with `pop(0)`. When the queue size is naturally bounded (a fixed-size buffer, a sliding window), use `deque(maxlen=n)`, which automatically discards the oldest element when full. Use `queue.PriorityQueue` for priority-based task scheduling; its thread-safe implementation is appropriate for multi-threaded backend workers.

## 15. Performance considerations

`collections.deque` provides O(1) append and popleft, making it the correct choice for queue behavior. Its internal doubly-linked list of fixed-size blocks means it doesn't require contiguous memory, so it handles large queues efficiently without the periodic O(n) resizes that list-based queues would trigger. Random access (`dq[5]`) is O(n) on a deque, unlike a list — but random access isn't a queue operation, so this tradeoff is acceptable.

## 16. Code style

Name queue instances semantically: `task_queue`, `message_queue`, `request_queue`. Use `deque` directly for simple in-function queue usage; wrap in a `Queue` class with `enqueue`/`dequeue` methods when the queue is passed around or needs to communicate intent clearly. Always document whether a queue is FIFO or priority-based at the point of creation.

## 17. Interview questions with model answers

**Q: Why shouldn't you use a Python list as a queue?**

Because `list.pop(0)` — which dequeues from the front — is O(n). It shifts every remaining element one position to the left to fill the gap. In a system processing 1 million messages, each dequeue triggers up to 1 million shifts, making the whole processing loop O(n²). `collections.deque.popleft()` is O(1) because it advances a pointer without shifting any elements.

**Q: What's the difference between a queue and a stack?**

A queue is FIFO: the first element added is the first removed, preserving arrival order. A stack is LIFO: the last element added is the first removed, reversing arrival order. They're used for different problems: queues for fair ordered processing (task schedulers, message queues), stacks for reversal and nested-structure parsing (undo, bracket matching, recursion).

**Q: What is a priority queue and when would you use one?**

A priority queue is a queue variant where each element has a priority, and elements are dequeued in priority order rather than arrival order. You'd use it when work items have different urgency — a hospital triage system, a background job scheduler where critical jobs must run before low-priority ones, or Dijkstra's shortest path algorithm, which always processes the closest unvisited node next.

## 18. Knowledge check

1. What does FIFO stand for, and which queue operation maps to each letter?
2. Why is `list.pop(0)` O(n) while `deque.popleft()` is O(1)?
3. What happens when you append to a `deque(maxlen=5)` that's already full?
4. Name two real backend systems that rely on queue behavior at their core.

## 19. Hands-on exercises

**Easy**

1. Using `collections.deque`, implement a simple print spooler: enqueue five document names, then dequeue and "print" (print to screen) each one in order.
2. Implement the `Queue` class from this lesson's syntax section and test `enqueue`, `dequeue`, `peek`, and `is_empty` with at least three items.
3. Create a `deque(maxlen=3)` and append the numbers 1 through 7 one at a time, printing the deque state after each append.

**Medium**

4. Implement a simple **task scheduler**: tasks are tuples of `(name, duration_seconds)`. Build a queue of five tasks, process them in order by dequeueing each one and printing its name and simulated completion time (running total of durations).
5. Implement the rate limiter described in the visual walkthrough: a function `is_allowed(timestamp, queue, window, limit)` that returns `True` if the request should be allowed, and `False` if it exceeds the rate limit. Remove expired timestamps from the front of the queue before checking.
6. Implement **BFS level-order printing**: given a simple tree represented as a dictionary `{node: [children]}`, use a queue to print all nodes level by level.

**Hard**

7. Implement the `CircularQueue` class from this lesson's syntax section fully, then write a test that fills it to capacity, dequeues half the items, fills it again, and confirms the wrap-around behavior works correctly.
8. Build a **multi-priority task queue** using `queue.PriorityQueue`: tasks are tuples of `(priority, arrival_time, name)` where lower priority number = higher urgency, and ties in priority are broken by arrival order. Enqueue 10 tasks with mixed priorities, then dequeue and process them all, confirming the output is correctly ordered.

## 20. Stretch challenge

Implement a simplified **message broker** inspired by systems like RabbitMQ. Your `MessageBroker` class should support:
- `create_queue(name)` — creates a named queue
- `publish(queue_name, message)` — adds a message to a named queue
- `consume(queue_name)` — dequeues and returns the oldest message
- `subscribe(queue_name, handler)` — registers a callable; when `dispatch(queue_name)` is called, the oldest message is consumed and passed to every registered handler

Use `collections.deque` internally. This exercise is a direct model of how real message queue systems work at a conceptual level: producers publish, consumers subscribe, and messages flow through in order.

## 21. Summary

A queue is a FIFO data structure: first in, first out. It models any process where arrival order determines service order. Always use `collections.deque` for Python queue implementations — `deque.popleft()` is O(1), while `list.pop(0)` is O(n), a difference that becomes catastrophic at scale. `deque(maxlen=n)` provides a bounded sliding window that automatically expires old elements. For priority-based ordering where urgency matters more than arrival time, `queue.PriorityQueue` handles the ordering correctly. Queues appear throughout backend systems: message queues, task schedulers, rate limiters, BFS traversal.

## 22. Additional resources

- [Python official docs: collections.deque](https://docs.python.org/3/library/collections.html#collections.deque)
- [Python official docs: queue module](https://docs.python.org/3/library/queue.html)
- [Wikipedia: Queue (abstract data type)](https://en.wikipedia.org/wiki/Queue_(abstract_data_type))
- [Visualgo: Queue visualization](https://visualgo.net/en/list)

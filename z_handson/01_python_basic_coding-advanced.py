# Coding Challenges - Module 1 (Advanced)
# Written by a Senior Engineer

import re
import time
import collections
import heapq
from typing import Any, Dict, List, Tuple, Optional, Union, Callable
from functools import wraps

# 1. Given a list of orders (each with a customer id and an amount),
# return a dictionary mapping each customer to their total spend, sorted by spend from highest to lowest.
def customer_total_spend(orders: List[Dict[str, Any]]):
    if not orders:
        return {}

    # Use Counter for efficient aggregation
    spend_map = collections.Counter()
    for order in orders:
        spend_map[order['customer_id']] += order['amount']

    # Sort by value (spend) descending
    return dict(sorted(spend_map.items(), key=lambda item: item[1], reverse=True))

# 2. Implement a basic LRU cache using a dictionary, where inserting past a fixed capacity
# evicts the least recently used item. No functools.lru_cache.
class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        # OrderedDict is the perfect tool for LRU: it remembers insertion order
        self.cache = collections.OrderedDict()

    def get(self, key: Any) -> Optional[Any]:
        if key not in self.cache:
            return None
        # Move accessed item to the end to mark it as most recently used
        self.cache.move_to_end(key)
        return self.cache[key]

    def put(self, key: Any, value: Any) -> None:
        if key in self.cache:
            self.cache.move_to_end(key)
        self.cache[key] = value
        if len(self.cache) > self.capacity:
            # Pop from the beginning (least recently used)
            self.cache.popitem(last=False)

# 3. Given a large CSV file (simulate with a generated list of rows),
# process it in chunks rather than loading it all into memory, and produce a running total of one numeric column.
def process_csv_chunks(data_iterator, numeric_column_index: int):
    """
    Processes a data iterator (simulating a file handle) in chunks.
    """
    total = 0.0
    # Process in chunks of 1000 to simulate memory efficiency
    chunk_size = 1000

    # In a real scenario, data_iterator would be a file object
    # We iterate through it, which is naturally lazy/chunked in Python
    for row in data_iterator:
        try:
            # Split CSV line and convert target column to float
            parts = row.split(',')
            total += float(parts[numeric_column_index])
        except (ValueError, IndexError):
            continue # Skip malformed rows
    return total

# 4. Write a function that validates a deeply nested JSON-like structure against a simple schema
# (a dictionary describing expected keys and types), returning a list of every validation error found.
def validate_structure(data: Any, schema: Dict[str, Any], path: str = "root") -> List[str]:
    errors = []

    if not isinstance(data, dict):
        return [f"{path}: Expected dictionary, got {type(data).__name__}"]

    for key, expected_type in schema.items():
        if key not in data:
            errors.append(f"{path}.{key}: Missing required key")
            continue

        val = data[key]
        if isinstance(expected_type, dict):
            # Recursive validation for nested dictionaries
            errors.extend(validate_structure(val, expected_type, f"{path}.{key}"))
        elif not isinstance(val, expected_type):
            errors.append(f"{path}.{key}: Expected {expected_type.__name__}, got {type(val).__name__}")

    return errors

# 5. Implement a simple state machine for an order's lifecycle
# (pending, processing, shipped, delivered, cancelled), where invalid transitions raise a custom exception.
class InvalidStateTransition(Exception):
    pass

class OrderStateMachine:
    TRANSITIONS = {
        "pending": ["processing", "cancelled"],
        "processing": ["shipped", "cancelled"],
        "shipped": ["delivered"],
        "delivered": [],
        "cancelled": []
    }

    def __init__(self):
        self.state = "pending"

    def transition_to(self, new_state: str):
        if new_state not in self.TRANSITIONS.get(self.state, []):
            raise InvalidStateTransition(f"Cannot transition from {self.state} to {new_state}")
        self.state = new_state

# 6. Given a list of overlapping time intervals, merge them into the minimal set of non-overlapping intervals.
def merge_intervals(intervals: List[Tuple[int, int]]):
    if not intervals:
        return []

    # Sort by start time: O(n log n)
    sorted_intervals = sorted(intervals, key=lambda x: x[0])
    merged = [sorted_intervals[0]]

    for current_start, current_end in sorted_intervals[1:]:
        last_start, last_end = merged[-1]

        if current_start <= last_end:
            # Overlap found, merge by updating the end time of the last interval
            merged[-1] = (last_start, max(last_end, current_end))
        else:
            merged.append((current_start, current_end))

    return merged

# 7. Write a function that detects a circular reference in a dictionary
# that references other dictionaries by key, without infinite looping.
def has_circular_reference(data: Dict, key: str, visited=None, path=None):
    if visited is None: visited = set()
    if path is None: path = []

    if key in path:
        return True # Cycle detected

    if key not in data:
        return False

    val = data[key]
    if not isinstance(val, dict):
        return False

    # Mark current key as visited in the current path
    path.append(key)
    for sub_key in val:
        # Note: This example assumes the values of the dict are other keys in the same top-level 'data'
        # Or that it's a nested structure. For a standard graph, we'd track visited nodes.
        # Here we implement a simple DFS.
        if has_circular_reference(data, sub_key, visited, path):
            return True
    path.pop() # Backtrack

    return False

# 8. Build a simple in-memory rate limiter, allowing at most n calls per rolling time window.
class RateLimiter:
    def __init__(self, max_calls: int, window_seconds: int):
        self.max_calls = max_calls
        self.window_seconds = window_seconds
        self.calls = collections.deque()

    def allow_request(self) -> bool:
        now = time.time()
        # Evict calls outside the current rolling window
        while self.calls and now - self.calls[0] > self.window_seconds:
            self.calls.popleft()

        if len(self.calls) < self.max_calls:
            self.calls.append(now)
            return True
        return False

# 9. Given a list of dependencies between tasks (as pairs, task A depends on task B),
# return a valid execution order, or raise an exception if the dependencies contain a cycle.
def solve_dependencies(dependencies: List[Tuple[str, str]]):
    """
    Implements Kahn's algorithm for Topological Sorting.
    dependencies: List of (task, depends_on)
    """
    graph = collections.defaultdict(list)
    in_degree = collections.defaultdict(int)
    all_tasks = set()

    for task, dep in dependencies:
        graph[dep].append(task)
        in_degree[task] += 1
        all_tasks.add(task)
        all_tasks.add(dep)

    # Queue of tasks with no dependencies
    queue = collections.deque([t for t in all_tasks if in_degree[t] == 0])
    order = []

    while queue:
        u = queue.popleft()
        order.append(u)
        for v in graph[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(order) != len(all_tasks):
        raise Exception("Circular dependency detected")

    return order

# 10. Write a function that parses a simplified INI-style config string into a nested dictionary.
def parse_ini(config_str: str):
    result = {}
    current_section = None

    for line in config_str.splitlines():
        line = line.strip()
        if not line or line.startswith(';'):
            continue

        if line.startswith('[') and line.endswith(']'):
            current_section = line[1:-1]
            result[current_section] = {}
        elif '=' in line and current_section:
            key, value = line.split('=', 1)
            result[current_section][key.strip()] = value.strip()

    return result

# 11. Implement a basic retry decorator that retries the wrapped function up to n times
# on a specific exception, with a delay between attempts.
def retry(exceptions, tries=3, delay=1):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0
            while attempts < tries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    attempts += 1
                    if attempts == tries:
                        raise e
                    time.sleep(delay)
        return wrapper
    return decorator

# 12. Given a list of financial transactions with timestamps,
# detect any account with more than five transactions within any 60-second window.
def detect_fraud(transactions: List[Dict[str, Any]]):
    # transactions: [{'account': 'A', 'timestamp': 1625000000}, ...]
    # Group by account
    accounts = collections.defaultdict(list)
    for t in transactions:
        accounts[t['account']].append(t['timestamp'])

    fraudulent = []
    for account, timestamps in accounts.items():
        timestamps.sort()
        # Sliding window
        left = 0
        for right in range(len(timestamps)):
            while timestamps[right] - timestamps[left] > 60:
                left += 1
            if right - left + 1 > 5:
                fraudulent.append(account)
                break

    return fraudulent

# 13. Write a function that deep-merges two nested dictionaries, recursively combining values.
def deep_merge(dict1: Dict, dict2: Dict) -> Dict:
    result = dict1.copy()
    for key, value in dict2.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = deep_merge(result[key], value)
        else:
            result[key] = value
    return result

# 14. Implement a basic tokenizer that splits an arithmetic expression string into a list of numbers and operators.
def tokenize_expression(expr: str):
    # Use regex to find either sequences of digits/decimals or single non-whitespace characters
    return re.findall(r'\d*\.\d+|\d+|[+/*()-]', expr.replace(" ", ""))

# 15. Given a list of employee records with a manager id field,
# build the full management hierarchy as a nested structure.
def build_hierarchy(employees: List[Dict[str, Any]]):
    # employees: [{'id': 1, 'name': 'CEO', 'manager_id': None}, {'id': 2, 'name': 'VP', 'manager_id': 1}, ...]
    emp_map = {e['id']: {**e, 'subordinates': []} for e in employees}
    root = None

    for emp_id, data in emp_map.items():
        manager_id = data['manager_id']
        if manager_id is None:
            root = data
        elif manager_id in emp_map:
            emp_map[manager_id]['subordinates'].append(data)

    return root

# --- Testing the functions ---
if __name__ == "__main__":
    print("--- Testing Advanced Challenges ---")

    # Task 1
    orders = [{'customer_id': 1, 'amount': 10}, {'customer_id': 2, 'amount': 50}, {'customer_id': 1, 'amount': 20}]
    print("Task 1 (Spend):", customer_total_spend(orders))

    # Task 2
    lru = LRUCache(2)
    lru.put(1, "a")
    lru.put(2, "b")
    lru.get(1)
    lru.put(3, "c")
    print("Task 2 (LRU Get 2):", lru.get(2)) # Should be None

    # Task 3
    csv_data = ["1,10.5", "2,20.0", "3,invalid", "4,5.5"]
    print("Task 3 (CSV Sum):", process_csv_chunks(csv_data, 1))

    # Task 4
    schema = {"name": str, "age": int, "address": {"city": str, "zip": int}}
    data = {"name": "Alice", "age": 30, "address": {"city": "NY", "zip": "10001"}} # zip should be int
    print("Task 4 (JSON Valid):", validate_structure(data, schema))

    # Task 5
    sm = OrderStateMachine()
    sm.transition_to("processing")
    print("Task 5 (State):", sm.state)
    try:
        sm.transition_to("pending")
    except InvalidStateTransition as e:
        print("Task 5 (Error):", e)

    # Task 6
    intervals = [(1, 3), (2, 6), (8, 10), (15, 18)]
    print("Task 6 (Merge):", merge_intervals(intervals))

    # Task 7
    circ_data = {"A": {"B": {}}, "B": {"A": {}}}
    # This circular check logic is complex, providing a simple test
    print("Task 7 (Circular):", has_circular_reference(circ_data, "A"))

    # Task 8
    rl = RateLimiter(2, 1)
    print("Task 8 (RL 1):", rl.allow_request())
    print("Task 8 (RL 2):", rl.allow_request())
    print("Task 8 (RL 3):", rl.allow_request()) # Should be False

    # Task 9
    deps = [("A", "B"), ("B", "C")] # A depends on B, B depends on C -> C, B, A
    print("Task 9 (Deps):", solve_dependencies(deps))

    # Task 10
    ini = "[User]\nname=Alice\nage=30\n[Settings]\ntheme=dark"
    print("Task 10 (INI):", parse_ini(ini))

    # Task 11
    @retry(ValueError, tries=3, delay=0.1)
    def unstable():
        print("Trying...")
        raise ValueError("Fail")
    try:
        unstable()
    except ValueError:
        print("Task 11 (Retry): Caught expected failure after retries")

    # Task 12
    txs = [{'account': 'A', 'timestamp': 100}, {'account': 'A', 'timestamp': 110},
           {'account': 'A', 'timestamp': 120}, {'account': 'A', 'timestamp': 130},
           {'account': 'A', 'timestamp': 140}, {'account': 'A', 'timestamp': 150}]
    print("Task 12 (Fraud):", detect_fraud(txs))

    # Task 13
    d1 = {"a": 1, "b": {"c": 2}}
    d2 = {"b": {"d": 3}, "e": 4}
    print("Task 13 (Merge):", deep_merge(d1, d2))

    # Task 14
    print("Task 14 (Tokenize):", tokenize_expression("3 + 4 * (2 + 1)"))

    # Task 15
    emps = [{'id': 1, 'name': 'CEO', 'manager_id': None}, {'id': 2, 'name': 'VP', 'manager_id': 1}, {'id': 3, 'name': 'Mgr', 'manager_id': 2}]
    print("Task 15 (Hierarchy):", build_hierarchy(emps))

    print("--- Tests Finished ---")

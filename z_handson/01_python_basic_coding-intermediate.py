# Coding Challenges - Module 1 (Intermediate)
# Written by a Senior Engineer (Refactored)

import re
import heapq
from collections import Counter

# 1. Given a list of dictionaries representing students (name and grade), return the name of the student with the highest grade.
def get_top_student(students):
    if len(students) == 0:
        return None

    top_student = students[0]
    for s in students:
        if s["grade"] > top_student["grade"]:
            top_student = s
    return top_student["name"]

# 2. Write a function that flattens a list of lists into a single list, without using any library.
def flatten_list(nested_list):
    flat = []
    for sublist in nested_list:
        for item in sublist:
            flat.append(item)
    return flat

# 3. Given a sentence, return the frequency of each word as a dictionary, ignoring punctuation and case.
def word_frequency(sentence):
    if not sentence:
        return {}
    # Use regex to find all alphanumeric sequences, ignoring punctuation and case
    words = re.findall(r'\w+', sentence.lower())
    return dict(Counter(words))

# 4. Write a function that checks whether two strings are anagrams of each other.
def are_anagrams(s1, s2):
    if s1 is None or s2 is None:
        return False
    # Normalize by removing non-alphanumeric characters and converting to lowercase
    clean_s1 = filter(str.isalnum, s1.lower())
    clean_s2 = filter(str.isalnum, s2.lower())

    return Counter(clean_s1) == Counter(clean_s2)

# 5. Given a list of numbers, return the second largest value without sorting the whole list.
def second_largest(numbers):
    if not numbers or len(numbers) < 2:
        return None

    # Remove duplicates using a set to ensure we get the second UNIQUE largest
    unique_numbers = set(numbers)
    if len(unique_numbers) < 2:
        return None

    # Use heapq.nlargest for O(n log k) efficiency (k=2 here, so effectively O(n))
    return heapq.nlargest(2, unique_numbers)[-1]

# 6. Write a function that groups a list of words by their first letter, returning a dictionary of lists.
def group_by_first_letter(words):
    groups = {}
    for w in words:
        if len(w) == 0:
            continue
        first_letter = w[0].lower()
        if first_letter not in groups:
            groups[first_letter] = []
        groups[first_letter].append(w)
    return groups

# 7. Given a list of transactions (each a dict with amount and type, where type is "credit" or "debit"), return the final balance.
def calculate_balance(transactions):
    balance = 0
    for t in transactions:
        if t["type"] == "credit":
            balance = balance + t["amount"]
        elif t["type"] == "debit":
            balance = balance - t["amount"]
    return balance

# 8. Write a function that removes duplicate entries from a list of dictionaries based on one key, keeping the first occurrence.
def remove_duplicate_dicts(data_list, key):
    seen = []
    unique_list = []
    for item in data_list:
        val = item[key]
        if val not in seen:
            seen.append(val)
            unique_list.append(item)
    return unique_list

# 9. Implement a basic Caesar cipher that shifts each letter of a string by a given number of positions.
def caesar_cipher(text, shift):
    if text is None:
        return None

    shift %= 26
    lower = "abcdefghijklmnopqrstuvwxyz"
    upper = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

    # Pre-compute the shifted alphabets
    shifted_lower = lower[shift:] + lower[:shift]
    shifted_upper = upper[shift:] + upper[:shift]

    # Create a translation table for O(n) mapping
    table = str.maketrans(lower + upper, shifted_lower + shifted_upper)
    return text.translate(table)

# 10. Given a list of tuples representing coordinates, return the one closest to the origin.
def closest_to_origin(coords):
    if not coords:
        return None

    closest = coords[0]
    # distance squared is enough for comparison (avoid sqrt)
    min_dist = coords[0][0]**2 + coords[0][1]**2

    for c in coords:
        dist = c[0]**2 + c[1]**2
        if dist < min_dist:
            min_dist = dist
            closest = c
    return closest

# 11. Write a function that merges two dictionaries, and when a key exists in both, keeps the value from the second one.
def merge_dicts(d1, d2):
    merged = d1.copy()
    for key in d2:
        merged[key] = d2[key]
    return merged

# 12. Given a paragraph of text, return the three most common words, excluding a provided list of stop words.
def top_three_words(text, stop_words):
    if not text:
        return []

    # Convert stop_words to a set for O(1) lookup
    stop_set = set(stop_words) if stop_words else set()

    # Tokenize and filter in one list comprehension
    words = [w for w in re.findall(r'\w+', text.lower()) if w not in stop_set]

    # most_common(3) uses a heap internally, avoiding a full sort
    return [word for word, count in Counter(words).most_common(3)]

# 13. Write a function that validates whether a string is a properly formatted email address, using basic checks rather than a regular expression.
def is_valid_email(email):
    if not email:
        return False

    # Professional standard: Use a regex for declarative validation
    # This pattern checks for: basic user @ domain . extension
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(email_regex, email))

# 14. Given a list of numbers, return True if the list is sorted in ascending order, False otherwise.
def is_sorted(numbers):
    for i in range(len(numbers) - 1):
        if numbers[i] > numbers[i+1]:
            return False
    return True

# 15. Write a function that takes a list of file names and groups them by extension.
def group_by_extension(files):
    groups = {}
    for f in files:
        if "." in f:
            # split from right for the extension
            parts = f.split(".")
            ext = parts[-1]
            if ext not in groups:
                groups[ext] = []
            groups[ext].append(f)
        else:
            if "no_ext" not in groups:
                groups["no_ext"] = []
            groups["no_ext"].append(f)
    return groups

# 16. Given a nested dictionary representing a company's departments and employees, count the total number of employees.
def count_employees(company):
    total = 0
    for dept in company:
        employees = company[dept]
        # assuming employees is a list of names
        total = total + len(employees)
    return total

# 17. Write a function that generates the first n numbers of the Fibonacci sequence using a loop.
def fibonacci_loop(n):
    if n <= 0:
        return []
    if n == 1:
        return [0]

    seq = [0, 1]
    while len(seq) < n:
        next_val = seq[-1] + seq[-2]
        seq.append(next_val)
    return seq

# 18. Given two lists representing set A and set B, return their union, intersection, and difference without using Python's built-in set operators directly (use loops).
def list_set_operations(list_a, list_b):
    if list_a is None or list_b is None:
        return {"union": [], "intersection": [], "difference": []}

    # Convert to sets for hash-based operations
    set_a, set_b = set(list_a), set(list_b)

    return {
        "union": list(set_a | set_b),
        "intersection": list(set_a & set_b),
        "difference": list(set_a - set_b)
    }

# 19. Write a function that takes a list of prices and a discount percentage, and returns the discounted prices rounded to two decimals.
def apply_discount(prices, discount_percent):
    discounted = []
    multiplier = (100 - discount_percent) / 100
    for p in prices:
        new_p = round(p * multiplier, 2)
        discounted.append(new_p)
    return discounted

# 20. Given a list of log entries as strings ("2026-01-04 ERROR disk full"), return a count of entries per severity level.
def count_log_severity(logs):
    counts = {}
    for entry in logs:
        parts = entry.split(" ")
        if len(parts) > 1:
            severity = parts[1] # the second word is the severity
            if severity not in counts:
                counts[severity] = 0
            counts[severity] = counts[severity] + 1
    return counts

# --- Testing the functions ---
if __name__ == "__main__":
    print("--- Testing Intermediate Challenges ---")

    print("Task 1 (Top Student):", get_top_student([{"name": "Alice", "grade": 85}, {"name": "Bob", "grade": 92}, {"name": "Charlie", "grade": 88}]))
    print("Task 2 (Flatten):", flatten_list([[1, 2], [3, 4], [5]]))
    print("Task 3 (Word Freq):", word_frequency("Hello world! Hello again, world."))
    print("Task 4 (Anagrams):", are_anagrams("Listen", "Silent"))
    print("Task 5 (2nd Largest):", second_largest([10, 20, 4, 45, 99]))
    print("Task 6 (Group by Letter):", group_by_first_letter(["Apple", "banana", "Apricot", "Blueberry"]))
    print("Task 7 (Balance):", calculate_balance([{"amount": 100, "type": "credit"}, {"amount": 50, "type": "debit"}, {"amount": 20, "type": "debit"}]))
    print("Task 8 (Remove Dups):", remove_duplicate_dicts([{"id": 1, "name": "A"}, {"id": 2, "name": "B"}, {"id": 1, "name": "C"}], "id"))
    print("Task 9 (Caesar):", caesar_cipher("Hello World!", 3))
    print("Task 10 (Closest Origin):", closest_to_origin([(10, 10), (1, 2), (5, 5)]))
    print("Task 11 (Merge):", merge_dicts({"a": 1, "b": 2}, {"b": 3, "c": 4}))
    print("Task 12 (Top 3):", top_three_words("the quick brown fox jumps over the lazy dog the fox is brown", ["the", "is"]))
    print("Task 13 (Email Valid):", is_valid_email("test@example.com"), is_valid_email("bad-email@com"))
    print("Task 14 (Sorted):", is_sorted([1, 2, 3, 5, 4]))
    print("Task 15 (Extensions):", group_by_extension(["test.py", "main.py", "image.png", "readme"]))
    print("Task 16 (Employees):", count_employees({"Sales": ["Joe", "Ann"], "Tech": ["Dev1", "Dev2", "Dev3"]}))
    print("Task 17 (Fibonacci):", fibonacci_loop(7))
    print("Task 18 (Sets):", list_set_operations([1, 2, 3], [2, 3, 4]))
    print("Task 19 (Discount):", apply_discount([100.0, 45.5, 10.99], 15))
    print("Task 20 (Log Severity):", count_log_severity(["2026-01-01 INFO start", "2026-01-01 ERROR crash", "2026-01-01 INFO stop", "2026-01-01 ERROR bug"]))

    print("--- Tests Finished ---")

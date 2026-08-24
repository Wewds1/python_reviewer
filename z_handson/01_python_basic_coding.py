# Coding Challenges - Module 1 (Beginner)
# Written by a Junior Engineer

# 1. Write a function that returns the square of a number.
def square_number(n):
    # multiply the number by itself to get the square
    result = n * n
    return result

# 2. Write a function that checks whether a number is positive, negative, or zero.
def check_number(n):
    if n > 0:
        return "positive"
    elif n < 0:
        return "negative"
    else:
        return "zero"

# 3. Write a function that returns the larger of two numbers without using max().
def find_larger(a, b):
    if a > b:
        return a
    else:
        return b

# 4. Print the numbers from 1 to 20, but print "buzz" instead of any multiple of 4.
def buzz_print():
    for i in range(1, 21):
        if i % 4 == 0:
            print("buzz")
        else:
            print(i)

# 5. Write a function that counts the vowels in a string.
def count_vowels(text):
    vowels = "aeiouAEIOU"
    count = 0
    for char in text:
        if char in vowels:
            count = count + 1
    return count

# 6. Reverse a list without using .reverse() or slicing.
def reverse_list(my_list):
    reversed_list = []
    # start from the end of the list and go backwards
    for i in range(len(my_list) - 1, -1, -1):
        reversed_list.append(my_list[i])
    return reversed_list

# 7. Write a function that returns the average of a list of numbers.
def calculate_average(numbers):
    if len(numbers) == 0:
        return 0
    total = 0
    for n in numbers:
        total = total + n
    return total / len(numbers)

# 8. Check whether a string is a palindrome, ignoring case.
def is_palindrome(text):
    # make it all lowercase first
    text = text.lower()
    # reverse the string manually
    reversed_text = ""
    for char in text:
        reversed_text = char + reversed_text

    if text == reversed_text:
        return True
    else:
        return False

# 9. Write a function that converts a temperature from Celsius to Fahrenheit.
def celsius_to_fahrenheit(celsius):
    # Formula is (C * 9/5) + 32
    fahrenheit = (celsius * 9/5) + 32
    return fahrenheit

# 10. Given a list of numbers, return a new list with only the even ones.
def get_even_numbers(numbers):
    evens = []
    for n in numbers:
        if n % 2 == 0:
            evens.append(n)
    return evens

# 11. Write a function that counts how many words are in a sentence.
def count_words(sentence):
    # split the sentence by spaces
    words = sentence.split()
    return len(words)

# 12. Given a dictionary of item names to prices, print each item with its price formatted as currency.
def print_prices(price_dict):
    for item in price_dict:
        price = price_dict[item]
        print("Item: " + item + " - Price: $" + str(price))

# 13. Write a function that returns the factorial of a number using a loop, not recursion.
def factorial_loop(n):
    result = 1
    for i in range(1, n + 1):
        result = result * i
    return result

# 14. Given a list of names, return the longest one.
def find_longest_name(names):
    if len(names) == 0:
        return None

    longest = names[0]
    for name in names:
        if len(name) > len(longest):
            longest = name
    return longest

# 15. Write a function that removes all whitespace from a string.
def remove_whitespace(text):
    result = ""
    for char in text:
        if char != " " and char != "\t" and char != "\n":
            result = result + char
    return result

# 16. Given two numbers, return their greatest common divisor using a loop.
def find_gcd(a, b):
    # we use the simpler loop method
    # find the smaller number
    if a < b:
        smaller = a
    else:
        smaller = b

    gcd = 1
    for i in range(1, smaller + 1):
        if (a % i == 0) and (b % i == 0):
            gcd = i
    return gcd

# 17. Write a function that capitalizes the first letter of every word in a sentence.
def capitalize_words(sentence):
    words = sentence.split()
    capitalized_list = []
    for word in words:
        # take first letter, make it upper, then add the rest of the word
        new_word = word[0].upper() + word[1:]
        capitalized_list.append(new_word)

    # join them back with spaces
    return " ".join(capitalized_list)

# 18. Given a list of numbers, return how many of them are negative.
def count_negatives(numbers):
    count = 0
    for n in numbers:
        if n < 0:
            count = count + 1
    return count

# 19. Write a simple calculator function that takes two numbers and an operator string ("+", "-", "*", "/") and returns the result.
def simple_calculator(num1, num2, operator):
    if operator == "+":
        return num1 + num2
    elif operator == "-":
        return num1 - num2
    elif operator == "*":
        return num1 * num2
    elif operator == "/":
        if num2 == 0:
            return "Error: Division by zero"
        return num1 / num2
    else:
        return "Invalid operator"

# 20. Given a string, count how many times each character appears and return the result as a dictionary.
def count_chars(text):
    char_counts = {}
    for char in text:
        if char in char_counts:
            char_counts[char] = char_counts[char] + 1
        else:
            char_counts[char] = 1
    return char_counts

# --- Testing the functions ---
if __name__ == "__main__":
    print("--- Testing Beginner Challenges ---")

    print("Task 1 (Square):", square_number(5))
    print("Task 2 (Check Number):", check_number(-10))
    print("Task 3 (Larger):", find_larger(10, 20))

    print("Task 4 (Buzz Print):")
    buzz_print()

    print("Task 5 (Vowels):", count_vowels("Hello World"))
    print("Task 6 (Reverse List):", reverse_list([1, 2, 3, 4, 5]))
    print("Task 7 (Average):", calculate_average([10, 20, 30]))
    print("Task 8 (Palindrome):", is_palindrome("Racecar"))
    print("Task 9 (Celsius to Fahr):", celsius_to_fahrenheit(25))
    print("Task 10 (Evens):", get_even_numbers([1, 2, 3, 4, 5, 6]))
    print("Task 11 (Word Count):", count_words("The quick brown fox"))

    print("Task 12 (Print Prices):")
    print_prices({"Apple": 0.5, "Banana": 0.3, "Orange": 0.7})

    print("Task 13 (Factorial):", factorial_loop(5))
    print("Task 14 (Longest Name):", find_longest_name(["Alice", "Bob", "Christopher", "Dan"]))
    print("Task 15 (Remove Space):", remove_whitespace(" Hello  World \t\n "))
    print("Task 16 (GCD):", find_gcd(48, 18))
    print("Task 17 (Capitalize):", capitalize_words("hello world from python"))
    print("Task 18 (Negatives):", count_negatives([1, -2, 3, -4, -5]))
    print("Task 19 (Calc):", simple_calculator(10, 5, "/"))
    print("Task 20 (Char Count):", count_chars("banana"))

    print("--- Tests Finished ---")

# Lesson 6: File Handling

## 1. Learning objectives

By the end of this lesson you should be able to:

- Open, read, write, and append to files without leaking file handles
- Explain why `with` is the correct way to open a file, not just the popular way
- Read and write CSV and JSON, the two formats you'll touch constantly in real work
- Handle file paths in a way that doesn't break the moment someone runs your script on a different operating system

## 2. Prerequisites

Lessons 1 through 5. You'll be using loops, dictionaries, and modules (`csv`, `json`, `pathlib`) together here.

## 3. Introduction

Sooner or later, a program needs to read something that isn't hardcoded, or save something that outlives the process. That's file handling. It's not conceptually hard, but it's full of small habits that separate someone who writes scripts that work on their machine from someone who writes scripts that work on everyone's machine, including the one running in a scheduled job at 2am with nobody watching if it fails halfway through.

## 4. Theory

Opening a file gives you a file object, a handle to the operating system's file descriptor, which you then read from or write to. The critical detail: that handle needs to be closed when you're done, or you risk leaving it open, which on some systems can lock the file, leak memory, or silently lose buffered writes that never got flushed to disk.

```python
file = open("notes.txt", "r")
content = file.read()
file.close()  # easy to forget, especially if an exception happens first
```

That pattern works, but it's fragile. If `file.read()` throws an exception, `file.close()` never runs. That's exactly the problem `with` solves.

## 5. Why this concept exists

Programs need to persist data past their own lifetime, and they need to read data they didn't generate themselves, client spreadsheets, config files, log output from another system. File I/O is the boundary between your program and the outside world, and because that boundary involves the operating system and physical disks, it's also where things are most likely to go wrong: a file might not exist, might be locked by another process, might have unexpected encoding. Python's file handling tools exist to make that boundary predictable.

## 6. How Python implements it internally

`open()` asks the operating system for a file descriptor and wraps it in a Python file object that buffers reads and writes for efficiency rather than hitting the disk on every single character. The `with` statement is syntactic sugar over a context manager protocol: it calls `__enter__` when the block starts and guarantees `__exit__` runs when the block ends, even if an exception was raised inside it. For files, `__exit__` closes the file. That guarantee, cleanup runs no matter what, is the entire reason `with open(...) as f:` is the standard idiom instead of manual `open()`/`close()` pairs.

## 7. Real-world analogy

Opening a file without `with` is like borrowing a library book and being responsible for remembering to return it yourself, every single time, including the times you got distracted by something else entirely. `with` is having the library check it back in automatically the moment you walk out the door, whether you finished reading or got called away halfway through. You genuinely cannot forget, because it's not on you to remember.

## 8. Enterprise use cases

Reading a client's data extract (usually CSV or Excel), validating it, and writing a cleaned version back out is one of the most common tasks in consulting-style Python work. Config files in JSON or YAML control application behavior without needing a code change. Log files get written continuously by long-running services and read back for debugging or audits. Every one of these depends on file handling that doesn't silently corrupt data or leave a file half-written if something goes wrong midway.

## 9. Syntax

**Opening, reading, writing, appending:**

```python
with open("notes.txt", "r") as f:
    content = f.read()

with open("notes.txt", "w") as f:
    f.write("This overwrites the entire file.\n")

with open("notes.txt", "a") as f:
    f.write("This gets added to the end.\n")

with open("notes.txt", "r") as f:
    for line in f:            # iterating a file reads it line by line
        print(line.strip())   # .strip() removes the trailing newline
```

Mode characters: `"r"` read (default, errors if the file doesn't exist), `"w"` write (creates the file if missing, overwrites if it exists), `"a"` append (creates if missing, adds to the end if it exists), `"x"` exclusive creation (errors if the file already exists, useful when you specifically don't want to overwrite anything).

**CSV:**

```python
import csv

with open("employees.csv", "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["name"], row["department"])

with open("output.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "department"])
    writer.writeheader()
    writer.writerow({"name": "Alex", "department": "Engineering"})
```

`DictReader` and `DictWriter` are worth defaulting to over the plain `reader`/`writer` versions; working with dictionaries by column name is far less error-prone than tracking numeric column positions.

**JSON:**

```python
import json

with open("config.json", "r") as f:
    config = json.load(f)  # parses JSON directly into a Python dict

with open("output.json", "w") as f:
    json.dump({"status": "complete", "count": 42}, f, indent=2)
```

**Paths, the portable way:**

```python
from pathlib import Path

data_dir = Path("data")
file_path = data_dir / "employees.csv"  # works correctly on Windows, macOS, and Linux

if file_path.exists():
    with open(file_path, "r") as f:
        content = f.read()
```

## 10. Step-by-step examples

**Easy — reading a text file line by line:**

```python
with open("todo.txt", "r") as f:
    for line in f:
        print(line.strip())
```

**Medium — reading a CSV and filtering rows:**

```python
import csv

with open("employees.csv", "r") as f:
    reader = csv.DictReader(f)
    engineers = [row for row in reader if row["department"] == "Engineering"]

print(len(engineers))
```

**Hard — reading a JSON config, modifying it, and writing it back safely:**

```python
import json
from pathlib import Path

config_path = Path("config.json")

with open(config_path, "r") as f:
    config = json.load(f)

config["retry_count"] = config.get("retry_count", 3) + 1

temp_path = config_path.with_suffix(".json.tmp")
with open(temp_path, "w") as f:
    json.dump(config, f, indent=2)

temp_path.replace(config_path)  # atomic on most systems, avoids a half-written config file
```

Writing to a temp file and then replacing the original is a genuinely useful pattern once you're dealing with files other processes might be reading concurrently. It avoids the window where the real config file exists but is only half-written.

## 11. Common mistakes

**Opening a file without `with` and forgetting to close it,** which can leave file handles open and, in write mode, lose data that was buffered but never flushed to disk.

**Using `"w"` mode when you meant `"a"`,** and silently wiping out an existing file's contents. This one has cost people entire log files.

**Hardcoding path separators,** like `"data\\employees.csv"` or `"data/employees.csv"`, which breaks the moment the script runs on a different operating system. Use `pathlib.Path` and the `/` operator instead, which handles the correct separator for you.

**Forgetting `newline=""` when writing CSV files on Windows,** which results in an extra blank line between every row because of how Windows handles line endings.

## 12. Debugging tips

`FileNotFoundError` almost always means either a typo in the path, or the script is being run from a different working directory than you assumed. Print `Path.cwd()` to check where Python actually thinks it's running from. If a file appears empty or truncated after writing, check whether you're closing it properly, or better, whether you're using `with` at all.

## 13. Best practices

Always use `with` for file operations, no exceptions. Use `pathlib.Path` instead of raw strings for file paths. Use `csv.DictReader`/`DictWriter` and `json.load`/`json.dump` instead of manually parsing text, they handle edge cases (quoted commas in CSV, nested structures in JSON) that a hand-rolled parser will get wrong eventually. When writing files that other processes might read, consider the write-to-temp-then-replace pattern to avoid partial writes being visible.

## 14. Performance considerations

Reading a file line by line with a `for` loop is memory-efficient for large files, since it only holds one line in memory at a time, versus `.read()` or `.readlines()`, which load the entire file at once. For genuinely large files (gigabytes), line-by-line iteration or chunked reading is the difference between a script that runs fine and one that runs out of memory.

## 15. Code style (PEP 8)

Always specify an explicit mode (`"r"`, `"w"`, etc.) rather than relying on the default. Use `pathlib.Path` objects rather than string concatenation for paths. Keep file operations wrapped in `with` blocks, and keep the block itself focused, read or write, then get out, rather than doing unrelated work while a file handle is open.

## 16. Interview questions with model answers

**Q: Why should you use `with open(...)` instead of `open()` and `close()`?**

`with` guarantees the file gets closed even if an exception is raised while working with it, because it relies on the context manager protocol rather than a manual, easy-to-forget cleanup step. Manually calling `close()` works in the happy path, but any error before that line means the file never closes.

**Q: What's the difference between `"w"` and `"a"` mode?**

`"w"` truncates the file first, if it exists, before writing, meaning any existing content is lost. `"a"` opens the file for writing but adds new content to the end, preserving what's already there. Mixing these up is a classic way to accidentally destroy a file's existing contents.

**Q: How would you safely process a very large CSV file that doesn't fit comfortably in memory?**

The ideal answer mentions iterating over the file (or `csv.reader`/`DictReader`, which are already iterators) row by row instead of loading the whole thing with `.readlines()` or into a list up front, processing and, if needed, writing output incrementally rather than holding everything in memory at once.

## 17. Knowledge check

1. What happens if you open a file in `"w"` mode and the file already has content in it?
2. Why does `with open(...) as f:` close the file even if an exception occurs inside the block?
3. What's wrong with hardcoding `"data\\file.csv"` as a path?
4. Why prefer `csv.DictReader` over manually splitting each line on commas?

## 18. Hands-on exercises

**Easy**

1. Write a script that creates a text file, writes three lines to it, and then reads and prints them back.
2. Write a script that appends a timestamped line to a log file each time it runs.
3. Use `pathlib.Path` to check whether a file exists before trying to open it.

**Medium**

4. Given a CSV of products (name, price, quantity), read it with `csv.DictReader` and print the total inventory value (price times quantity, summed across all rows).
5. Write a Python dictionary to a JSON file, then read it back and confirm the round trip preserved the data correctly.
6. Write a script that reads a config JSON file, increments a counter field, and writes it back, using the temp-file-and-replace pattern from this lesson.

**Hard**

7. Given a CSV of transactions, write a script that splits it into two separate output CSV files, one for transactions over $100 and one for the rest, without loading the entire input into memory at once.
8. Write a script that merges two JSON files representing partial user records (matched by a shared `id` field) into one combined JSON file, handling the case where a given `id` only appears in one of the two files.

## 19. Stretch challenge

Write a small log-processing script that reads a text log file where each line has a timestamp and a severity level (`INFO`, `WARNING`, `ERROR`), and produces a JSON summary counting how many lines fall into each severity level, plus a separate CSV containing only the `ERROR` lines with their timestamps. Do it using line-by-line iteration so the script would still work if the log file were several gigabytes.

## 20. Summary

File handling is where your program stops being a closed box and starts talking to the outside world, which means it's also where things are most likely to fail in ways you didn't anticipate: missing files, wrong encodings, half-written output. `with` isn't a stylistic preference, it's the difference between code that cleans up after itself and code that occasionally doesn't. `pathlib` and the `csv`/`json` modules handle the genuinely annoying edge cases so you don't have to rediscover them the hard way.

## 21. Additional resources

- [Python official docs: Reading and Writing Files](https://docs.python.org/3/tutorial/inputoutput.html#reading-and-writing-files)
- [Python official docs: pathlib — Object-oriented filesystem paths](https://docs.python.org/3/library/pathlib.html)
- [Python official docs: csv — CSV File Reading and Writing](https://docs.python.org/3/library/csv.html)

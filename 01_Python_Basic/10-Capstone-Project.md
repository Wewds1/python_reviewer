# Capstone Project — Client Records Manager

## What you're building

A command-line application that manages client records for a small consulting practice: adding, editing, searching, and reporting on client data, with everything persisted to disk as CSV and JSON, and every operation protected by real error handling. It's small enough to finish, but it deliberately uses every major concept from this module: variables and data types, control flow, functions, modules and packages, file handling, and exception handling, organized as a proper multi-file Python package instead of one long script.

This is the project a hiring manager actually wants to see on your GitHub, not because it's flashy, but because it's the same shape as the small internal tools that get built constantly in real consulting and backend work.

I'm not handing you finished code. You're going to build this in five milestones, and I'll review what you've built after each one before you move to the next. That's not busywork, it's how real projects get built: in reviewable chunks, not as one 800-line commit nobody can meaningfully review.

## Architecture

```
┌─────────────────────┐
│      main.py         │  entry point, menu loop
└──────────┬───────────┘
           │
┌──────────▼───────────┐
│   client_manager/     │  the package
│                       │
│  ├── __init__.py      │  exposes the public interface
│  ├── models.py        │  the Client data shape + validation
│  ├── storage.py        │  reading/writing CSV and JSON
│  ├── operations.py     │  add, edit, search, delete, report
│  ├── exceptions.py     │  custom exception classes
│  └── cli.py             │  menu display + input handling
│
└──────────┬───────────┘
           │
┌──────────▼───────────┐
│      data/            │  clients.csv, backups/
└───────────────────────┘
```

The point of this structure: `main.py` should stay tiny, just wiring things together. Every layer below it has one clear job. `models.py` doesn't know anything about files. `storage.py` doesn't know anything about the menu. That separation is what makes a codebase like this survive contact with a second developer, or with you six months from now having forgotten most of the details.

## Folder structure

```
client-records-manager/
├── main.py
├── requirements.txt
├── README.md
├── data/
│   └── clients.csv
├── client_manager/
│   ├── __init__.py
│   ├── models.py
│   ├── storage.py
│   ├── operations.py
│   ├── exceptions.py
│   └── cli.py
└── tests/
    └── manual_test_checklist.md
```

## Feature list

- Add a new client record (name, email, company, status: active/inactive)
- List all clients, formatted as a readable table in the terminal
- Search clients by name or company (case-insensitive, partial match)
- Edit an existing client's details
- Delete a client, with a confirmation prompt
- Save all data to a CSV file, loaded automatically on startup
- Export a summary report to JSON: total clients, count by status, clients added in the last N days
- Handle every predictable failure gracefully: missing data file on first run, malformed rows in the CSV, invalid menu input, duplicate email on add

## Milestone 1: project skeleton and the Client model

Set up the folder structure above. In `models.py`, define what a client record looks like and how you'll validate one. You don't need a full class hierarchy, a dictionary-based structure with a validation function is fine for this module; if you want to reach slightly ahead and use a `dataclass`, that's a reasonable stretch, but it's not required.

In `exceptions.py`, define at least `DuplicateClientError` and `ClientNotFoundError`, both inheriting from a shared base `ClientManagerError`.

Deliverable: a `models.py` with a `validate_client(data)` function that raises a clear, specific exception for each thing that can be wrong with a client record (missing name, invalid email format, invalid status value), and a small script that proves it works against a few good and bad example records.

Bring this back before touching storage.

## Milestone 2: storage layer

Build `storage.py`. It needs functions to load all clients from `data/clients.csv` into a list of dictionaries on startup, and to save the current list back out. Handle the case where the file doesn't exist yet (first run) by starting with an empty list rather than crashing. Handle the case where a row in the CSV is malformed by skipping it, logging what was skipped and why, rather than letting one bad row take down the whole load.

This is the layer where Lesson 6 and Lesson 7 do the real work. Every file operation should be wrapped in `with`, and every predictable failure mode (missing file, malformed row, permission error) needs its own specific handling, not one broad catch-all.

Deliverable: `load_clients()` and `save_clients(clients)`, tested against a CSV with at least one deliberately broken row.

## Milestone 3: core operations

Build `operations.py`: `add_client`, `search_clients`, `edit_client`, `delete_client`. Each of these works against the in-memory list of clients (loaded once at startup, saved after any change) and raises the custom exceptions from Milestone 1 where appropriate, `DuplicateClientError` if you try to add a client with an email that's already in use, `ClientNotFoundError` if you try to edit or delete an id that doesn't exist.

This is also where the report generation goes: a function that takes the client list and returns a summary dictionary, ready to be written out as JSON by the storage layer.

Deliverable: each operation function, plus a short script exercising all of them against a small in-memory list, no CLI yet.

## Milestone 4: the CLI

Build `cli.py` and wire everything together in `main.py`. This is a menu loop: display options, read input, call the right operation function, handle whatever exception it might raise by printing something useful to the user instead of a raw traceback, and loop back to the menu. This is where Lesson 3's control flow and Lesson 4's function design come together with everything built so far.

Deliverable: a working end-to-end application. You should be able to run `python main.py`, add a few clients, search for one, edit it, delete another, and see the CSV file on disk reflect all of it correctly after you exit.

## Milestone 5: polish and the report export

Add the JSON report export feature, and go back through every operation checking for edge cases you might have missed: what happens if someone searches with an empty string, what happens if the CSV file exists but is completely empty, what happens if two clients somehow end up with the same id. Fix what you find.

Deliverable: the finished application, plus a short written note (a paragraph or two in the README) on what you'd do differently if you were building this for a real team, not a bootcamp exercise.

## Suggested git commits

Commit at the end of each milestone, not once at the very end. A reasonable history looks like:

```
1. project skeleton, empty package structure
2. Client model and validation
3. custom exception classes
4. storage layer: load and save CSV
5. storage layer: handle malformed rows and missing file
6. core operations: add, search
7. core operations: edit, delete
8. report generation
9. CLI menu loop
10. wire CLI to operations, end-to-end working app
11. JSON export
12. edge case fixes and README
```

Small, focused commits with clear messages are worth practicing now. "fixed stuff" as a commit message tells a reviewer nothing; "handle malformed CSV rows without crashing the whole load" tells them exactly what changed and why.

## Manual testing checklist

Before you consider a milestone done, walk through this by hand:

- Does the app start cleanly on a completely empty `data/` folder?
- Does adding a client with a duplicate email get rejected with a clear message, not a crash?
- Does editing or deleting a nonexistent client id get handled gracefully?
- Does the app survive a CSV file with one deliberately corrupted row, skipping just that row?
- Does searching with mixed case and partial text still find the right clients?
- Does the app save correctly if you exit normally, and does it not lose data if you interrupt it mid-operation?

## Ideas for future enhancement

Once this module's concepts feel solid, natural next steps (not required for this capstone, but worth thinking about) include swapping the CSV storage for a real SQLite database, adding a proper logging setup instead of print statements, writing actual automated tests with `pytest` instead of the manual checklist above, and adding a simple web interface on top of the same `operations.py` layer, which is exactly why keeping that layer independent of the CLI mattered from the start.

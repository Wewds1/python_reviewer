# Filtering and Sorting Data

In the previous lesson we learned how to retrieve data using the `SELECT` statement. Asking a database to return all rows from a table is rarely useful in a production application.

If you are building an API endpoint like `GET /users?status=active`, you need to ask the database specific questions and ensure the answers come back in a predictable order. This is where `WHERE` and `ORDER BY` come in.

## The WHERE clause

The `WHERE` clause filters records, returning only rows that fulfill a specified mathematical or logical condition. The database evaluates the condition for every row (or uses an index to skip rows). If the condition evaluates to TRUE, the row is included.

### Basic comparison operators

SQL supports standard comparisons:

- `=` (equal)
- `!=` or `<>` (not equal)
- `>` (greater than), `<` (less than)
- `>=` (greater than or equal), `<=` (less than or equal)

Example: Find a user by email

```sql
-- Find a specific user by their unique email
SELECT user_id, first_name, last_name
FROM users
WHERE email = 'ceo@example.com';
```

Example: Find users with many failed logins

```sql
SELECT email, login_attempts
FROM users
WHERE login_attempts > 3;
```

## Logical operators (AND, OR, NOT)

Combine multiple conditions using logical operators.

### AND

Returns rows where all conditions are TRUE.

```sql
SELECT order_id, total_amount
FROM orders
WHERE status = 'pending' AND total_amount > 1000.00;
```

### OR

Returns rows where any condition is TRUE.

```sql
SELECT first_name, last_name, department
FROM employees
WHERE department = 'Engineering' OR department = 'Product';
```

### Grouping with parentheses (crucial)

`AND` is evaluated before `OR`. Use parentheses to make intent explicit.

```sql
-- BUG: This might return all HR employees regardless of salary!
SELECT *
FROM employees
WHERE department = 'Engineering' OR department = 'HR' AND salary > 100000;

-- CORRECT: Clearly defines the logic
SELECT *
FROM employees
WHERE (department = 'Engineering' OR department = 'HR')
  AND salary > 100000;
```

## Advanced filtering

### IN

Use `IN` instead of multiple `OR` conditions.

```sql
SELECT first_name, last_name
FROM users
WHERE country IN ('USA', 'Canada', 'UK', 'Australia');
```

### BETWEEN

Filters values within an inclusive range (works for numbers, text, and dates).

```sql
SELECT order_id, order_date
FROM orders
WHERE order_date BETWEEN '2023-01-01' AND '2023-12-31';
```

### Pattern matching with LIKE

`LIKE` searches for patterns using two wildcards:

- `%` — zero, one, or multiple characters
- `_` — a single character

```sql
-- Find all users whose email ends with '@google.com'
SELECT email
FROM users
WHERE email LIKE '%@google.com';

-- Find all users whose first name starts with 'A'
SELECT first_name
FROM users
WHERE first_name LIKE 'A%';
```

(Note: In PostgreSQL, `LIKE` is case-sensitive. Use `ILIKE` for case-insensitive searches.)

Enterprise warning — leading wildcard anti-pattern

Using a leading wildcard (e.g., `LIKE '%john%'`) prevents use of standard B-Tree indexes and forces a full table scan. For robust text search use full-text search features (Postgres `tsvector`) or search engines like Elasticsearch.

## The NULL problem

`NULL` means "unknown" or "missing", not zero or empty string. Because it's unknown, you cannot compare it using `=` or `!=`.

```sql
-- WRONG: This is an anti-pattern and returns no rows
SELECT * FROM users WHERE phone_number = NULL;
```

Use `IS NULL` or `IS NOT NULL` instead:

```sql
-- Find users who haven't provided a phone number
SELECT first_name, email
FROM users
WHERE phone_number IS NULL;

-- Find users who HAVE provided a phone number
SELECT first_name, email
FROM users
WHERE phone_number IS NOT NULL;
```

## Sorting with ORDER BY

Databases return rows in an arbitrary order unless you request a specific ordering. `ORDER BY` sorts the result set.

### Ascending and descending

- `ASC` (ascending) — default (A-Z, 0-9, oldest→newest)
- `DESC` (descending) — (Z-A, 9-0, newest→oldest)

```sql
-- Get the 10 most recently created users
SELECT user_id, email, created_at
FROM users
ORDER BY created_at DESC
LIMIT 10;
```

### Sorting by multiple columns

The database sorts by the first column, then uses subsequent columns to break ties.

```sql
SELECT last_name, first_name, email
FROM users
ORDER BY last_name ASC, first_name ASC;
```

## Execution order (how the database thinks)

SQL is written in a readable order, but the engine executes clauses in a specific sequence. For queries with `SELECT`, `FROM`, `WHERE`, `ORDER BY`, and `LIMIT` the typical execution order is:

1. `FROM` — locate the table(s)
2. `WHERE` — filter rows
3. `SELECT` — pick the requested columns
4. `ORDER BY` — sort the filtered data
5. `LIMIT` / `OFFSET` — slice the pagination window

## Up next

You can now retrieve, filter, and sort rows. To learn how to summarize data (totals, averages, counts) proceed to the next lesson on aggregation using `GROUP BY` and aggregate functions.
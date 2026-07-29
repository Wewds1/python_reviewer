# 03. SQL Basics (Data Manipulation Language)

In the previous lesson, you designed a relational schema. Now it is time to interact with data.

Structured Query Language (SQL) is the standard language for working with Relational Database Management Systems (RDBMS). While SQL also includes DDL and DCL, most day-to-day backend work centers on **Data Manipulation Language (DML)**.

DML is commonly described with CRUD:

- Create -> `INSERT`
- Read -> `SELECT`
- Update -> `UPDATE`
- Delete -> `DELETE`

This lesson covers syntax, practical usage, and enterprise safety practices for these commands.

---

## 1. Setup: Target Schema

Assume the following PostgreSQL table exists.

```sql
-- Reference schema (DDL)
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    login_attempts INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 2. INSERT (Create)

`INSERT` adds new rows to a table.

### Standard syntax

Always list explicit columns in production SQL.

```sql
INSERT INTO users (first_name, last_name, email)
VALUES ('Jane', 'Doe', 'jane.doe@example.com');
```

Key behaviors:

- String literals use single quotes.
- Omitted columns use defaults or auto-generated values.
  - `user_id` auto-generates via `SERIAL`
  - `login_attempts` defaults to `0`
  - `created_at` defaults to `CURRENT_TIMESTAMP`

### Bulk insert

Insert many rows in one round trip for better performance.

```sql
INSERT INTO users (first_name, last_name, email)
VALUES
    ('John', 'Smith', 'john@example.com'),
    ('Alice', 'Johnson', 'alice@example.com'),
    ('Bob', 'Williams', 'bob@example.com');
```

### PostgreSQL `RETURNING`

Return generated values immediately after insert.

```sql
INSERT INTO users (first_name, last_name, email)
VALUES ('Charlie', 'Brown', 'charlie@example.com')
RETURNING user_id, created_at;
```

### Handling duplicates (Upsert)

Use `ON CONFLICT` to insert-or-update.

```sql
INSERT INTO users (first_name, last_name, email, login_attempts)
VALUES ('Jane', 'Doe', 'jane.doe@example.com', 1)
ON CONFLICT (email)
DO UPDATE SET login_attempts = users.login_attempts + 1;
```

---

## 3. SELECT (Read)

`SELECT` retrieves data from one or more tables.

### Select specific columns

```sql
SELECT first_name, email
FROM users;
```

Best practice: request only needed columns to reduce network and memory cost.

### `SELECT *` (anti-pattern in production)

```sql
SELECT *
FROM users;
```

`SELECT *` is fine for quick manual inspection, but risky in production APIs. Schema changes can silently increase payload size and latency.

### Aliasing with `AS`

Use aliases to shape output for API contracts.

```sql
SELECT
    first_name AS "firstName",
    last_name AS "lastName"
FROM users;
```

### Unique values with `DISTINCT`

```sql
SELECT DISTINCT first_name
FROM users;
```

### Pagination basics: `LIMIT` and `OFFSET`

```sql
-- Page 2 when page size is 10 (rows 11-20)
SELECT user_id, first_name, email
FROM users
LIMIT 10 OFFSET 10;
```

---

## 4. UPDATE (Update)

`UPDATE` modifies existing rows.

### Standard syntax

```sql
UPDATE users
SET
    first_name = 'Jonathan',
    last_name = 'Smythe'
WHERE email = 'john@example.com';
```

### Using expressions

```sql
-- Increment login attempts
UPDATE users
SET login_attempts = login_attempts + 1
WHERE user_id = 1001;
```

### Most dangerous SQL mistake

Running `UPDATE` without `WHERE` updates every row.

```sql
-- DANGER: updates all rows
UPDATE users
SET first_name = 'Hacked';
```

Always verify the `WHERE` clause before executing updates.

---

## 5. DELETE (Delete)

`DELETE` removes rows.

### Standard syntax

```sql
DELETE FROM users
WHERE user_id = 1002;
```

### Soft delete vs hard delete

In enterprise systems, hard deletes are often avoided for critical entities. Instead, add a status column and mark records inactive.

```sql
-- Soft delete pattern
UPDATE users
SET is_active = FALSE
WHERE user_id = 1002;
```

### `DELETE` vs `TRUNCATE`

If you need to clear an entire table, `TRUNCATE` is typically faster and more efficient than deleting row by row.

```sql
TRUNCATE TABLE users;
```

---

## 6. Enterprise Safety Checklist

Before executing write queries:

- Confirm `WHERE` clause scope
- Prefer explicit column lists in `INSERT`
- Avoid `SELECT *` in production code
- Use transactions for multi-step business operations
- Use parameterized queries in Python to prevent SQL injection

---

## Up Next

You now know basic DML syntax for creating, reading, updating, and deleting data.

Next, proceed to `04-Filtering-and-Sorting.md` to master:

- Advanced `WHERE` conditions
- Logical operators
- `NULL` handling
- Result sorting strategies

# Aggregation and Grouping

So far we have learned how to retrieve, filter, and sort individual rows. As an engineer you will often be asked to build analytical endpoints, reporting dashboards, or financial summaries. For those features you don't want millions of individual rows — you want summarized answers, for example:

- "What is our total revenue for the month?"
- "How many active users do we have per country?"
- "What is the average salary in the Engineering department?"

To answer these questions, use aggregate functions and the `GROUP BY` clause.

## 1. Aggregate functions

Aggregate functions take a collection of values (multiple rows) and return a single summarized value.

Core functions:

- `COUNT()` — counts rows
- `SUM()` — adds values in a numeric column
- `AVG()` — calculates the average of a numeric column
- `MAX()` — finds the highest value (numbers, dates, strings)
- `MIN()` — finds the lowest value (numbers, dates, strings)

Examples without grouping

```sql
-- Count total registered users
SELECT COUNT(user_id) AS total_users
FROM users;

-- Total amount of all successful orders
SELECT SUM(total_amount) AS lifetime_revenue
FROM orders
WHERE status = 'successful';

-- Date of the very first order
SELECT MIN(created_at) AS first_order_date
FROM orders;
```

### COUNT(*) vs COUNT(column)

`COUNT(*)` counts every row. `COUNT(column_name)` counts only rows where `column_name` is NOT NULL.

```sql
-- Counts ALL users
SELECT COUNT(*) FROM users;

-- Counts ONLY users who provided a phone number
SELECT COUNT(phone_number) FROM users;
```

(Note: `SUM`, `AVG`, `MIN`, and `MAX` ignore `NULL` values automatically.)

## 2. The GROUP BY clause

`GROUP BY` creates summary rows (buckets) for rows that share the same values in the specified column(s).

```sql
-- Count users grouped by country
SELECT country, COUNT(user_id) AS user_count
FROM users
GROUP BY country;
```

You can group by multiple columns — each unique combination becomes its own bucket:

```sql
-- Total revenue per department, broken down by year
SELECT department, EXTRACT(YEAR FROM order_date) AS order_year, SUM(total_amount)
FROM orders
GROUP BY department, EXTRACT(YEAR FROM order_date);
```

### The golden rule of GROUP BY

If you use `GROUP BY`, every column in `SELECT` must either be inside an aggregate function or listed in the `GROUP BY` clause. Otherwise the database does not know how to reduce multiple rows into a single summary value.

```sql
-- WRONG: Will throw an error
SELECT department, country, COUNT(*)
FROM users
GROUP BY country;

-- CORRECT: Both non-aggregated columns are in the GROUP BY
SELECT department, country, COUNT(*)
FROM users
GROUP BY department, country;
```

## 3. The HAVING clause (filtering groups)

`WHERE` filters rows before aggregation. To filter after aggregation (based on aggregate results), use `HAVING`.

```sql
-- WRONG: can't use aggregate in WHERE
SELECT country, COUNT(*)
FROM users
WHERE COUNT(*) > 10000
GROUP BY country;

-- CORRECT: HAVING filters grouped results
SELECT country, COUNT(*) AS user_count
FROM users
GROUP BY country
HAVING COUNT(*) > 10000;
```

Combining `WHERE` and `HAVING` is common: use `WHERE` to reduce raw data for performance, then `GROUP BY`, then `HAVING` to filter buckets.

```sql
-- Find departments with more than 5 active employees
SELECT department, COUNT(employee_id) AS active_count
FROM employees
WHERE status = 'active'          -- 1. Filter raw rows first
GROUP BY department              -- 2. Bucket the remaining rows
HAVING COUNT(employee_id) > 5;   -- 3. Filter buckets
```

## 4. Execution order (updated mental model)

With grouping, the execution order is:

1. `FROM` — locate the tables
2. `WHERE` — filter individual rows
3. `GROUP BY` — form buckets
4. `HAVING` — filter buckets
5. `SELECT` — compute aggregates and pick columns
6. `ORDER BY` — sort final results
7. `LIMIT` / `OFFSET` — paginate

This explains why aliases from `SELECT` aren't available in `WHERE` or `HAVING` — those clauses run earlier.

```sql
-- WRONG: alias doesn't exist yet in HAVING
SELECT department, COUNT(employee_id) AS active_count
FROM employees
GROUP BY department
HAVING active_count > 5;
```

## Up next

You can now retrieve, filter, sort, and summarize data from single tables. To build real applications you must combine data from multiple tables — proceed to the next lesson on `JOIN`s.

Proceed to [06-JOINs.md](06-JOINs.md).
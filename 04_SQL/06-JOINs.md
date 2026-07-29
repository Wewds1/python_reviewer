
SELECT 
# Connecting tables with JOINs

Relational databases minimize redundancy by storing related data in separate tables and linking them with foreign keys. When an API client requests a single resource (for example `GET /orders/123`) you usually need to return a combined result (order details plus user email). To reassemble normalized data into one result set, use JOINs.

## 1. Setup: target schema

Example tables:

Table A: `users`

- `user_id` (PK)
- `first_name`

| user_id | first_name |
|--------:|------------|
| 1       | Alice      |
| 2       | Bob        |
| 3       | Charlie    |

Table B: `orders`

- `order_id` (PK)
- `user_id` (FK)
- `total`

| order_id | user_id | total   |
|--------:|--------:|--------:|
| 101     | 1       | $50.00  |
| 102     | 1       | $20.00  |
| 103     | 2       | $100.00 |
| 104     | 99      | $10.00  |

Note: Charlie (user 3) has no orders. Order 104 references a missing user (99).

## 2. INNER JOIN (the default)

`INNER JOIN` returns rows that have matches in both tables — the intersection.

```sql
SELECT
    users.user_id,
    users.first_name,
    orders.order_id,
    orders.total
FROM users
INNER JOIN orders
    ON users.user_id = orders.user_id;
```

Result:

| user_id | first_name | order_id | total   |
|--------:|------------|---------:|--------:|
| 1       | Alice      | 101      | $50.00 |
| 1       | Alice      | 102      | $20.00 |
| 2       | Bob        | 103      | $100.00 |

Alice appears twice (two orders). Charlie is excluded (no orders). Order 104 is excluded (no matching user).

## 3. LEFT JOIN (left outer join)

`LEFT JOIN` returns all rows from the left table plus matched rows from the right table. Missing matches are filled with `NULL`.

```sql
SELECT
    users.user_id,
    users.first_name,
    orders.order_id
FROM users
LEFT JOIN orders
    ON users.user_id = orders.user_id;
```

Result:

| user_id | first_name | order_id |
|--------:|------------|---------:|
| 1       | Alice      | 101      |
| 1       | Alice      | 102      |
| 2       | Bob        | 103      |
| 3       | Charlie    | NULL     |

Use case: find users who never placed an order

```sql
SELECT u.first_name
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE o.order_id IS NULL;
```

## 4. RIGHT JOIN and FULL OUTER JOIN

### RIGHT JOIN

`RIGHT JOIN` is the mirror of `LEFT JOIN`: it returns all rows from the right table and matched rows from the left. In practice, developers prefer swapping table order and using `LEFT JOIN` for readability.

### FULL OUTER JOIN

`FULL OUTER JOIN` returns all rows from both tables; missing sides are filled with `NULL`.

```sql
SELECT u.first_name, o.order_id
FROM users u
FULL OUTER JOIN orders o
    ON u.user_id = o.user_id;
```

This would include users without orders and orders without users.

## 5. CROSS JOIN (cartesian product)

`CROSS JOIN` pairs every row from the first table with every row from the second table. It does not use an `ON` clause.

```sql
SELECT u.first_name, p.product_name
FROM users u
CROSS JOIN products p;
```

Warning: accidental cartesian products can be catastrophic — only use intentionally.

## 6. SELF JOIN

A self join joins a table to itself. Use aliases to distinguish the two roles (for example employee vs manager).

```sql
-- Table: employees (employee_id, name, manager_id)
SELECT
    emp.name AS "Employee Name",
    mgr.name AS "Manager Name"
FROM employees emp
LEFT JOIN employees mgr
    ON emp.manager_id = mgr.employee_id;
```

## 7. Table aliasing (best practice)

Aliases keep queries readable when joining many tables.

```sql
SELECT
    u.first_name,
    u.email,
    o.order_date,
    o.total
FROM users u
INNER JOIN orders o ON u.user_id = o.user_id
INNER JOIN order_items oi ON o.order_id = oi.order_id
INNER JOIN products p ON oi.product_id = p.product_id
WHERE u.status = 'active';
```

## 8. ON vs WHERE (crucial distinction)

With `INNER JOIN`, filtering in `ON` vs `WHERE` often yields the same result. With `LEFT JOIN`, they behave differently:

- `ON` filters the right table before joining; left rows still survive with `NULL`s for unmatched columns.
- `WHERE` filters the result set after the join, potentially turning a `LEFT JOIN` into an implicit `INNER JOIN`.

```sql
-- Keeps all users, but only attaches orders > $100 (others get NULLs)
SELECT u.first_name, o.total
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id AND o.total > 100;

-- Keeps ONLY users who have an order > $100 (LEFT JOIN effectively becomes INNER JOIN)
SELECT u.first_name, o.total
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE o.total > 100;
```

## Up next

You can now query data, summarize it, and reconstruct relationships spread across multiple tables. To learn how to design tables and relationships, proceed to the next lesson on DDL and relationships.

Proceed to [07-Database-Relationships.md](07-Database-Relationships.md).
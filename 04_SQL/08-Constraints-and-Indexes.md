## Constraints and indexes

An enterprise database must not only store data but protect it and serve it fast. Use Constraints to enforce correctness, and Indexes to make reads fast at scale.

### Part 1 — Constraints (protecting your data)

The database is the final source of truth. Never rely exclusively on application code for validation. Constraints are rules enforced by the engine; violating a constraint aborts the transaction and returns an error.

Common constraint types:

- `NOT NULL` — column cannot be `NULL`
- `UNIQUE` — values must be unique (single or composite)
- `PRIMARY KEY` — `NOT NULL` + `UNIQUE`; identifies a row
- `FOREIGN KEY` — enforces referential integrity
- `CHECK` — arbitrary boolean expression (business rules)
- `DEFAULT` — default value when none supplied

Example: a products table with named constraints and checks

```sql
CREATE TABLE products (
    product_id   SERIAL PRIMARY KEY,
    sku          VARCHAR(50) NOT NULL,
    name         VARCHAR(255) NOT NULL,
    description  TEXT DEFAULT 'No description provided',
    is_active    BOOLEAN DEFAULT TRUE,
    price        DECIMAL(10,2) NOT NULL,
    discount_mul DECIMAL(3,2) DEFAULT 1.00,
    CONSTRAINT uq_product_sku   UNIQUE (sku),
    CONSTRAINT chk_price_positive CHECK (price >= 0),
    CONSTRAINT chk_discount_range CHECK (discount_mul >= 0.00 AND discount_mul <= 1.00)
);
```

Other useful constraint examples:

```sql
-- Composite unique constraint (email per tenant)
ALTER TABLE accounts ADD CONSTRAINT uq_tenant_email UNIQUE (tenant_id, email);

-- CHECK constraint enforcing business rule
ALTER TABLE orders ADD CONSTRAINT chk_positive_quantity CHECK (quantity > 0);
```

Enterprise tip: name constraints so error logs are actionable (e.g. `chk_positive_price`).

### Part 2 — Indexes (performance at scale)

Indexes (usually B-Trees) keep columns sorted so lookups are logarithmic (O(log N)) instead of linear (O(N)). Primary keys and unique constraints create indexes automatically; create additional indexes for frequent filters, joins, and sorts.

Basic index examples

```sql
-- Single-column index
CREATE INDEX idx_users_last_name ON users(last_name);

-- Composite index (left-to-right matters)
CREATE INDEX idx_users_location ON users(country, city);
```

Composite index behavior:

- `WHERE country = 'USA'` — uses the index
- `WHERE country = 'USA' AND city = 'Seattle'` — uses the index
- `WHERE city = 'Seattle'` — does NOT use the index (left-to-right rule)

Advanced index patterns

```sql
-- Partial index (PostgreSQL): index only active users' emails
CREATE INDEX idx_users_active_email ON users(email) WHERE is_active = TRUE;

-- Expression index: index lower(email) for case-insensitive lookups
CREATE INDEX idx_users_email_lower ON users(LOWER(email));

-- Covering index (include): include additional columns to avoid lookups (Postgres uses INCLUDE)
CREATE INDEX idx_orders_customer_date ON orders(customer_id, order_date) INCLUDE (total_amount);
```

Indexes and `LIKE` queries

- `WHERE last_name LIKE 'Smit%'` — can use B-Tree index
- `WHERE last_name LIKE '%mith'` — cannot use B-Tree and is slow (full table scan)

### The trade-offs

- Storage: indexes consume disk space (a copy of data ordered for fast access)
- Writes: `INSERT`/`UPDATE`/`DELETE` must update indexes, slowing writes

Guideline: avoid indexing everything. Only add indexes for columns used frequently in `WHERE`, `JOIN`, or `ORDER BY`.

### Quick troubleshooting commands

```sql
-- Show indexes for a table (Postgres)
\d+ users

-- Explain a query plan to see if an index is used
EXPLAIN ANALYZE SELECT * FROM users WHERE last_name = 'Anderson';
```

## Up next

You now know how to lock down data with constraints and accelerate reads with indexes. Next, learn Normalization to design tables correctly.

Proceed to [09-Normalization.md](09-Normalization.md).

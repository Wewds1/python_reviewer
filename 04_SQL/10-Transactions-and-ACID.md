# 10 — Transactions and ACID Properties

Up to this point we have treated SQL statements in isolation: we run an INSERT or UPDATE and the database executes it. Real-world, enterprise applications do not run in a vacuum — many users interact with the database at the same millisecond.

What happens if User A buys the last pair of shoes at the exact moment User B adds them to their cart? What happens if your Python server crashes halfway through processing a $1,000 bank transfer? What happens if an admin updates ticket prices while a customer is halfway through checkout?

To prevent data corruption and unpredictable state, relational databases provide Transactions.

## 1. The classic problem: multi-step operations

Imagine a simple banking app: Alice wants to send $100 to Bob. In SQL this requires two separate updates:

```sql
-- Step 1: Deduct $100 from Alice
UPDATE accounts
SET balance = balance - 100
WHERE user_id = 1;

-- Step 2: Add $100 to Bob
UPDATE accounts
SET balance = balance + 100
WHERE user_id = 2;
```

The danger: what if Step 1 succeeds but the server crashes before Step 2 runs? Alice has lost $100 but Bob never received it — money disappears from the system. This kind of partial failure is unacceptable for enterprise systems.

The same pattern appears in many domains:
- E-commerce: deducting inventory and writing order history
- Social platforms: deleting an account and all associated posts

## 2. What is a transaction?

A transaction is a logical unit of work that contains one or more SQL statements. The database guarantees the transaction behaves as a single, indivisible operation: either all statements succeed, or none do.

You control transactions with Transaction Control Language (TCL):

- `BEGIN` (or `START TRANSACTION`): start a transaction block
- `COMMIT`: persist all changes made in the transaction
- `ROLLBACK`: undo every change made since the `BEGIN`

Example (same transfer inside a transaction):

```sql
BEGIN;

UPDATE accounts SET balance = balance - 100 WHERE user_id = 1;
UPDATE accounts SET balance = balance + 100 WHERE user_id = 2;

COMMIT;
```

If the server crashes before `COMMIT`, the database will detect the incomplete transaction and roll back the partial changes when it recovers, restoring Alice's balance.

## 3. The ACID properties

Enterprise databases (PostgreSQL, SQL Server, Oracle, etc.) adhere to four guarantees summarized by ACID:

### A — Atomicity (All or nothing)

A transaction is an indivisible atom of work. It cannot be partially completed. If any part fails, the entire transaction is rolled back.

Example: in checkout, if inventory deduction fails, the payment and order creation must be rolled back.

### C — Consistency

A transaction moves the database from one valid state to another, preserving all constraints (primary keys, foreign keys, CHECK constraints, triggers, etc.). You cannot commit data that violates schema rules.

Example: a `CHECK (stock_quantity >= 0)` prevents committing a negative stock value; an offending transaction is rejected and rolled back.

### I — Isolation

Concurrent transactions must not interfere with each other. A transaction should not see another transaction's uncommitted (partial) work.

Example: two users attempting to buy the same seat should not both succeed; the database enforces isolation to prevent double-booking.

### D — Durability

Once a transaction is committed, its changes are permanent — even in the event of a crash. Databases typically write commit information to a write-ahead log (WAL) before acknowledging success.

## 4. Concurrency problems (why isolation is hard)

Running transactions sequentially would be safe but slow. Databases run many transactions concurrently and provide isolation levels to balance safety and performance. Common problems include:

- Dirty reads: reading uncommitted data that may later be rolled back
- Non-repeatable reads: data read twice in a transaction changes in between reads
- Phantom reads: new rows appear or disappear between related queries

SQL defines standard isolation levels to address these issues: `READ UNCOMMITTED`, `READ COMMITTED`, `REPEATABLE READ`, and `SERIALIZABLE`. Higher isolation prevents more anomalies but can reduce concurrency and increase contention.

PostgreSQL and SQL Server default to `READ COMMITTED`, which prevents dirty reads and is suitable for most web apps. Use `SERIALIZABLE` for critical reports that require strict correctness.

## 5. Deadlocks

Databases use locks to enforce isolation, which can lead to deadlocks: two transactions waiting on each other's locks indefinitely. When detected, the engine aborts one transaction and returns a deadlock error.

Best practices: catch deadlock errors in your application, retry the transaction, and access shared resources in a consistent order across your codebase to reduce deadlock risk.

---

Proceed to `11-Views-and-Stored-Procedures.md` to learn how to encapsulate complex logic inside the database.
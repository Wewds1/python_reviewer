# 11 — Views, Stored Procedures, and Triggers

As your enterprise application scales, queries grow complex. Multiple applications (a Python backend, BI dashboard, and mobile API) may all need the same business rules. To reduce duplication, simplify code, and encapsulate rules near the data, databases let you store logic using Views, Stored Procedures, and Triggers.
## Part 1: Views (Virtual Tables)

A View is a saved SQL query that behaves like a virtual table. It does not store rows itself; it stores the query that retrieves rows from underlying tables.
Why use views?

- **Simplicity & abstraction:** Hide a complex query behind a simple name.
- **Security & masking:** Expose only selected columns/rows (e.g., hide `salary`/`ssn`).
- **Consistency:** Update the view definition once instead of changing many client apps.
Example — creating and querying a view:

```sql
CREATE OR REPLACE VIEW user_spending_summary AS
-- Querying the view:
SELECT first_name, lifetime_value
FROM user_spending_summary
### Updatable views and `WITH CHECK OPTION`

If a view maps 1:1 to a single table, it can be updatable (support INSERT/UPDATE/DELETE). Use `WITH CHECK OPTION` to prevent changes that would make the row disappear from the view.
```sql
CREATE VIEW vip_customers AS
SELECT user_id, first_name, email, is_vip
## Part 2: Materialized Views (The performance hack)

Standard views re-run their query each time. Materialized views store the query result on disk for fast reads at the cost of staleness.
```sql
CREATE MATERIALIZED VIEW monthly_sales_report AS
SELECT DATE_TRUNC('month', order_date) AS month,
-- Refresh periodically (e.g., nightly)
REFRESH MATERIALIZED VIEW monthly_sales_report;
```
Enterprise tip: In PostgreSQL, `REFRESH MATERIALIZED VIEW CONCURRENTLY` avoids blocking readers but requires a unique index.

## Part 3: Functions vs Stored Procedures
Functions (UDFs) and Procedures are saved programs. They differ in purpose and capabilities.

### User-Defined Functions (UDFs)
- Purpose: compute and return a value; used inline in queries.
- Limitation: typically cannot manage transactions (no COMMIT/ROLLBACK inside the function).

```sql
-- Used inline:
SELECT order_id, subtotal, calculate_tax(subtotal, 'CA') AS tax FROM orders;
```
### Stored Procedures

- Purpose: perform actions or batches; invoked with `CALL`.
- Power: can manage transactions, handle exceptions, and perform multiple statements atomically.

```sql
-- Call from application:
CALL process_refund(9942, 50.00);
```
Why use procedures?

- Reduced network traffic: execute complex logic server-side with one call.
- Security: grant `EXECUTE` without exposing underlying table permissions.

## Part 4: Database Triggers (Event-driven logic)
A trigger automatically fires in response to `INSERT`, `UPDATE`, or `DELETE` events. Triggers can run `BEFORE` or `AFTER` the event.

Example — audit trail for salary changes:
```sql
CREATE OR REPLACE FUNCTION log_salary_change()
RETURNS TRIGGER
CREATE TRIGGER trigger_audit_salary
AFTER UPDATE ON employees
FOR EACH ROW
## Part 5: The great enterprise debate

Should you put business logic in the database?

- The "Thick Database" approach: push logic into stored procedures and the DB (common in banking, legacy systems). Pros: performance, proximity to data.
- The "Thin Database" approach: keep business logic in the application (modern standard). Pros: better version control, easier debugging, easier scaling, less vendor lock-in.

Modern best practice: default to application-layer logic in `Python`. Use Views for reporting, Materialized Views for heavy precomputed queries, and Triggers sparingly for guaranteed, audit or integrity tasks.

---

Proceed to `12-Indexes-and-Query-Optimization.md` for performance tuning and index strategies.
11: Views, Stored Procedures, and TriggersAs your enterprise application scales, your database queries will inevitably become more complex. You might find yourself writing massive, 50-line SELECT statements with half a dozen JOINs, aggregations, and subqueries just to generate a standard daily report.Furthermore, you might have multiple different applications (e.g., a Python web backend, a BI reporting dashboard, and a mobile app API) all hitting the same database. If a business rule changes, updating the exact same complex logic across three different codebases is a recipe for disaster.To reduce duplication, simplify code, improve security, and encapsulate business logic, relational databases allow you to store logic directly on the database server using Views, Stored Procedures, and Triggers.Part 1: Views (Virtual Tables)A View is essentially a saved SQL query that acts like a virtual table. It does not physically store data itself; rather, it stores the instructions (the query) on how to retrieve the data from the underlying physical tables.Why Use Views?Simplicity & Abstraction: You can hide a massive, complex query behind a simple view name. When the Python backend queries the view, it looks and behaves exactly like querying a standard table.Security & Data Masking: You can create a view that exposes only specific columns or rows to a user. For example, you can grant an HR intern access to an employee_directory_view that hides the salary and ssn columns present in the main employees table.Consistency: If the underlying physical table structure changes, you only need to update the View definition in one place, rather than hunting down and updating 50 different Python scripts.Creating and Using a ViewImagine an E-Commerce database where generating a summary of a user's total spending requires joining users, orders, and payments.-- 1. Create the View
CREATE OR REPLACE VIEW user_spending_summary AS
SELECT 
    u.user_id,
    u.first_name,
    u.last_name,
    u.country,
    COUNT(o.order_id) AS total_orders,
    SUM(o.total_amount) AS lifetime_value,
    MAX(o.order_date) AS last_purchase_date
FROM users u
LEFT JOIN orders o ON u.user_id = o.user_id
WHERE u.status = 'active'
GROUP BY u.user_id, u.first_name, u.last_name, u.country;
Once the view is created on the database, your Python backend can query it as if it were a physical table. You can even apply further WHERE and ORDER BY clauses to it:-- 2. Query the View
SELECT first_name, lifetime_value 
FROM user_spending_summary 
WHERE country = 'USA' AND lifetime_value > 1000
ORDER BY lifetime_value DESC;
Behind the scenes, the database engine seamlessly merges your outer SELECT with the complex instructions saved inside the view, optimizing it into a single execution plan.Updatable Views and WITH CHECK OPTIONNormally, Views are read-only because they involve joins and aggregations. However, if a view maps 1-to-1 with a single underlying table, it can be an Updatable View. You can run INSERT, UPDATE, and DELETE commands directly against the view.-- Create a view for only VIP customers
CREATE VIEW vip_customers AS
SELECT user_id, first_name, email, is_vip
FROM users
WHERE is_vip = TRUE
WITH CHECK OPTION;
The WITH CHECK OPTION is a powerful enterprise feature. It prevents a user from inserting or updating a row through the view that would cause the row to instantly disappear from the view.For example, if a developer runs this via the Python backend:-- This will fail and throw a constraint violation error!
UPDATE vip_customers SET is_vip = FALSE WHERE user_id = 101;
Because of the WITH CHECK OPTION, the database rejects the update because setting is_vip = FALSE violates the view's own WHERE clause.Part 2: Materialized Views (The Performance Hack)Standard Views run their underlying query every single time they are accessed. If the view contains complex math over 50 million rows, querying it will be agonizingly slow, eating up CPU cycles.A Materialized View solves this. It runs the query once and physically saves the results to the disk.Pro: Querying it is instantaneous, just like reading a normal table.Con: The data becomes "stale". As new orders come in, the Materialized View does not update automatically.You must manually tell the database to refresh the data:-- Creates the physical table based on the query
CREATE MATERIALIZED VIEW monthly_sales_report AS
SELECT 
    DATE_TRUNC('month', order_date) AS month,
    SUM(total) AS revenue
FROM orders
GROUP BY DATE_TRUNC('month', order_date);

-- Later, to update the data (usually run via a nightly Cron job)
REFRESH MATERIALIZED VIEW monthly_sales_report;
Enterprise Tip: In PostgreSQL, a standard REFRESH locks the table, meaning nobody can read it while it updates. Use REFRESH MATERIALIZED VIEW CONCURRENTLY to update it in the background without blocking read queries (requires a Unique Index on the view).Part 3: Functions vs. Stored ProceduresIf a View is a saved SELECT statement, Functions and Procedures are saved programs that contain loops, variables, IF/THEN logic, and multiple SQL statements.While often used interchangeably in conversation, they have strict technical differences in modern SQL (like PostgreSQL 11+).User-Defined Functions (UDFs)Purpose: To compute and return a value.Usage: Called inside a standard SQL query (e.g., in a SELECT or WHERE clause).Limitation: Functions generally cannot manage transactions (they cannot COMMIT or ROLLBACK halfway through).-- A function to calculate tax
CREATE OR REPLACE FUNCTION calculate_tax(subtotal DECIMAL, state_code VARCHAR) 
RETURNS DECIMAL 
LANGUAGE plpgsql
AS $$
DECLARE
    tax_rate DECIMAL;
BEGIN
    IF state_code = 'CA' THEN tax_rate := 0.0825;
    ELSIF state_code = 'NY' THEN tax_rate := 0.0400;
    ELSE tax_rate := 0.00;
    END IF;
    
    RETURN subtotal * tax_rate;
END;
$$;

-- Used inline:
SELECT order_id, subtotal, calculate_tax(subtotal, 'CA') AS tax FROM orders;
Stored ProceduresPurpose: To perform an action or a batch of actions.Usage: Invoked independently using the CALL statement.Power: Procedures can manage transactions. You can open a transaction, try an update, catch an error, ROLLBACK, and write to an error log all within the procedure.CREATE OR REPLACE PROCEDURE process_refund(
    IN p_order_id INT, 
    IN p_refund_amount DECIMAL
)
LANGUAGE plpgsql
AS $$
BEGIN
    -- 1. Update order status
    UPDATE orders SET status = 'refunded' WHERE order_id = p_order_id;

    -- 2. Insert financial record
    INSERT INTO refunds (order_id, amount) VALUES (p_order_id, p_refund_amount);

    -- Commit the transaction (PostgreSQL handles this implicitly in procedures, 
    -- but you can explicitly use COMMIT / ROLLBACK here for complex multi-step logic)
    COMMIT;
    
EXCEPTION
    WHEN OTHERS THEN
        -- If anything fails, rollback everything and log the error
        ROLLBACK;
        INSERT INTO system_logs (error_message) VALUES ('Refund failed for order ' || p_order_id);
END;
$$;
To execute this from your Python backend, you simply run:CALL process_refund(9942, 50.00);
Why Use Stored Procedures?Reduced Network Traffic: Instead of your Python backend sending 10 different SQL queries across the network to process a complex checkout, it sends one command. The database executes all the logic internally, which is significantly faster.Security: You can grant a backend application permission to EXECUTE a specific procedure without giving it INSERT or UPDATE permissions on the underlying tables.Part 4: Database Triggers (Event-Driven Logic)A Trigger is a special type of stored procedure that automatically executes ("fires") in response to a specific event on a particular table or view.Events that can fire a trigger include INSERT, UPDATE, or DELETE. They can be set to run BEFORE the event (to validate or modify data) or AFTER the event (to log changes or update related tables).Example: The Audit TrailIn enterprise finance and healthcare, you must track every time a sensitive record changes. You should not rely on Python to remember to write an audit log. A database trigger guarantees it happens.-- 1. Create a function that writes to an audit table
CREATE OR REPLACE FUNCTION log_salary_change()
RETURNS TRIGGER 
LANGUAGE plpgsql
AS $$
BEGIN
    -- 'NEW' and 'OLD' are special variables available inside triggers
    IF NEW.salary <> OLD.salary THEN
        INSERT INTO employee_audit_log (
            employee_id, old_salary, new_salary, changed_at, changed_by
        ) VALUES (
            OLD.employee_id, OLD.salary, NEW.salary, CURRENT_TIMESTAMP, CURRENT_USER
        );
    END IF;
    
    -- Must return the NEW record so the original UPDATE can proceed
    RETURN NEW;
END;
$$;

-- 2. Attach the trigger to the employees table
CREATE TRIGGER trigger_audit_salary
AFTER UPDATE ON employees
FOR EACH ROW
EXECUTE FUNCTION log_salary_change();
Now, if a rogue database admin manually types UPDATE employees SET salary = 900000 WHERE id = 5;, the trigger fires instantly, and their actions are permanently logged.Part 5: The Great Enterprise DebateYou now know that you can put complex business logic directly into the database using Procedures and Triggers. The real question is: Should you?This is one of the longest-running architectural debates in software engineering.The "Thick Database" ApproachProponents say: The database is the only thing that actually matters. Applications come and go, but data is forever. Stored procedures are blisteringly fast because the logic lives right next to the data on the disk.Used heavily by: Traditional banking, older enterprise systems (Oracle/SQL Server shops), and highly secure environments.The "Thin Database" Approach (Modern Standard)Proponents say: The database should only be a dumb, highly-optimized, reliable storage bucket. All business logic should live in the Python/Backend layer.Why this won out in modern tech:Version Control & CI/CD: Python code is easy to track in Git, review in Pull Requests, and deploy automatically. Managing and versioning 500 stored procedures inside a live database state is notoriously difficult.Debugging: Debugging Python with breakpoints is easy. Debugging PL/pgSQL inside a database engine is a terrible developer experience.Scaling: It is very easy and cheap to spin up 50 extra Python Docker containers on AWS to handle heavy compute logic. It is extremely expensive and difficult to scale a relational database server to handle high CPU loads.Vendor Lock-in: Stored procedure syntax is wildly different between Postgres (PL/pgSQL), Oracle (PL/SQL), and SQL Server (T-SQL). If your logic is in Python, switching database vendors is infinitely easier.Enterprise Golden Rule: In modern tech companies, default to writing your business logic in Python. Use Views to simplify reporting, use Materialized Views for performance, use Triggers strictly for audit logging, and only use Stored Procedures for incredibly specific tasks where the performance gain of executing logic directly on the disk is absolutely mandatory.Up NextYou have now reached the end of the theoretical concepts regarding database architecture, querying, and programmability. You know how to design schemas, query millions of rows, protect data with ACID transactions, and abstract logic into Views and Procedures.Proceed to 12-SQL-Best-Practices.md for a concise summary of the daily habits, formatting rules, and security mindsets (like preventing SQL Injection) you must adopt to write professional enterprise SQL.
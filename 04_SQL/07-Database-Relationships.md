## Database relationships and DDL

We learned how to manipulate data with DML (`SELECT`, `INSERT`, `UPDATE`, `DELETE`) and how to use `JOIN`s to reassemble related rows. To enforce structure and relationships we use Data Definition Language (DDL): `CREATE`, `ALTER`, and `DROP`.

This lesson covers the three foundational relationship types: One-to-Many, One-to-One, and Many-to-Many, plus referential integrity options.

### DDL basics

- `CREATE TABLE` — create a new table
- `ALTER TABLE` — modify an existing table (add/remove columns or constraints)
- `DROP TABLE` — permanently remove a table and its data (dangerous)

```sql
-- Create a basic table
CREATE TABLE departments (
  department_id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);

-- Add a new column to an existing table
ALTER TABLE departments ADD COLUMN budget DECIMAL(12,2);

-- Delete the table entirely (Dangerous!)
DROP TABLE departments;
```

### 1. One-to-Many (1:N)

Concept: A single row in table A maps to many rows in table B; the FK is stored on the "many" side (child).

Example: One department has many employees. Place the FK on `employees.department_id`.

```sql
-- Parent table (one)
CREATE TABLE departments (
  department_id SERIAL PRIMARY KEY,
  department_name VARCHAR(100) NOT NULL
);

-- Child table (many)
CREATE TABLE employees (
  employee_id SERIAL PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  department_id INTEGER,
  CONSTRAINT fk_department FOREIGN KEY (department_id) REFERENCES departments(department_id)
);
```

Enterprise tip: Name constraints explicitly (e.g., `CONSTRAINT fk_department`) for clearer error logs.

### 2. One-to-One (1:1)

Concept: Each row in A maps to at most one row in B and vice versa. Common for splitting optional or sensitive fields.

Implementation: Add a FK on the child plus a `UNIQUE` constraint on that FK.

```sql
CREATE TABLE users (
  user_id SERIAL PRIMARY KEY,
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE user_profiles (
  profile_id SERIAL PRIMARY KEY,
  user_id INTEGER UNIQUE NOT NULL, -- FK + UNIQUE => 1:1
  bio TEXT,
  avatar_url VARCHAR(255),
  CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(user_id)
);
```

### 3. Many-to-Many (M:N)

Concept: Multiple rows in A map to multiple rows in B. Implement via a junction table that contains FKs to both parents.

```sql
CREATE TABLE students (
  student_id SERIAL PRIMARY KEY,
  name VARCHAR(100) NOT NULL
);

CREATE TABLE courses (
  course_id SERIAL PRIMARY KEY,
  title VARCHAR(100) NOT NULL
);

CREATE TABLE student_courses (
  student_id INTEGER NOT NULL,
  course_id INTEGER NOT NULL,
  enrollment_date DATE DEFAULT CURRENT_DATE,
  PRIMARY KEY (student_id, course_id),
  CONSTRAINT fk_student FOREIGN KEY (student_id) REFERENCES students(student_id),
  CONSTRAINT fk_course FOREIGN KEY (course_id) REFERENCES courses(course_id)
);
```

Note: Junction tables often carry relationship-specific attributes such as `enrollment_date`, `grade`, etc.

### 4. Referential integrity (ON DELETE / ON UPDATE)

Deleting a parent row can orphan child rows. Choose a FK action that matches your domain rules:

- `ON DELETE RESTRICT` / `NO ACTION` (default): Prevent parent deletion if children exist.
- `ON DELETE CASCADE`: Deleting the parent deletes associated children automatically. Use with extreme caution.
- `ON DELETE SET NULL`: Delete parent, set FK on children to `NULL`.

```sql
CREATE TABLE user_sessions (
  session_id SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  token VARCHAR(255) NOT NULL,
  CONSTRAINT fk_user_session FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);
```

Choose conservative defaults (`RESTRICT`) in financial or auditing domains; use `CASCADE` only when you truly want dependent data removed.

### Up next

You can now design and implement relational architectures. Next, learn how constraints and indexes enforce correctness and performance.

Proceed to [08-Constraints-and-Indexes.md](08-Constraints-and-Indexes.md).

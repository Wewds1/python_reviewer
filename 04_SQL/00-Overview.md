# Module 4: SQL and Relational Databases

## Welcome to Module 4

Welcome to Module 4 of the Enterprise Python Backend Developer Bootcamp.

As a backend engineer, Python is only half of the equation. Your application needs a place to store, organize, and retrieve data efficiently, reliably, and securely. This is where the database comes in.

In the enterprise world, data is one of the most valuable assets a company owns. Your role as a database engineer or backend developer is not just to write queries that work. It is to design schemas that scale, write queries that perform under heavy load, and guarantee data integrity even when systems fail.

This module will transform you from someone who knows basic SQL commands into a professional who can design normalized enterprise schemas, analyze query performance, and understand how a Relational Database Management System (RDBMS) works internally.

---

## Why This Module Matters

At companies like PwC, backend engineers work with massive datasets. You might build an API that aggregates millions of financial records, design a hospital patient management system, or optimize a daily report that a client depends on.

- Python plus SQL: Python is the logic layer; the database is the persistence layer. You need mastery of both.
- Performance is paramount: A poorly written SQL query can slow or halt an entire application.
- Data integrity is non-negotiable: If money is transferred and a crash occurs midway, data must remain correct.
- System design impact: A weak schema design can cause long-term architectural problems.

---

## Learning Objectives

By the end of this module, you will be able to:

- Understand RDBMS architecture:
	Explain file systems vs NoSQL vs relational databases, and understand DBMS internals.
- Design enterprise schemas:
	Translate business requirements into ERDs and robust table designs.
- Master SQL syntax:
	Write SQL using filtering, sorting, aggregation, and window functions (where applicable).
- Conquer joins:
	Apply INNER, LEFT, RIGHT, FULL OUTER, CROSS, and SELF joins correctly.
- Enforce data integrity:
	Use primary keys, foreign keys, unique constraints, and check constraints.
- Optimize performance:
	Understand B-Tree indexing and clustered vs non-clustered trade-offs.
- Normalize data:
	Apply 1NF, 2NF, and 3NF, and identify when denormalization is practical.
- Manage concurrency:
	Use BEGIN, COMMIT, and ROLLBACK and explain ACID and isolation levels.
- Use database objects:
	Create views and stored procedures to encapsulate logic.
- Apply best practices:
	Write readable, secure SQL and prevent SQL injection.

---

## Module Structure

This module is a progressive journey from fundamentals to enterprise operations.

### Part 1: Foundations of Data

- 01-Introduction-to-Databases.md
	- Evolution of data storage, RDBMS vs NoSQL, and database engine roles
- 02-Database-Design.md
	- Mapping real-world entities to tables, attributes, and ERDs

### Part 2: Querying Data (DML)

- 03-SQL-Basics.md
	- SELECT, INSERT, UPDATE, DELETE
- 04-Filtering-and-Sorting.md
	- WHERE, logical operators, ORDER BY
- 05-Aggregation.md
	- GROUP BY, HAVING, aggregate functions
- 06-JOINs.md
	- Combining data across related tables

### Part 3: Architecture and Integrity (DDL)

- 07-Database-Relationships.md
	- 1:1, 1:N, and M:N relationship modeling
- 08-Constraints-and-Indexes.md
	- Rule enforcement and read performance optimization
- 09-Normalization.md
	- Eliminating redundancy and preventing anomalies

### Part 4: Enterprise Operations

- 10-Transactions-and-ACID.md
	- Concurrency control and reliability
- 11-Views-and-Stored-Procedures.md
	- Abstraction and reusable data-layer logic
- 12-SQL-Best-Practices.md
	- Formatting, security, and senior-level SQL habits

### Part 5: Practical Application and Assessment

- 13-Interview-Questions.md
	- Real enterprise interview preparation
- 14-Coding-Challenges.md
	- 100 graded SQL exercises
- 15-Hospital-Database-Project.md
	- Capstone: normalized Hospital Management System
- 16-Module-Assessment.md
	- Comprehensive evaluation

---

## Prerequisites for This Module

- Basic understanding of data types from Module 1 and Module 2
	- strings, integers, booleans, dates
- Comfort with command-line usage
- Local database installation
	- PostgreSQL recommended
	- Concepts also apply to MySQL and SQL Server
- A SQL client tool
	- DBeaver, pgAdmin, DataGrip, or VS Code SQL tools

---

## Note from Your Technical Lead

"SQL is deceptively simple. The syntax reads like English: 'SELECT this FROM that'. Because of this, many developers learn just enough to get by, relying on ORMs in Python to do the heavy lifting.

Do not fall into this trap.

When a system scales to millions of rows, ORMs can generate inefficient queries. When the system slows down, the engineer who understands execution plans, indexing strategies, and normalization is the one who fixes it.

Treat SQL as a primary programming language in your backend toolkit. Master the data layer, and the application layer becomes much easier to build."

---

Proceed to 01-Introduction-to-Databases.md.
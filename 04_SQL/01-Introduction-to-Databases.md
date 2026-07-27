# 01. Introduction to Databases

## Module 4: SQL and Relational Databases

Welcome to Module 4 of the Enterprise Python Backend Developer Bootcamp.

As a backend engineer, Python is only half of the equation. Your application needs a place to store, organize, and retrieve data efficiently, reliably, and securely. This is where the database comes in.

In the enterprise world, data is one of the most valuable assets a company owns. Your role is not just to write queries that work. Your role is to design schemas that scale, write queries that perform under heavy load, and guarantee data integrity even when systems fail.

This module is designed to move you from basic SQL familiarity to enterprise-level database thinking.

---

## Why This Module Matters

At companies like PwC, backend engineers work with large, high-value datasets. You might:

- Build APIs that aggregate millions of financial records
- Design patient-management systems for hospital networks
- Optimize slow business-critical reports

Key realities:

- **Python plus SQL:** Python is the logic layer, SQL is the persistence layer.
- **Performance matters:** Poor SQL can bottleneck an entire backend.
- **Integrity matters:** Crashes must not corrupt financial or clinical records.
- **Schema quality matters:** Bad schema decisions are expensive long-term.

---

## Learning Objectives

By the end of this module, you will be able to:

- Explain RDBMS architecture and compare it with file systems and NoSQL systems
- Translate business requirements into normalized database schemas and ERDs
- Write SQL for filtering, sorting, aggregation, and advanced querying
- Use joins correctly: INNER, LEFT, RIGHT, FULL OUTER, CROSS, SELF
- Enforce integrity with primary keys, foreign keys, unique constraints, and checks
- Understand indexing trade-offs and query performance basics
- Apply 1NF, 2NF, and 3NF, and evaluate denormalization trade-offs
- Use transactions and explain ACID/isolation behavior
- Create and use views and stored procedures
- Follow secure and readable SQL best practices, including SQL injection prevention

---

## Module Roadmap

### Part 1: Foundations of Data

- 01-Introduction-to-Databases.md
	- Data storage evolution, RDBMS vs NoSQL, database engine roles
- 02-Database-Design.md
	- Entities, attributes, and ERD fundamentals

### Part 2: Querying Data (DML)

- 03-SQL-Basics.md
	- SELECT, INSERT, UPDATE, DELETE
- 04-Filtering-and-Sorting.md
	- WHERE, logical operators, ORDER BY
- 05-Aggregation.md
	- GROUP BY, HAVING, aggregate functions
- 06-JOINs.md
	- Multi-table querying patterns

### Part 3: Architecture and Integrity (DDL)

- 07-Database-Relationships.md
	- 1:1, 1:N, M:N modeling
- 08-Constraints-and-Indexes.md
	- Data rules and performance strategies
- 09-Normalization.md
	- Redundancy elimination and anomaly prevention

### Part 4: Enterprise Operations

- 10-Transactions-and-ACID.md
	- Reliability and concurrency control
- 11-Views-and-Stored-Procedures.md
	- Encapsulating data logic
- 12-SQL-Best-Practices.md
	- Formatting, security, maintainability

### Part 5: Application and Assessment

- 13-Interview-Questions.md
	- Enterprise interview preparation
- 14-Coding-Challenges.md
	- 100 graded SQL exercises
- 15-Hospital-Database-Project.md
	- Capstone implementation
- 16-Module-Assessment.md
	- Final evaluation

---

## Prerequisites

- Basic Python data types from Modules 1 and 2
- Familiarity with command-line usage
- Local database installation (PostgreSQL recommended)
- A SQL client tool (DBeaver, pgAdmin, DataGrip, or VS Code SQL extensions)

---

## Note from Your Technical Lead

"SQL is deceptively simple. The syntax reads like English: 'SELECT this FROM that'. Because of this, many developers learn just enough to get by, relying on ORMs in Python to do the heavy lifting.

Do not fall into this trap.

At scale, ORMs can generate inefficient queries. When systems slow down, engineers who understand execution plans, indexing strategies, and normalization are the ones who solve the problem.

Treat SQL as a primary programming language in your backend toolkit. Master the data layer, and the application layer becomes much easier to build."

---

Proceed to **02-Database-Design.md** after reviewing this introduction.
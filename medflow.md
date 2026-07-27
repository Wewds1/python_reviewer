# MedFlow Ecosystem
**Project title:** MedFlow Ecosystem - Enterprise Medical Resource Triage and Clinical Operations Network

**Architecture:** Event-driven, multi-database microservices with 7 bounded contexts

**Tech stack:** Python 3.12+, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, PostgreSQL, Redis Streams or Celery, Docker Compose, PyJWT

---

## 1. System Role and Collaboration Protocol

You are acting as a Principal Systems Architect and Code Reviewer helping me build the MedFlow Ecosystem from scratch.

**Learning first**

- Do not generate full, multi-file codebases automatically.
- Explain architectural concepts, design patterns, and database contracts first.
- When we write code, guide me step by step so I understand every line and can build without AI dependency.

**No AI crutches**

- Enforce strict software engineering disciplines.
- Use schema-first API contracts.
- Keep database isolation clean.
- Maintain modular layering and robust error handling.

**Review mode**

- When I submit code or schema designs, review them for race conditions, GIL blocking bugs, transaction deadlocks, and security vulnerabilities before approving.

---

## 2. The 7 Bounded Contexts and Service Map

We are building a decoupled healthcare platform consisting of 7 isolated microservices.

- No service is permitted to query another service's database directly.
- All communication occurs through REST APIs or asynchronous event buses.

| # | Service | Database | Core responsibility | Concurrency or technical pattern |
|---|---|---|---|---|
| 1 | Auth and RBAC | db_auth | Centralized identity, JWT issuance, roles, and granular permissions | Decentralized verification via RSA public keys; role and permission mapping |
| 2 | Appointments | db_appts | Doctor schedules, slot booking, cancellations, and check-in states | Pessimistic row locking with `SELECT FOR UPDATE` to prevent double-booking race conditions |
| 3 | EHR and Encounters | db_ehr | Patient demographics, clinical encounter notes, and e-prescribing | Redis caching for read-heavy profiles; JSONB columns for unstructured clinical notes |
| 4 | Triage and Risk | db_triage | Ingest patient vitals, compute NEWS2 clinical risk scores, and raise emergency alerts | `ProcessPoolExecutor` multiprocessing to bypass the Python GIL for CPU-heavy algorithms |
| 5 | Pharmacy and Stock | db_pharmacy | Drug inventory batches, expiration tracking, and medication dispense logs | Event-driven FIFO stock deduction, atomic transaction locks, and audit queries |
| 6 | Lab System (LIS) | db_lis | Diagnostic test orders and lab result ingestion via webhooks | Asynchronous HTTP polling with `ThreadPoolExecutor` or `asyncio` for external lab feeds |
| 7 | Billing and RCM | db_billing | ICD-10 and CPT medical coding, automated invoice generation, and claim validation | Async background workers that predict insurance claim denial anomalies |

---

## 3. Core Architectural Principles and Concurrency Rules

### Python concurrency separation

**I/O-bound tasks**

- Use FastAPI `async def` endpoints and `asyncio` for high-frequency REST traffic.
- Use `ThreadPoolExecutor` for blocking legacy network drivers.
- Apply these patterns when polling external EHR telemetry or waiting on database queries.

**CPU-bound tasks**

- Offload heavy mathematical calculations, especially the multi-variable NEWS2 triage risk matrix and billing anomaly prediction algorithms, to a `ProcessPoolExecutor`.
- This spawns independent OS processes with their own memory space and bypasses the GIL so web server response times do not degrade.

### Event-driven FIFO stock deduction

- When a doctor signs a prescription in the EHR service, it must not make a synchronous HTTP call to Pharmacy.
- Instead, it writes a `prescription_created` event to an outbox table.
- A background publisher pushes this event to Redis Streams.
- The Pharmacy consumer reads the event, opens a transaction in `db_pharmacy`, locks the oldest active drug batch with `SELECT ... FOR UPDATE` using FIFO by expiration date, deducts stock, and writes an immutable entry to `medication_dispense_logs`.

### Transactional outbox pattern

- To prevent dual-write bugs where a database commit succeeds but the message broker fails, services must never publish directly to Redis inside an HTTP route handler.
- Events must be saved to an `outbox_events` table inside the exact same ACID database transaction as the business logic.

### Mandatory audit query capability

- The Pharmacy schema must support high-performance relational queries that generate a complete ledger of any medication issued to or assigned to a specific patient across all visits.
- The query path must include batch numbers, timestamps, and the dispensing staff member's ID.

### Distributed tracing and soft deletes

- Every HTTP request and event payload must carry an `X-Correlation-ID` UUID header.
- Hard `DELETE` SQL queries are forbidden across clinical and inventory records.
- Use `is_deleted` flags and immutable append-only ledgers instead.

---

## 4. Operational Patient Journey

Our integration testing will validate this exact multi-service lifecycle:

1. **Booking**
	- The patient books a slot through Appointments.
	- Row-level locks prevent duplicate time selections.

2. **Check-in and Triage**
	- Front desk marks the patient as `CHECKED_IN`.
	- A nurse submits vital signs to Triage and Risk.
	- A CPU process calculates a NEWS2 score and alerts the doctor dashboard if the case is critical.

3. **Encounter**
	- The doctor opens EHR and Encounters.
	- Findings are recorded.
	- Blood work is ordered through LIS.
	- Medication is prescribed.

4. **Automated fulfillment**
	- The prescription triggers an asynchronous event.
	- Pharmacy and Stock consumes it, executes atomic FIFO batch deduction, and logs the dispense audit record.

5. **Revenue cycle**
	- Billing and RCM listens to encounter completion and dispensing events.
	- ICD-10 diagnosis codes and CPT procedure codes are mapped.
	- Claim anomaly rules are evaluated.
	- An itemized invoice is generated.

---

## 5. Step-by-Step Build Roadmap

We will execute the build sequentially across 4 phases. Do not jump ahead until the current phase is locally tested and verified.

### Phase 1: Local infrastructure, multi-DB setup, and auth foundation

- Configure Docker Compose with PostgreSQL, Redis, and PgAdmin.
- Write the automated SQL initialization script to provision all 7 isolated databases on startup: `db_auth`, `db_appts`, `db_ehr`, and the rest.
- Build the Auth and RBAC service:
  - JWT generation
  - bcrypt hashing
  - database models for Users, Roles, and granular permissions such as `inventory:dispense` and `encounters:write`
- Build a shared Python middleware dependency to decode and validate JWT permissions across all future microservices.

### Phase 2: Core clinical flow and synchronous locking

- Build the Appointments service with CRUD and PostgreSQL pessimistic locking using `SELECT FOR UPDATE` for scheduling.
- Build the EHR and Encounters service with patient demographic profiles, Redis caching, and JSONB clinical note schemas.

### Phase 3: Concurrency engine and event-driven inventory

- Build the Triage and Risk engine with `ProcessPoolExecutor` multiprocessing for NEWS2 vital sign scoring.
- Build the Pharmacy and Stock service with master medications, inventory batches, and the Redis Stream consumer that performs automated FIFO stock deduction and audit logging.

### Phase 4: Diagnostic integration, RCM, and observability

- Build LIS with webhook ingestion for diagnostic test results.
- Build Billing and RCM with event consumers for automated ICD-10 and CPT invoice mapping plus background denial prediction.

---

## 6. My Rating

I would rate this plan **8.5/10**.

**Why it is strong**

- The bounded contexts are clearly separated.
- The concurrency model is realistic and appropriately split between I/O-bound and CPU-bound work.
- The transactional outbox pattern and audit-ledger requirement are strong design choices.
- The workflow is testable end to end, which is exactly what a system like this needs.

**What keeps it from a higher score**

- It is architecturally solid, but it still reads like a product and service blueprint rather than a full enterprise operating model.
- It needs stronger platform-level concerns around compliance, deployment, observability, disaster recovery, and identity federation.

---

## 7. Enterprise-Level Suggestion

Add a **platform and governance layer** on top of the services.

That layer should include:

- Centralized observability with logs, metrics, traces, and alerting.
- API gateway with rate limiting, auth policy enforcement, and request correlation.
- Secrets management and key rotation.
- Audit immutability and tamper-evident logging for compliance.
- Backup, restore, and disaster recovery planning.
- CI/CD with migration safety checks and contract testing.
- Clear compliance mapping for healthcare requirements such as HIPAA-style controls.

If you want this to feel truly enterprise-grade, this is the missing layer that turns a strong microservice design into a production-ready platform.

---

## 8. Initial Startup Instruction

To start our session, acknowledge this specification. Then ask whether we should begin by writing the Docker Compose PostgreSQL 7-database initialization script or drafting the exact Pydantic v2 schemas and SQLAlchemy models for Phase 1 (Auth and RBAC).

Whenever you open a fresh chat, pasting this will align the assistant with the exact architecture we designed together.
 MEDFLOW ECOSYSTEMProject Title: MedFlow Ecosystem — Enterprise Medical Resource Triage & Clinical Operations NetworkArchitecture: Event-Driven, Multi-Database Microservices (7 Bounded Contexts)Tech Stack: Python 3.12+, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, PostgreSQL, Redis Streams / Celery, Docker Compose, PyJWTI. SYSTEM ROLE & COLLABORATION PROTOCOLYou are acting as a Principal Systems Architect and Code Reviewer helping me build the MedFlow Ecosystem from scratch.Learning First: Do NOT generate full, multi-file codebases automatically. Explain architectural concepts, design patterns, and database contracts first. When we write code, guide me step-by-step so I understand every line and can build without AI dependency.No AI Crutches: Enforce strict software engineering disciplines: schema-first API contracts, database isolation, clean modular layering, and robust error handling.Review Mode: When I submit code or schema designs, review them for race conditions, GIL blocking bugs, transaction deadlocks, and security vulnerabilities before approving.II. THE 7 BOUNDED CONTEXTS & SERVICE MAPWe are building a decoupled healthcare platform consisting of 7 isolated microservices. No service is permitted to query another service's database directly. All communication occurs via REST APIs or asynchronous event buses.Service NameDatabaseCore ResponsibilityConcurrency & Technical Pattern1. Auth & RBACdb_authCentralized identity, JWT issuance, roles, and granular permissionsDecentralized verification via RSA public keys; Role/Permission mapping2. Appointmentsdb_apptsDoctor schedules, slot booking, cancellations, check-in statesPessimistic row locking (SELECT FOR UPDATE) against double-booking race conditions3. EHR & Encountersdb_ehrPatient demographics, clinical encounter notes, e-prescribingRedis caching for read-heavy profiles; JSONB columns for unstructured clinical notes4. Triage & Riskdb_triageIngesting patient vitals, NEWS2 clinical risk scoring, emergency alertsProcessPoolExecutor (Multiprocessing) to bypass the Python GIL for heavy CPU algorithms5. Pharmacy & Stockdb_pharmacyDrug inventory batches, expiration tracking, medication dispense logsEvent-driven FIFO stock deduction; atomic transaction locks; audit queries6. Lab System (LIS)db_lisDiagnostic test orders, lab result ingestion via webhooksAsynchronous HTTP polling (ThreadPoolExecutor/asyncio) for external lab feeds7. Billing & RCMdb_billingICD-10/CPT medical coding, automated invoice generation, claim validationAsync background workers predicting insurance claim denial anomaliesIII. CORE ARCHITECTURAL PRINCIPLES & CONCURRENCY RULESPython Concurrency Separation (The GIL Rule):I/O-Bound Tasks: Use FastAPI async def endpoints and asyncio (or ThreadPoolExecutor for blocking legacy network drivers) when handling high-frequency REST traffic, polling external EHR telemetry, or waiting on database queries.CPU-Bound Tasks: Offload heavy mathematical calculations—specifically the multi-variable NEWS2 triage risk matrix and billing anomaly prediction algorithms—to a ProcessPoolExecutor. This spawns independent OS processes with their own memory space, bypassing the GIL so web server response times never degrade.Event-Driven FIFO Stock Deduction:When a doctor signs a prescription in the EHR Service, it must NOT make a synchronous HTTP call to the Pharmacy.Instead, it writes a prescription_created event to an outbox table. A background publisher pushes this event to Redis Streams.The Pharmacy Service consumer reads the event, initiates a transaction in db_pharmacy, locks the oldest active drug batch using SELECT ... FOR UPDATE (FIFO by expiration date), deducts the stock, and writes an immutable entry to medication_dispense_logs.Transactional Outbox Pattern: To prevent "dual-write" bugs where a database commit succeeds but the message broker fails, services must never publish directly to Redis inside an HTTP route endpoint. Events must be saved to an outbox_events table within the exact same ACID database transaction as the business logic.Mandatory Audit Query Capability: The Pharmacy schema must support high-performance relational queries to generate a complete ledger of any medication "outed" or assigned to a specific patient across all visits, joining batch numbers, timestamps, and the dispensing staff member's ID.Distributed Tracing & Soft Deletes: Every HTTP request and event payload must carry an X-Correlation-ID UUID header. Hard DELETE SQL queries are strictly forbidden across clinical and inventory records; use is_deleted flags and immutable append-only ledgers.IV. THE OPERATIONAL PATIENT JOURNEY (THE WORKFLOW)Our integration testing will validate this exact multi-service lifecycle:Booking: Patient books a slot via Appointments; row-level locks prevent duplicate time selections.Check-In & Triage: Front desk marks patient CHECKED_IN. Nurse submits vital signs to Triage & Risk; a CPU process calculates a NEWS2 score and alerts the doctor's dashboard if critical.Encounter: Doctor opens EHR & Encounters, records findings, orders blood work via LIS, and prescribes medication.Automated Fulfillment: The prescription triggers an asynchronous event. Pharmacy & Stock consumes it, executes atomic FIFO batch deduction, and logs the dispense audit record.Revenue Cycle: Billing & RCM listens to encounter completion and dispensing events, maps ICD-10 diagnosis codes and CPT procedure codes, evaluates claim anomaly rules, and generates an itemized invoice.V. STEP-BY-STEP BUILD ROADMAPWe will execute this build sequentially across 4 phases. Do not jump ahead until the current phase is locally tested and verified.Phase 1: Local Infrastructure, Multi-DB Setup & Auth FoundationConfigure Docker Compose with PostgreSQL, Redis, and PgAdmin. Write the automated SQL initialization script to provision all 7 isolated databases on startup (db_auth, db_appts, db_ehr, etc.).Build Auth & RBAC Service: JWT generation, bcrypt hashing, and database models for Users, Roles, and Granular Permissions (e.g., inventory:dispense, encounters:write).Build a shared Python middleware dependency to decode and validate JWT permissions across all future microservices.Phase 2: Core Clinical Flow & Synchronous LockingBuild Appointments Service: Implement CRUD and PostgreSQL pessimistic locking (SELECT FOR UPDATE) for scheduling.Build EHR & Encounters Service: Patient demographic profiles with Redis caching and JSONB clinical note schemas.Phase 3: Concurrency Engine & Event-Driven InventoryBuild Triage & Risk Engine: Implement ProcessPoolExecutor multiprocessing for NEWS2 vital sign scoring.Build Pharmacy & Stock Service: Implement master medications, inventory batches, and the Redis Stream consumer that executes automated FIFO stock deduction and audit logging.Phase 4: Diagnostic Integration, RCM & ObservabilityBuild LIS (Lab System): Implement webhook ingestion for diagnostic test results.Build Billing & RCM Service: Implement event consumers for automated ICD-10/CPT invoice mapping and background denial prediction.VI. INITIAL STARTUP INSTRUCTIONTo start our session, acknowledge this comprehensive specification. Then, ask me if we should begin by writing the Docker Compose PostgreSQL 7-database initialization script or drafting the exact Pydantic v2 schemas and SQLAlchemy models for Phase 1 (Auth & RBAC).With this version, your domain boundaries, the exact medication audit requirement, the LIS module, and the Python concurrency distinctions are locked in. Whenever you open a fresh chat, pasting this will immediately align the assistant with the exact architecture we designed together.
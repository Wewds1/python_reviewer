# MedFlow Ecosystem

**Project title:** MedFlow Ecosystem — Medical Resource Triage and Clinical Operations Network

**Architecture:** Event-driven, multi-database microservices, 7 bounded contexts

**Tech stack:** Python 3.12+, FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, PostgreSQL, Redis Streams (or Celery), Docker Compose, PyJWT, React (frontend, see section 6)

**Status note:** this document is an architecture and build plan, not a finished app. There's no working code, no tests, no UI, and no deployment target yet. Treat every phase below as "locally tested and understood" before calling it done — that's the actual bar, not just "the service runs."

---

## 1. System role and collaboration protocol

You are acting as a Principal Systems Architect and Code Reviewer helping me build the MedFlow Ecosystem from scratch.

**Learning first**
- Don't generate full, multi-file codebases automatically.
- Explain architectural concepts, design patterns, and database contracts before writing code.
- When we write code, walk through it step by step so I understand every line and can build without AI dependency.

**No AI crutches**
- Enforce schema-first API contracts.
- Keep database isolation strict — no service touches another service's tables.
- Maintain modular layering and real error handling, not try/except pass.

**Review mode**
- When I submit code or schema designs, check for race conditions, GIL-blocking mistakes, transaction deadlocks, and security gaps before approving.
- If I reach for a concurrency pattern (threads, processes, async) without a measured reason, ask me to justify it before we build on top of it.

---

## 2. The 7 bounded contexts

No service queries another service's database directly. All cross-service communication goes through REST APIs or the event bus.

| # | Service | Database | Core responsibility | Concurrency pattern |
|---|---|---|---|---|
| 1 | Auth and RBAC | db_auth | Identity, JWT issuance, roles, permissions | RSA public-key verification, decentralized across services |
| 2 | Appointments | db_appts | Doctor schedules, booking, cancellations, check-in | `SELECT FOR UPDATE` row locking to prevent double-booking |
| 3 | EHR and Encounters | db_ehr | Patient demographics, encounter notes, e-prescribing | Redis caching for reads; JSONB for unstructured notes |
| 4 | Triage and Risk | db_triage | Vitals ingestion, NEWS2 scoring, emergency alerts | Synchronous or async calculation in-process (see note below) |
| 5 | Pharmacy and Stock | db_pharmacy | Inventory batches, expiration tracking, dispense logs | Event-driven FIFO deduction, atomic locks, audit trail |
| 6 | Lab System (LIS) | db_lis | Test orders, result ingestion via webhooks | `asyncio` or `ThreadPoolExecutor` for polling external feeds |
| 7 | Billing and RCM | db_billing | ICD-10/CPT coding, invoicing, claim validation | Async background worker for denial-risk prediction |

**Note on NEWS2 scoring:** this is a weighted sum over a handful of vital-sign bands — it runs in microseconds. Don't reach for `ProcessPoolExecutor` here by default; it adds serialization and process-spawn overhead for no benefit. Run it synchronously, or as a plain async function on the request path. If you're ever batch-scoring thousands of patients at once and profiling shows it's actually the bottleneck, that's the point to reconsider — not before.

**Note on billing anomaly prediction:** this one might legitimately be CPU-heavy, if there's a real model doing inference. Start with an async background worker. Move to `ProcessPoolExecutor` only if profiling shows the model call is blocking the event loop.

---

## 3. Core architectural principles

### Concurrency rules

- **I/O-bound work** (REST traffic, database queries, polling external feeds): `async def` endpoints, `asyncio`, or `ThreadPoolExecutor` for blocking legacy drivers.
- **CPU-bound work**: only offload to `ProcessPoolExecutor` after profiling shows it's needed. Default to running it in-process. Multiprocessing adds real cost — separate memory space, serialization across the process boundary — and that cost isn't automatically worth paying.

### Event-driven FIFO stock deduction

When a doctor signs a prescription in EHR, it does not call Pharmacy synchronously. Instead:

1. EHR writes a `prescription_created` event to an outbox table, in the same transaction as the prescription write.
2. A background publisher pushes the event to Redis Streams.
3. The Pharmacy consumer opens a transaction in `db_pharmacy`, locks the oldest active batch with `SELECT ... FOR UPDATE` (FIFO by expiration), deducts stock, and writes an immutable entry to `medication_dispense_logs`.

### Transactional outbox pattern

Services never publish directly to Redis inside an HTTP route handler — that's how you get a database commit that succeeds while the message never goes out. Events go into an `outbox_events` table inside the same ACID transaction as the business logic that produced them.

### Audit query requirement

Pharmacy's schema needs to support a query that reconstructs the full history of any medication dispensed to a given patient across all visits — batch numbers, timestamps, and the staff member who dispensed it. This is a read path, not an afterthought; design the indexes for it up front.

### Tracing and deletes

- Every request and event carries an `X-Correlation-ID` header.
- No hard `DELETE` on clinical or inventory records. Use `is_deleted` flags and append-only ledgers.

---

## 4. Operational patient journey

Integration testing validates this lifecycle end to end:

1. **Booking** — patient books a slot through Appointments; row locks prevent double-booking.
2. **Check-in and triage** — front desk marks `CHECKED_IN`; a nurse submits vitals; NEWS2 score is calculated and flags the doctor's dashboard if critical.
3. **Encounter** — doctor records findings in EHR, orders labs through LIS, prescribes medication.
4. **Fulfillment** — the prescription event triggers Pharmacy's FIFO deduction and dispense log.
5. **Revenue cycle** — Billing listens for encounter and dispensing events, maps ICD-10/CPT codes, checks for claim anomalies, generates an invoice.

---

## 5. Build roadmap

Eight phases. Each one should be locally tested and something you can explain line by line before moving to the next — that's the actual goal here, not just having seven services running.

### Phase 1: Foundation — Auth, Docker, and one working service

- Docker Compose with PostgreSQL, Redis, PgAdmin.
- SQL init script provisioning all 7 databases (they can exist empty — you're not building all 7 services yet).
- Auth and RBAC: JWT generation, bcrypt hashing, models for Users, Roles, Permissions (`inventory:dispense`, `encounters:write`, etc).
- Shared middleware dependency for decoding and validating JWT permissions.

### Phase 2: Core clinical flow, no event bus yet

- Appointments: CRUD plus `SELECT FOR UPDATE` locking.
- EHR and Encounters: demographics, Redis caching, JSONB note schemas.
- At this point you have three services talking to Auth and to each other only through REST. Get comfortable with that before adding async messaging.

### Phase 3: The event bus, end to end, on one pair of services

- Build the outbox pattern and Redis Streams publisher, connected to EHR.
- Build Pharmacy and Stock: inventory batches, the FIFO consumer, dispense audit logging.
- This is the phase to deliberately break things — kill the publisher mid-run, duplicate an event, see what happens to the lock. That's where the real learning is.

### Phase 4: Remaining services

- Triage and Risk: NEWS2 scoring (in-process, per the note in section 2).
- LIS: webhook ingestion for lab results.
- Billing and RCM: event consumers for ICD-10/CPT mapping, async denial-risk worker.

### Phase 5: Security, compliance, and platform concerns

This isn't a bullet list at the end — treat it as real build work if there's any chance real patient data touches this system.

- Encryption at rest for `db_ehr`, `db_triage`, `db_pharmacy`.
- Access logging that can survive an actual audit (who read what, when).
- Centralized observability: logs, metrics, traces, alerting.
- API gateway: rate limiting, policy enforcement, correlation ID propagation.
- Secrets management and key rotation.
- Backup, restore, and disaster recovery plan — tested, not just documented.
- CI/CD with migration safety checks and contract testing between services.
- A written mapping from each control above to the specific HIPAA requirement it satisfies. "HIPAA-style controls" isn't a real compliance posture — if this ever handles real PHI, this section needs a lawyer, not just an architecture doc.

### Phase 6: Gateway and BFF

- Build the gateway service described in section 6: single auth entry point, request aggregation across services, rate limiting, correlation ID propagation.
- This is also where API versioning gets decided, before any UI depends on a specific shape.

### Phase 7: UI, one role at a time

- Start with the front desk and doctor views — booking and encounter recording — since those exercise Appointments and EHR, already built and tested by this point.
- Add the nurse triage view with the websocket/SSE alert path once Triage is live.
- Add pharmacist and billing views last; they depend on the event-driven services from Phases 3 and 4.
- Resist building all five role views in parallel. Ship one, use it against real (test) data, then move to the next.

### Phase 8: Testing and deployment

- Integration tests that intentionally break things: kill the outbox publisher mid-transaction, duplicate an event, force a lock timeout on the same appointment slot from two requests at once.
- Decide a deployment target before writing CI/CD — the shape of Phase 5's secrets management and backup plan depends on whether this runs on a single box, Kubernetes, or a managed platform.
- Contract tests between services, so a schema change in Pharmacy doesn't silently break Billing's event consumer.

---

## 6. UI architecture

This system serves five distinct jobs — front desk, nurse, doctor, pharmacist, billing clerk — not one generic user. Design for that split from the start rather than retrofitting roles onto a single dashboard later.

**Gateway / BFF layer**

Before any UI work, put a thin backend-for-frontend service in front of the seven microservices. It should own:

- The single auth handshake the UI talks to (rather than seven).
- Request aggregation — a "patient chart" view needs data from EHR, Triage, and Pharmacy; the UI shouldn't make three round trips and stitch them together client-side.
- Rate limiting and correlation ID propagation at the edge.

**Frontend**

- One React codebase, role-based routing enforced server-side by the same RBAC permissions already in Auth — not just hidden UI elements. A stolen nurse token should never be able to render the billing view, regardless of what the client-side router does.
- Websockets or server-sent events for the triage alert path specifically. A critical NEWS2 score needs to reach the doctor's dashboard immediately, not on the next poll. This is the one place in the system where real-time actually matters; everywhere else, a normal REST fetch is fine.
- Forms-first design. This is clinical data entry, often under time pressure. Prioritize keyboard navigation, high contrast, and large touch targets over visual polish. A nurse entering vitals mid-crisis is not the audience for a clever dropdown.
- Every UI action that writes data should show which permission it required and log against the same `X-Correlation-ID` used on the backend — makes debugging a support ticket ("why couldn't I dispense this medication") much faster.

---

## 7. Startup instruction

To start a session, acknowledge this specification, then ask whether to begin with the Docker Compose seven-database init script or the Pydantic v2 schemas and SQLAlchemy models for Phase 1 (Auth and RBAC).
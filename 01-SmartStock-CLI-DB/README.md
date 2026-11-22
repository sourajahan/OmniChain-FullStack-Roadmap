<div align="center">

<br/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://capsule-render.vercel.app/api?type=transparent&height=120&section=header&text=SmartStock%20CLI%20%26%20DB&fontSize=48&fontColor=F8FAFC&fontAlignY=42&desc=Module%2001%20%2F%2006%20%E2%80%94%20Foundations%2C%20Python%20Engineering%20%26%20Relational%20Commerce%20DB&descAlignY=75&descSize=16&descColor=38BDF8" />
  <img alt="SmartStock CLI & DB" src="https://capsule-render.vercel.app/api?type=transparent&height=120&section=header&text=SmartStock%20CLI%20%26%20DB&fontSize=48&fontColor=0F172A&fontAlignY=42&desc=Module%2001%20%2F%2006%20%E2%80%94%20Foundations%2C%20Python%20Engineering%20%26%20Relational%20Commerce%20DB&descAlignY=75&descSize=16&descColor=0284C7" />
</picture>

<p>
  <a href="../README.md"><img src="https://img.shields.io/badge/⬅_OmniChain-Master_Blueprint-0F172A?style=flat-square&logo=github&logoColor=white" /></a>
  <img src="https://img.shields.io/badge/Part_I-Technical_Foundations-0284C7?style=flat-square" />
  <img src="https://img.shields.io/badge/Part_II-2_Python_Apps_%2B_PostgreSQL-064E3B?style=flat-square" />
</p>

<p>
  <img src="https://skillicons.dev/icons?i=linux,git,github,py,postgres,postman&perline=6" />
</p>

<br/>
</div>

---

# Part I: Core Engineering Foundations (Concepts & Real-World Usage)

## 1. Terminal & Linux Operations
* **Filesystem Navigation & Manipulation (`cd`, `ls`, `cp`, `mv`, `rm`):** Moving across directory trees (`cd`), inspecting permissions and hidden files (`ls -la`), duplicating configs (`cp`), renaming/relocating artifacts (`mv`), and safely purging build caches (`rm -rf`).
* **Stream Filtering & Pipelines (`grep`, `|`):** Chaining standard output (`stdout`) of one command into another (`|`) to isolate critical runtime errors or specific HTTP status codes from massive server logs (`cat app.log | grep "ERROR"`).
* **Access Control (`chmod`, `permissions`):** Enforcing Unix read/write/execute (`rwx`) boundaries for owner, group, and public users (e.g., `chmod +x scripts/deploy.sh` or `chmod 600 .env`) to prevent unauthorized script execution or credential leaks.
* **Environment Variables (`export`, `.env`):** Decoupling sensitive configuration (database URLs, API secrets) from source code into OS-level runtime memory (`os.getenv`), ensuring zero hardcoded secrets in version control.

---

## 2. Git & GitHub Version Control
* **Local Lifecycle (`init`, `add`, `commit`):** Initializing tracked repositories (`git init`), staging exact changesets (`git add`), and recording atomic, descriptive snapshots (`git commit -m "feat: ..."`).
* **Branching & Integration (`branch`, `merge`):** Isolating parallel feature development (`git checkout -b feature/db-lock`) away from production `main`, then integrating verified work back (`git merge`).
* **Conflict Resolution (`merge conflicts`):** Manually reconciling overlapping line edits across branches by inspecting `<<<<<<<`, `=======`, and `>>>>>>>` markers and preserving valid business logic.
* **Collaboration & Hygiene (`Pull Request`, `.gitignore`):** Reviewing diffs before merging via GitHub Pull Requests, while excluding virtual environments (`venv/`), secrets (`.env`), and OS artifacts (`.DS_Store`) via `.gitignore`.

---

## 3. Python Core Fundamentals
* **Static Typing & Variables (`type`, `variable`):** Binding memory references with explicit type hints (`sku: str`, `price: Decimal`, `qty: int`) to catch type mismatches early and enforce self-documenting code.
* **Control Flow (`if`, `for`, `while`):** Guarding business invariants with conditional branches (`if/elif/else`), iterating over database cursors (`for`), and driving interactive CLI event loops (`while`).
* **Modular Functions (`def`, `*args`, `**kwargs`):** Encapsulating single-responsibility business logic into pure, reusable functions with clear input/output contracts.
* **Built-in Data Structures (`list`, `dict`, `set`):** Selecting optimal structures for algorithmic efficiency—ordered sequences (`list`), $O(1)$ hash-map SKU lookups (`dict`), and deduplicated tag/category collections (`set`).

---

## 4. Practical Python Engineering
* **File I/O & Serialization (`open`, `json`):** Reading and writing structured audit logs, inventory snapshots, and configuration payloads safely using context managers (`with open(...)`) and `json.load` / `json.dump`.
* **Exception Handling (`try/except/raise`):** Designing a custom domain exception hierarchy (`OutOfStockError`, `InvalidSKUError`) to fail gracefully and trigger database rollbacks instead of unhandled crashes.
* **Object-Oriented Design (`OOP`, `@dataclass`):** Modeling real-world entities (`Product`, `Order`, `OrderItem`) with clean encapsulation, immutability (`frozen=True`), and auto-generated boilerplate via `@dataclass`.
* **Environment Isolation & Testing (`venv`, `pip`, `pytest`):** Pinning deterministic dependencies inside isolated virtual environments (`venv` + `requirements.txt`) and verifying edge cases with automated `pytest` suites.

---

## 5. SQL & PostgreSQL Relational Engine
* **Querying & Filtering (`SELECT`, `WHERE`):** Projecting specific columns and filtering rows using indexed predicates (`=`, `IN`, `BETWEEN`, `ILIKE`).
* **Relational Joins & Aggregations (`JOIN`, `GROUP BY`):** Reconstructing normalized multi-table relationships (`INNER JOIN`, `LEFT JOIN`) and computing business KPIs (`SUM`, `COUNT`, `AVG`) grouped by category or date.
* **Integrity Constraints & Indexing (`constraint`, `index`):** Enforcing data validity at the storage engine level (`PRIMARY KEY`, `FOREIGN KEY`, `UNIQUE`, `CHECK (stock >= 0)`) and accelerating read paths with `B-Tree` indexes.
* **ACID Transactions & Query Profiling (`transaction`, `EXPLAIN`):** Guaranteeing all-or-nothing execution (`BEGIN`, `COMMIT`, `ROLLBACK`) with pessimistic row locking (`SELECT ... FOR UPDATE`) to prevent overselling, while auditing index scans via `EXPLAIN ANALYZE`.

---

## 6. HTTP & RESTful Web Architecture
* **Protocol Semantics (`method`, `status code`):** Mapping CRUD operations to idempotent/safe HTTP verbs (`GET`, `POST`, `PUT`, `PATCH`, `DELETE`) and returning accurate status codes (`200 OK`, `201 Created`, `400 Bad Request`, `404 Not Found`, `409 Conflict`).
* **Metadata & State (`header`, `cookie`):** Passing content negotiation (`Content-Type: application/json`), authorization tokens (`Authorization: Bearer ...`), and session state via HTTP headers and secure `HttpOnly` cookies.
* **Stateless APIs & Cross-Origin Security (`REST`, `CORS`):** Designing resource-oriented endpoints (`/api/v1/products/{id}`) and configuring Cross-Origin Resource Sharing (`Access-Control-Allow-Origin`) for browser clients.
* **API Verification (`Postman`):** Constructing automated request collections, environment variables, and assertion scripts in Postman to validate payloads, headers, and error responses.

---

# Part II: Production Deliverables (2 Python Projects + Store Database)

| Deliverable | Architecture & Purpose | Applied Stack |
| :--- | :--- | :--- |
| **01. Store Relational Database (`store_db`)** | Normalized 3NF PostgreSQL schema (`products`, `customers`, `orders`, `order_items`) enforcing `CHECK (stock >= 0)`, composite `B-Tree` indexes, `EXPLAIN ANALYZE` reports, and `ACID` row-locking. | `PostgreSQL` • `SQL` • `ACID` • `Indexes` |
| **02. Project 1: SmartStock CLI Engine** | Object-oriented Python CLI application (`@dataclass`, custom exceptions, `JSON` export/import, `dict/set` $O(1)$ indexing) executing concurrent-safe stock deductions and sales analytics directly against `store_db`. | `Python OOP` • `Psycopg2` • `JSON` • `Pytest` |
| **03. Project 2: SmartStock REST Gateway** | Lightweight HTTP/REST service exposing `store_db` over JSON endpoints (`GET /products`, `POST /orders`, `GET /reports/sales`) with proper HTTP status codes, headers, `CORS`, and a complete `Postman` test collection. | `Python HTTP/REST` • `JSON` • `CORS` • `Postman` |

---

<div align="center">
  <sub>Module 01 of the <a href="../README.md">OmniChain Enterprise Platform</a> • Engineered by <a href="https://github.com/sourajahan">Soura</a></sub>
</div>

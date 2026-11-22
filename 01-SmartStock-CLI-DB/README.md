 <div align="center">

<!-- Reliable Vibrant Gradient Header Banner -->
<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1E1B4B,35:1D4ED8,70:0284C7,100:059669&height=200&section=header&text=SmartStock%20CLI%20%26%20DB&fontSize=44&fontColor=FFFFFF&animation=fadeIn&fontAlignY=38&desc=Module%2001%20%2F%2006%20%E2%80%94%20Systems%20Foundations%2C%20Python%20Engineering%20%26%20Commerce%20DB&descAlignY=63&descSize=15&descColor=BAE6FD" width="100%" />

<!-- Live Typing Animation -->
<a href="../README.md">
  <img src="https://readme-typing-svg.demolab.com?font=JetBrains+Mono&weight=700&size=18&duration=2600&pause=800&color=38BDF8&center=true&vCenter=true&width=820&lines=01.+Linux+%26+Git+%E2%80%A2+02.+Python+Core+%26+OOP+%E2%80%A2+03.+PostgreSQL+ACID+%26+REST;2+Complete+Python+Applications+%2B+Normalized+Store+Database;Zero-Overselling+Concurrency+Control+with+Row-Level+Locking" alt="Typing SVG" />
</a>

<br/>

<!-- Colorful Navigation Badges -->
<p>
  <a href="../README.md"><img src="https://img.shields.io/badge/⬅_Master-OmniChain_Core-0F172A?style=for-the-badge&logo=github&logoColor=white" /></a>
  <a href="#part-i-systems--engineering-foundations"><img src="https://img.shields.io/badge/Part_I-6_Engineering_Pillars-6366F1?style=for-the-badge" /></a>
  <a href="#part-ii-production-deliverables-architecture"><img src="https://img.shields.io/badge/Part_II-2_Python_Apps_%2B_DB-10B981?style=for-the-badge" /></a>
  <img src="https://img.shields.io/badge/Guarantee-ACID_%26_Zero_Overselling-F59E0B?style=for-the-badge" />
</p>

<!-- Tech Stack Icons -->
<p>
  <img src="https://skillicons.dev/icons?i=linux,git,github,py,postgres,postman&perline=6" />
</p>

</div>

---

## 🎯 Executive Summary & Architectural Role

**SmartStock-CLI-DB** is the foundational transactional layer of the **OmniChain Enterprise Platform**. Before introducing web frameworks, caches, or distributed brokers, a commerce system must guarantee **data integrity, concurrency safety, and clean domain boundaries** at the operating system, language, and relational storage layers.

* 🟦 **Part I (Engineering Foundations):** Deep breakdown of the six core disciplines—from Linux process streams and Git workflows to Python memory structures, PostgreSQL ACID row-locking, and stateless HTTP/REST contracts.
* 🟩 **Part II (Production Deliverables):** Three integrated engineering artifacts—a **3NF PostgreSQL Store Database**, an **Object-Oriented CLI Inventory & Flash-Sale Engine**, and a **Zero-Dependency REST API Gateway** verified via Postman.

---

# Part I: Systems & Engineering Foundations

### 🟨 01. Linux Kernel Space, Shell & Process Hygiene
![Linux](https://img.shields.io/badge/Linux_Shell-FCC624?style=flat-square&logo=linux&logoColor=black) ![Bash](https://img.shields.io/badge/Bash_Pipes-4EAA25?style=flat-square&logo=gnubash&logoColor=white) ![Security](https://img.shields.io/badge/Env_Isolation-EF4444?style=flat-square)

| Primitive | Engineering Mechanism | Production Application in SmartStock |
| :--- | :--- | :--- |
| **`cd, ls, cp, mv, rm`** | Direct inode traversal and filesystem tree manipulation (`ls -la` for hidden dotfiles, `rm -rf` for deterministic cache purges). | Managing multi-package directory trees, rotating JSON backup snapshots, and cleaning `__pycache__` artifacts. |
| **`grep` & `\|` (Pipes)** | Unix stream redirection connecting `stdout` of one process directly to `stdin` of another in memory without temporary disk writes. | Real-time log forensics: `cat logs/audit.log \| grep "ROLLBACK" \| wc -l` to isolate failed concurrent transactions. |
| **`chmod` & Permissions** | Octal bitmask enforcement (`rwx` for `user/group/others`) controlling execution privileges and file confidentiality. | Hardening credential files (`chmod 600 .env`) and enabling automated test/bootstrap runners (`chmod +x scripts/setup.sh`). |
| **`Environment Variables`** | OS-level key-value injection (`export`, `.env` via `os.getenv`) separating runtime configuration from immutable source code. | Injecting `DB_HOST`, `DB_PASSWORD`, and `API_SECRET` at runtime so zero credentials ever enter Git history. |

---

### 🟧 02. Distributed Version Control (Git & GitHub Flow)
![Git](https://img.shields.io/badge/Git-F05032?style=flat-square&logo=git&logoColor=white) ![GitHub](https://img.shields.io/badge/GitHub_PRs-181717?style=flat-square&logo=github&logoColor=white) ![Workflow](https://img.shields.io/badge/Feature_Branching-8B5CF6?style=flat-square)

| Primitive | Engineering Mechanism | Production Application in SmartStock |
| :--- | :--- | :--- |
| **`init, add, commit`** | Content-addressable SHA-1 object graph tracking atomic repository snapshots via staging index (`git add -p`). | Recording granular, self-contained engineering milestones using Conventional Commits (`feat:`, `fix:`, `perf:`, `test:`). |
| **`branch` & `merge`** | Lightweight pointer isolation allowing parallel feature development without destabilizing the `main` release branch. | Isolating database schema migrations (`feat/pg-row-lock`) and REST endpoints (`feat/http-gateway`) prior to integration. |
| **`Conflict Resolution`** | Deterministic reconciliation of overlapping AST/line mutations between `HEAD` and incoming branch pointers (`<<<<<<<` / `>>>>>>>`). | Resolving concurrent schema or model modifications cleanly while preserving all unit test assertions. |
| **`Pull Request` & `.gitignore`** | Peer-level diff auditing before branch integration, paired with path exclusion rules preventing binary/secret pollution. | Excluding `venv/`, `.env`, `.DS_Store`, and `.pytest_cache/` while documenting architectural changes in PR descriptions. |

---

### 🟦 03. Python Core: Type Systems, Control Flow & Complexity
![Python](https://img.shields.io/badge/Python_3.12+-3776AB?style=flat-square&logo=python&logoColor=white) ![Typing](https://img.shields.io/badge/Static_Typing-0284C7?style=flat-square) ![Big-O](https://img.shields.io/badge/O(1)_Lookups-10B981?style=flat-square)

| Primitive | Engineering Mechanism | Production Application in SmartStock |
| :--- | :--- | :--- |
| **`type` & `variable`** | Explicit static type annotations (`sku: str`, `unit_price: Decimal`, `qty: int`) enforcing self-documenting contracts and IDE static analysis. | Eliminating floating-point currency rounding bugs by enforcing `decimal.Decimal` across all ledger calculations. |
| **`if, for, while`** | Deterministic branching guards, iterator protocol traversal over database cursors, and state-machine event loops. | Validating stock thresholds (`if qty <= 0`), streaming batch exports (`for row in cursor`), and driving the interactive CLI loop (`while`). |
| **`function`** | Pure, single-responsibility callables with explicit input/output signatures and zero hidden global state mutations. | Decoupling tax/discount calculation engines and SQL query builders into composable, unit-testable units. |
| **`list, dict, set`** | Asymptotic data structure selection: contiguous arrays (`list`), $O(1)$ hash-table indexing (`dict`), and hash-deduplicated collections (`set`). | Indexing in-memory product catalogs by `SKU` in `dict[str, Product]` for $O(1)$ lookup speed and deduplicating category tags with `set`. |

---

### 🟪 04. Practical Python: Domain Modeling, Persistence & Verification
![OOP](https://img.shields.io/badge/OOP_%26_Dataclasses-7C3AED?style=flat-square) ![JSON](https://img.shields.io/badge/JSON_%26_File_I%2FO-F59E0B?style=flat-square) ![Pytest](https://img.shields.io/badge/Pytest_Verified-0A9EDC?style=flat-square&logo=pytest&logoColor=white)

| Primitive | Engineering Mechanism | Production Application in SmartStock |
| :--- | :--- | :--- |
| **`file` & `JSON`** | Context-managed I/O streams (`with open(...)`) and structured serialization (`json.dumps` / `json.loads`) with custom encoders. | Exporting daily warehouse audit trails to `.json` and ingesting bulk supplier catalog updates safely. |
| **`exception`** | Hierarchical error propagation (`try / except / else / finally`) allowing clean resource teardown and transactional rollbacks. | Raising domain-specific `OutOfStockError`, `DuplicateSKUError`, and `DatabaseConnectionError` mapped directly to HTTP status codes. |
| **`OOP` & `@dataclass`** | Encapsulated domain entities with immutable value semantics (`@dataclass(frozen=True)`) and clear behavioral methods. | Modeling `Product`, `Customer`, `Order`, and `OrderLine` as strictly typed domain objects separate from raw SQL tuples. |
| **`venv, pip, pytest`** | Hermetic dependency isolation per project (`venv` + `requirements.txt`) paired with fixture-driven automated verification (`pytest`). | Running isolated database rollback tests, concurrency simulations, and edge-case validation with `pytest -v`. |

---

### 🩵 05. SQL & PostgreSQL Relational Internals
![PostgreSQL](https://img.shields.io/badge/PostgreSQL_16-4169E1?style=flat-square&logo=postgresql&logoColor=white) ![ACID](https://img.shields.io/badge/ACID_Transactions-059669?style=flat-square) ![Indexing](https://img.shields.io/badge/B--Tree_%26_EXPLAIN-0EA5E9?style=flat-square)

| Primitive | Engineering Mechanism | Production Application in SmartStock |
| :--- | :--- | :--- |
| **`SELECT` & `WHERE`** | Relational projection and predicate filtering leveraging sargable expressions (`=`, `IN`, `BETWEEN`) over indexed columns. | Querying low-stock SKUs (`WHERE stock_qty <= reorder_threshold`) and filtering active customer orders by timestamp range. |
| **`JOIN` & `GROUP BY`** | Set-theoretic multi-table reconstruction (`INNER JOIN`, `LEFT JOIN`) and hash/sort aggregation (`SUM`, `COUNT`, `AVG`). | Generating executive revenue-by-category reports and identifying top-performing products across normalized tables. |
| **`constraint` & `index`** | Storage-level invariant enforcement (`PK`, `FK`, `UNIQUE`, `CHECK`) combined with `B-Tree` balanced search trees. | Enforcing `CHECK (stock_qty >= 0)` so negative inventory is physically impossible, and indexing `orders(customer_id, created_at)`. |
| **`transaction` & `EXPLAIN`** | All-or-nothing `ACID` execution (`BEGIN`, `COMMIT`, `ROLLBACK`) with pessimistic row locks (`FOR UPDATE`) and query plan telemetry. | Locking product rows during checkout to prevent flash-sale overselling, and auditing index scans via `EXPLAIN (ANALYZE, BUFFERS)`. |

---

### 🩷 06. HTTP Protocol & Stateless REST Architecture
![REST](https://img.shields.io/badge/RESTful_HTTP-EC4899?style=flat-square) ![CORS](https://img.shields.io/badge/CORS_Security-DC2626?style=flat-square) ![Postman](https://img.shields.io/badge/Postman_Collection-FF6C37?style=flat-square&logo=postman&logoColor=white)

| Primitive | Engineering Mechanism | Production Application in SmartStock |
| :--- | :--- | :--- |
| **`method` & `status code`** | Uniform interface mapping (`GET`, `POST`, `PATCH`, `DELETE`) paired with exact semantic response signaling (`200`, `201`, `400`, `404`, `409`). | Returning `201 Created` with `Location` header on order placement, and `409 Conflict` when `OutOfStockError` triggers. |
| **`header` & `cookie`** | Out-of-band metadata negotiation (`Content-Type`, `Authorization`, `X-Request-ID`) and stateful browser session tokens (`HttpOnly`, `Secure`). | Propagating correlation trace IDs (`X-Request-ID`) across logs and enforcing strict `application/json` payload contracts. |
| **`REST` & `CORS`** | Resource-oriented URI hierarchy (`/api/v1/products/{sku}`) and preflight cross-origin access governance (`OPTIONS` + `Access-Control-*`). | Exposing clean, stateless endpoints ready for browser storefronts while blocking unauthorized cross-origin requests. |
| **`Postman`** | Automated API test harnesses with environment variables, pre-request scripts, and JavaScript response schema assertions. | Maintaining an executable Postman collection verifying happy paths, payload validation errors, and `409` stock conflicts. |

---

# Part II: Production Deliverables Architecture

```text
  ┌────────────────────────────────────────────────────────────────────────────────────────┐
  │                        DELIVERABLE 03: SmartStock REST Gateway                         │
  │   • Stateless HTTP/REST Server (GET /products, POST /orders, GET /analytics/revenue)   │
  │   • Semantic Status Codes (200, 201, 400, 404, 409) • Headers • CORS • Postman Suite   │
  └───────────────────────────────────────────┬────────────────────────────────────────────┘
                                              │ Shared Domain & Transaction Engine
  ┌───────────────────────────────────────────▼────────────────────────────────────────────┐
  │                        DELIVERABLE 02: SmartStock CLI Engine                           │
  │   • Interactive Operations Terminal (Stock Intake, Flash-Sale Checkout, JSON Audit)    │
  │   • Typed @dataclass Models • O(1) dict/set SKU Cache • Custom Exception Hierarchy     │
  └───────────────────────────────────────────┬────────────────────────────────────────────┘
                                              │ Psycopg2 ACID Connection & FOR UPDATE
  ┌───────────────────────────────────────────▼────────────────────────────────────────────┐
  │                     DELIVERABLE 01: Store Relational Database                          │
  │   • 3NF PostgreSQL Schema: categories, products, customers, orders, order_items        │
  │   • Hard Constraints (CHECK stock_qty >= 0) • Composite B-Tree Indexes • EXPLAIN Plans │
  └────────────────────────────────────────────────────────────────────────────────────────┘

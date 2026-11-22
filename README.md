 <div align="center">

<img src="https://capsule-render.vercel.app/api?type=rect&color=0:090D16,100:131C31&height=170&section=header&text=OmniChain%20Core&fontSize=50&fontColor=38BDF8&fontAlignY=42&desc=Enterprise%20Commerce%20%26%20Supply%20Chain%20Engine%20%7C%206%2B1%20Roadmap&descAlignY=68&descSize=16&descColor=94A3B8" width="100%" />

<br/>

<p align="center">
  <img src="https://img.shields.io/badge/Core_Stack-Python_%E2%80%A2_PostgreSQL_%E2%80%A2_FastAPI_%E2%80%A2_React-0F172A?style=for-the-badge&logo=python&logoColor=38BDF8" />
  <img src="https://img.shields.io/badge/Cloud_%26_Scale-Docker_%E2%80%A2_Redis_%E2%80%A2_AWS_%E2%80%A2_Kafka_%E2%80%A2_K8s-0F172A?style=for-the-badge&logo=kubernetes&logoColor=38BDF8" />
  <img src="https://img.shields.io/badge/Quality-ACID_%E2%80%A2_OWASP_%E2%80%A2_%3E70%25_Coverage-0F172A?style=for-the-badge&logo=pytest&logoColor=10B981" />
</p>

</div>

---

## 🎯 The Engineering Mission

**OmniChain Core** is a production-grade Commerce & Supply Chain platform designed to solve four core distributed systems challenges:
* **Zero-Overselling Guarantee:** Atomic row-level locking in PostgreSQL during flash sales.
* **Sub-Millisecond Discovery:** Redis caching and semantic AI vector search across massive catalogs.
* **Zero-Trust Security:** Stateless JWT auth, strict RBAC, rate limiting, and OWASP Top 10 protection.
* **Fault-Tolerant Async Workers:** Decoupling payments and notifications via event queues under heavy traffic.

---

## 🏛️ System Architecture Blueprint

<div align="center">
  <img src="./architecture.jpeg" alt="OmniChain System Architecture" width="100%" />
</div>

---

## 📦 Engineering Curriculum & Modules (1 to 6)

<details open>
<summary><strong>01. SmartStock-CLI-DB — Foundations, Python & Relational Databases (Month 1)</strong></summary>
<br/>

* **Repository:** [`SmartStock-CLI-DB`](https://github.com/sourajahan/SmartStock-CLI-DB)
* **Linux & Shell:** `cd, ls, cp, mv, rm`, `grep` & `pipe`, `chmod` & `permissions`, `environment variables`.
* **Git & GitHub:** `init, add, commit`, `branch` & `merge`, `conflict` resolution, `Pull Request` & `.gitignore`.
* **Python Core:** `type` & `variable`, `if, for, while`, `function`, `list, dict, set`.
* **Practical Python:** `file` & `JSON`, `exception`, `OOP` & `dataclass`, `venv, pip, pytest`.
* **SQL & PostgreSQL:** `SELECT` & `WHERE`, `JOIN` & `GROUP BY`, `constraint` & `index`, `transaction` & `EXPLAIN`.
* **HTTP & REST:** `method` & `status code`, `header` & `cookie`, `REST` & `CORS`, `Postman`.
</details>

<details>
<summary><strong>02. CoreAuth-Order-API — Backend Engineering, Security & ORM (Month 2)</strong></summary>
<br/>

* **Repository:** `CoreAuth-Order-API`
* **Flask Core:** `route, blueprint`, `JSON`, `application factory`, `config`.
* **Database & ORM:** `SQLAlchemy`, `relationships`, `Alembic migration`, solving the `N+1` problem.
* **Auth & Security:** `password hashing`, `session vs JWT`, `refresh token`, `RBAC`.
* **Validation & Error:** `pydantic/marshmallow`, `error handler`, `status code`, `logging`.
* **Testing:** `pytest fixture`, `test database`, `API tests`, `coverage > 70%`.
* **FastAPI:** `async`, `Swagger/OpenAPI`, `dependency injection`.
</details>

<details>
<summary><strong>03. OmniStore-Frontend-Portal — Type-Safe React & Modern UI (Month 3)</strong></summary>
<br/>

* **Repository:** `OmniStore-Frontend-Portal`
* **HTML & CSS:** `semantic HTML`, `Flexbox, Grid`, `responsive`, `accessibility`.
* **JavaScript:** `closure, scope`, `array methods`, `DOM, event`, `fetch, async/await`.
* **TypeScript:** `type, interface`, `generic`, `tsconfig`, typing API responses.
* **React:** `component, props`, `state, useEffect`, `custom hook`, `Router, form`.
* **Data & UI:** `TanStack Query`, `Tailwind CSS`, `token` login, `loading/error` states.
</details>

<details>
<summary><strong>04. SearchMedia-DevOps-Engine — Caching, Containers & CI/CD (Month 4)</strong></summary>
<br/>

* **Repository:** `SearchMedia-DevOps-Engine`
* **Backend:** `pagination`, `search`, `file upload`, `API tests`.
* **Frontend:** `routing`, `validation`, `state management`, `component test`.
* **DevOps:** `Dockerfile, docker-compose`, `GitHub Actions`, `pre-commit, lint`.
* **Quality & Scale:** `code review`, `refactor`, `Redis cache`, `ADR`.
</details>

<details>
<summary><strong>05. CloudShield-Production-Gateway — Cloud Infrastructure & Security (Month 5)</strong></summary>
<br/>

* **Repository:** `CloudShield-Production-Gateway`
* **Deployment:** Cloud hosting (`Render/Railway/AWS`), managed DB, `HTTPS`, `log` & `backup`.
* **Security & Scale:** `OWASP Top 10`, `rate limiting`, `CDN`, `secrets management`.
* **Portfolio:** English `README`, demo video, architecture diagram, pinned repos.
</details>

<details>
<summary><strong>06. AsyncQueue-Notifier-Service — Distributed Queues & High Availability (Month 6)</strong></summary>
<br/>

* **Repository:** `AsyncQueue-Notifier-Service`
* **System Design:** `load balancer`, `caching`, `DB replication`, `queue`, `URL shortener`.
* **Integrations:** External Payment/SMS APIs with fault tolerance and retries.
</details>

<details>
<summary><strong>07 & 08. OmniChain-Enterprise-Platform — Capstone & Hyperscale</strong></summary>
<br/>

* **Project 7:** Unified microservices ecosystem orchestrated via `Docker Compose` and `API Gateway`.
* **Phase 8 (Hyperscale):** `Apache Kafka`, `Kubernetes (K8s)`, `Elasticsearch + AI Vector Search`, `Saga Pattern`, `Prometheus & Grafana`.
</details>

---

## 📊 Live Progress Tracker

| Step | Module | Repository | Core Stack | Status |
| :--- | :--- | :--- | :--- | :--- |
| **01** | Core Inventory & DB | [`SmartStock-CLI-DB`](https://github.com/sourajahan/SmartStock-CLI-DB) | `Linux` `Git` `Python` `PostgreSQL` | 🟡 **Active** |
| **02** | Auth & Order API | `CoreAuth-Order-API` | `Flask` `FastAPI` `SQLAlchemy` `JWT` | ⚪ Planned |
| **03** | Storefront & Admin UI | `OmniStore-Frontend-Portal` | `React` `TypeScript` `Tailwind` | ⚪ Planned |
| **04** | Search, Cache & DevOps | `SearchMedia-DevOps-Engine` | `Redis` `Docker` `GitHub Actions` | ⚪ Planned |
| **05** | Cloud & Security | `CloudShield-Production-Gateway` | `AWS` `HTTPS` `OWASP` `CDN` | ⚪ Planned |
| **06** | Async Queue & Scale | `AsyncQueue-Notifier-Service` | `Queue` `Load Balancer` `APIs` | ⚪ Planned |
| **07** | **Unified Platform** | `OmniChain-Enterprise-Platform` | `Microservices` `Kafka` `K8s` `AI Search` | 🎯 **Capstone** |

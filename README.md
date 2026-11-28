<div align="center">
  <img src="./.github/assets/banner.svg" alt="OmniChain Enterprise Platform" width="100%" />

  <h1>⚡ OmniChain — Full-Stack &amp; Hyperscale Enterprise Roadmap</h1>
  <p>
    <strong>From ACID inventory engines to Multi-Region Kubernetes, Apache Kafka, AI Vector Search, and Distributed Sagas — built as 8 progressive, production-tested modules.</strong>
  </p>

  <p>
    <img src="./.github/assets/badges.svg" alt="Modules 8/8 | Release v2.0.0 | Hyperscale | GitHub Actions" width="760" />
  </p>

  <p>
    <a href="#-system-architecture">Architecture</a> •
    <a href="#-distributed-saga--compensation-flow">Saga Flow</a> •
    <a href="#-roadmap-modules-0108">Modules (01–08)</a> •
    <a href="#-tech-stack">Tech Stack</a> •
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-architecture-decision-records-adrs">ADRs</a>
  </p>

  <br/>
  <img src="./.github/assets/highlights.svg" alt="OmniChain Key Highlights" width="840" />
</div>

---

## 🏗️ System Architecture

```mermaid
flowchart TB
    subgraph EDGE["🌐 Edge, Portal & Security Layer"]
        direction LR
        Portal["03 OmniStore Portal<br/>React + TypeScript + Tailwind"]
        Shield["05 CloudShield Gateway<br/>TLS + Rate Limit + OWASP"]
        Portal --> Shield
    end

    subgraph CORE["⚙️ Core Commerce & Cloud Logistics"]
        direction LR
        Auth["02 CoreAuth & Order API<br/>FastAPI + JWT + RBAC"]
        Search["04 Search & Media Engine<br/>Redis Cache + DevOps"]
        Enterprise["07 OmniChain Enterprise Core<br/>Multi-Warehouse + Logistics"]
        Auth --> Enterprise
    end

    subgraph ASYNC["⚡ Async Messaging & Load Balancing"]
        direction LR
        LB["06 Nginx Load Balancer<br/>least_conn"]
        Queue["06 Async Queue & Workers<br/>Redis + Idempotency + DLQ"]
        LB --> Queue
    end

    subgraph HYPER["🚀 Hyperscale, AI & Multi-Region Platform"]
        direction LR
        Vector["08 AI Vector Search<br/>Cosine Similarity"]
        Saga["08 Distributed Saga<br/>Event Orchestrator"]
        Kafka[("Apache Kafka KRaft<br/>Event Backbone")]
        K8s["Kubernetes HPA + PDB<br/>eu-west-1 & us-east-1"]
        Obs["Observability Stack<br/>Prometheus + Grafana + OTel"]
        Vector --> K8s
        Saga --> Kafka
        Kafka --> Obs
    end

    Shield --> Auth
    Shield --> Search
    Shield --> LB
    Enterprise --> Saga
    Enterprise --> Vector

    classDef edge fill:#0EA5E9,stroke:#0284C7,color:#FFFFFF,stroke-width:2px;
    classDef core fill:#6366F1,stroke:#4338CA,color:#FFFFFF,stroke-width:2px;
    classDef async fill:#F59E0B,stroke:#D97706,color:#0F172A,stroke-width:2px;
    classDef hyper fill:#10B981,stroke:#047857,color:#FFFFFF,stroke-width:2px;
    classDef infra fill:#EC4899,stroke:#BE185D,color:#FFFFFF,stroke-width:2px;

    class Portal,Shield edge;
    class Auth,Search,Enterprise core;
    class LB,Queue async;
    class Vector,Saga,K8s hyper;
    class Kafka,Obs infra;
```

---

## 🔄 Distributed Saga & Compensation Flow

```mermaid
flowchart LR
    Req["🛒 Checkout Request<br/>Idempotency-Key"] --> Step1["1️⃣ Reserve Inventory<br/>Multi-Warehouse"]
    Step1 --> Step2["2️⃣ Authorize Payment<br/>Gateway Capture"]
    Step2 -->|Success| Step3["3️⃣ Dispatch Logistics<br/>TRK-... Generated"]
    Step3 --> Done["✅ Order CONFIRMED<br/>Kafka: SagaStepCompleted"]

    Step2 -->|Failure| Comp1["↩️ Compensate Stock<br/>Release Reservation"]
    Comp1 --> Rolled["⚠️ Order COMPENSATED<br/>Kafka: SagaStepCompensated"]

    classDef start fill:#3B82F6,stroke:#1D4ED8,color:#FFFFFF,stroke-width:2px;
    classDef step fill:#8B5CF6,stroke:#6D28D9,color:#FFFFFF,stroke-width:2px;
    classDef ok fill:#10B981,stroke:#047857,color:#FFFFFF,stroke-width:2px;
    classDef fail fill:#EF4444,stroke:#B91C1C,color:#FFFFFF,stroke-width:2px;

    class Req start;
    class Step1,Step2,Step3 step;
    class Done ok;
    class Comp1,Rolled fail;
```

---

## 📦 Roadmap Modules (01–08)

| # | Module | Key Engineering Capabilities | Stack | Status |
| :---: | :--- | :--- | :--- | :---: |
| **01** | [`01-SmartStock-CLI-DB`](./01-SmartStock-CLI-DB) | ACID inventory engine, relational schema, CLI workflows | Python, PostgreSQL/SQLite, Pytest | ✅ |
| **02** | [`02-CoreAuth-Order-API`](./02-CoreAuth-Order-API) | JWT authentication, RBAC guards, order lifecycle API | FastAPI, JWT, Pydantic | ✅ |
| **03** | [`03-OmniStore-Frontend-Portal`](./03-OmniStore-Frontend-Portal) | Storefront & admin dashboard, responsive UI | React, TypeScript, Tailwind CSS | ✅ |
| **04** | [`04-SearchMedia-DevOps-Engine`](./04-SearchMedia-DevOps-Engine) | Search & media service, Redis caching, CI/CD | FastAPI, Redis, Docker | ✅ |
| **05** | [`05-CloudShield-Production-Gateway`](./05-CloudShield-Production-Gateway) | Reverse proxy, HTTPS/TLS, rate limiting, OWASP headers | Nginx, TLS, Security | ✅ |
| **06** | [`06-AsyncQueue-LoadBalancer-Messenger`](./06-AsyncQueue-LoadBalancer-Messenger) | Idempotent producer, async worker retries, DLQ replay, LB | Redis, Nginx `least_conn`, FastAPI | ✅ |
| **07** | [`07-OmniChain-Enterprise-Core`](./07-OmniChain-Enterprise-Core) | Multi-warehouse stock, carrier routing, Saga-ready rollback | FastAPI, Event Bus, PostgreSQL | ✅ |
| **08** | [`08-Hyperscale-Enterprise-Platform`](./08-Hyperscale-Enterprise-Platform) | AI Vector Search, Distributed Saga, Kafka, K8s HPA, OTel | Kafka, K8s, Prometheus, Grafana | ✅ |

---

## 🛠️ Tech Stack

<div align="center">
  <img src="./.github/assets/tech-stack.svg" alt="OmniChain Tech Stack" width="820" />
</div>

---

## 🚀 Quick Start

<details>
<summary><strong>⚡ Launch Module 06 — Async Queue, DLQ &amp; Nginx Load Balancer</strong></summary>

```bash
cd 06-AsyncQueue-LoadBalancer-Messenger
docker compose up --build
# Load Balancer Health: http://localhost:8083/health
```
</details>

<details>
<summary><strong>🏢 Launch Module 07 — Enterprise Commerce &amp; Cloud Logistics Core</strong></summary>

```bash
cd 07-OmniChain-Enterprise-Core
docker compose up --build
# Enterprise Core Health: http://localhost:8004/health
```
</details>

<details>
<summary><strong>🌐 Launch Module 08 — Hyperscale AI Vector Search, Saga, Kafka &amp; Observability</strong></summary>

```bash
cd 08-Hyperscale-Enterprise-Platform
docker compose up --build
# EU Region: http://localhost:8005/health | US Region: http://localhost:8006/health
# Prometheus: http://localhost:9090 | Grafana: http://localhost:3001
```
</details>

---

## 📐 Architecture Decision Records (ADRs)

- [**ADR 0003** — Async Queue, Dead-Letter Queue & Load Balancing](./06-AsyncQueue-LoadBalancer-Messenger/docs/adr/0003-async-queue-dlq-and-load-balancing.md)
- [**ADR 0004** — Event-Driven Commerce & Cloud Logistics Orchestration](./07-OmniChain-Enterprise-Core/docs/adr/0004-enterprise-commerce-logistics-orchestration.md)
- [**ADR 0005** — Hyperscale Architecture: Kafka, AI Vector Search, Saga, K8s HPA & Multi-Region](./08-Hyperscale-Enterprise-Platform/docs/adr/0005-hyperscale-kafka-saga-vector-k8s-multiregion.md)

---

<div align="center">
  <sub>Crafted for the <strong>OmniChain FullStack &amp; Hyperscale Roadmap</strong> • Release <code>v2.0.0</code></sub>
</div>

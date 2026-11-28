<div align="center">
  <img src="./.github/assets/banner.svg" alt="OmniChain Enterprise Platform" width="100%" />

  <h1>OmniChain — Full-Stack & Hyperscale Enterprise Roadmap</h1>
  <p>
    <strong>An end-to-end, production-grade software engineering monorepo spanning 8 progressive modules — from ACID inventory engines to Multi-Region Kubernetes, Kafka, AI Vector Search, and Distributed Sagas.</strong>
  </p>

  <p>
    <a href="#-roadmap-modules-0108"><img src="[https://img.shields.io/badge/Modules-8%2F8%20Complete-10B981?style=for-the-badge](https://img.shields.io/badge/Modules-8%2F8%20Complete-10B981?style=for-the-badge)" alt="Modules 8/8" /></a>
    <a href="[https://github.com/sourajahan/OmniChain-FullStack-Roadmap/releases/tag/v2.0.0](https://github.com/sourajahan/OmniChain-FullStack-Roadmap/releases/tag/v2.0.0)"><img src="[https://img.shields.io/badge/Release-v2.0.0-0284C7?style=for-the-badge](https://img.shields.io/badge/Release-v2.0.0-0284C7?style=for-the-badge)" alt="Release v2.0.0" /></a>
    <img src="[https://img.shields.io/badge/Architecture-Event--Driven%20%26%20Hyperscale-6366F1?style=for-the-badge](https://img.shields.io/badge/Architecture-Event--Driven%20%26%20Hyperscale-6366F1?style=for-the-badge)" alt="Architecture" />
    <img src="[https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-1E293B?style=for-the-badge&logo=githubactions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-1E293B?style=for-the-badge&logo=githubactions)" alt="CI/CD" />
  </p>

  <p>
    <a href="#-architecture-overview">Architecture</a> •
    <a href="#-roadmap-modules-0108">Modules (01–08)</a> •
    <a href="#-tech-stack">Tech Stack</a> •
    <a href="#-quick-start">Quick Start</a> •
    <a href="#-architecture-decision-records-adrs">ADRs</a>
  </p>
</div>

---

## ✨ Why OmniChain?

Modern enterprise platforms demand more than isolated CRUD services. **OmniChain** demonstrates how to design, test, containerize, and scale a complete commerce and cloud logistics ecosystem with real-world engineering patterns:

- **Idempotency & Fault Isolation:** Deduplicated APIs (`Idempotency-Key`), Redis async queues, worker retries, and Dead-Letter Queues (DLQ).
- **Distributed Consistency:** Multi-warehouse inventory reservation, Saga-ready orchestration, and automatic compensating rollbacks on payment/logistics failures.
- **Hyperscale Readiness:** Cosine-similarity AI Vector Search, Apache Kafka (KRaft) event envelopes, Prometheus `/metrics`, W3C `traceparent` tracing, and Multi-Region Kubernetes (`eu-west-1` / `us-east-1`) with zero-downtime `RollingUpdate` and HPA.
- **Automated Quality Gates:** Every module ships with `pytest` suites, `ruff` linting, Docker Compose stacks, and dedicated GitHub Actions CI workflows.

---

## 🏗️ Architecture Overview

```mermaid
flowchart TB
    Portal["03 OmniStore Portal<br/>React + TypeScript + Tailwind"] --> Shield["05 CloudShield Gateway<br/>TLS + Rate Limit + OWASP"]
    Shield --> Auth["02 CoreAuth & Order API<br/>FastAPI + JWT + RBAC"]
    Shield --> Search["04 Search & Media Engine<br/>Redis Cache + DevOps"]
    Shield --> LB["06 Nginx Load Balancer<br/>least_conn"]
    LB --> Queue["06 Async Queue & Workers<br/>Redis + Retries + DLQ"]
    Auth --> Core["07 OmniChain Enterprise Core<br/>Multi-Warehouse + Cloud Logistics"]
    Core --> Hyper["08 Hyperscale Platform<br/>AI Vector Search + Distributed Saga"]
    Hyper --> Kafka[("Apache Kafka KRaft")]
    Hyper --> K8s["Kubernetes HPA + PDB<br/>eu-west-1 & us-east-1"]
    Hyper --> Obs["Observability Stack<br/>Prometheus + Grafana + OpenTelemetry"]
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
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white" />
  <img src="https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white" />
  <img src="https://img.shields.io/badge/React-61DAFB?style=flat-square&logo=react&logoColor=black" />
  <img src="https://img.shields.io/badge/TypeScript-3178C6?style=flat-square&logo=typescript&logoColor=white" />
  <img src="https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white" />
  <img src="https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white" />
  <img src="https://img.shields.io/badge/Apache%20Kafka-231F20?style=flat-square&logo=apachekafka&logoColor=white" />
  <img src="https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white" />
  <img src="https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white" />
  <img src="https://img.shields.io/badge/Kubernetes-326CE5?style=flat-square&logo=kubernetes&logoColor=white" />
  <img src="https://img.shields.io/badge/Prometheus-E6522C?style=flat-square&logo=prometheus&logoColor=white" />
  <img src="https://img.shields.io/badge/Grafana-F46800?style=flat-square&logo=grafana&logoColor=white" />
</div>

---

## 🚀 Quick Start

Each module is self-contained and can be launched independently with Docker Compose:

```bash
# Run Module 06 (Load-Balanced Async Queue & DLQ Cluster)
cd 06-AsyncQueue-LoadBalancer-Messenger && docker compose up --build

# Run Module 07 (Enterprise Commerce & Cloud Logistics Core)
cd 07-OmniChain-Enterprise-Core && docker compose up --build

# Run Module 08 (Hyperscale AI Vector Search, Saga, Kafka, Prometheus & Grafana)
cd 08-Hyperscale-Enterprise-Platform && docker compose up --build
```

---

## 📐 Architecture Decision Records (ADRs)

- [**ADR 0003** — Async Queue, Dead-Letter Queue & Load Balancing](./06-AsyncQueue-LoadBalancer-Messenger/docs/adr/0003-async-queue-dlq-and-load-balancing.md)
- [**ADR 0004** — Event-Driven Commerce & Cloud Logistics Orchestration](./07-OmniChain-Enterprise-Core/docs/adr/0004-enterprise-commerce-logistics-orchestration.md)
- [**ADR 0005** — Hyperscale Architecture: Kafka, AI Vector Search, Saga, K8s HPA & Multi-Region](./08-Hyperscale-Enterprise-Platform/docs/adr/0005-hyperscale-kafka-saga-vector-k8s-multiregion.md)

---

<div align="center">
  <sub>Built with engineering discipline for the <strong>OmniChain FullStack Roadmap</strong> • Release <code>v2.0.0</code></sub>
</div>

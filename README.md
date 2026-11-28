<div align="center">
  <img src="./.github/assets/banner.svg" alt="OmniChain Enterprise Platform" width="100%" />

  <p>
    <img src="[https://img.shields.io/badge/Modules-8%2F8%20Complete-10B981?style=for-the-badge](https://img.shields.io/badge/Modules-8%2F8%20Complete-10B981?style=for-the-badge)" alt="Modules 8/8" />
    <img src="[https://img.shields.io/badge/Release-v2.0.0-0284C7?style=for-the-badge](https://img.shields.io/badge/Release-v2.0.0-0284C7?style=for-the-badge)" alt="Release v2.0.0" />
    <img src="[https://img.shields.io/badge/Architecture-Hyperscale%20%26%20Event--Driven-6366F1?style=for-the-badge](https://img.shields.io/badge/Architecture-Hyperscale%20%26%20Event--Driven-6366F1?style=for-the-badge)" alt="Architecture" />
    <img src="[https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-1E293B?style=for-the-badge&logo=githubactions](https://img.shields.io/badge/CI%2FCD-GitHub%20Actions-1E293B?style=for-the-badge&logo=githubactions)" alt="CI/CD" />
  </p>
</div>

## Complete Roadmap Overview (Modules 01–08)

| # | Module | Core Stack & Engineering Highlights | Status |
|---|---|---|---|
| **01** | [`01-SmartStock-CLI-DB`](./01-SmartStock-CLI-DB) | Python CLI, PostgreSQL/SQLite, ACID Inventory Engine, Automated Tests | ✅ Completed |
| **02** | [`02-CoreAuth-Order-API`](./02-CoreAuth-Order-API) | FastAPI, JWT Authentication, RBAC, Order API, Pytest Suite | ✅ Completed |
| **03** | [`03-OmniStore-Frontend-Portal`](./03-OmniStore-Frontend-Portal) | React, TypeScript, Tailwind CSS, Admin & Storefront Portal | ✅ Completed |
| **04** | [`04-SearchMedia-DevOps-Engine`](./04-SearchMedia-DevOps-Engine) | Search & Media Engine, Redis Caching, Docker, CI/CD Pipeline | ✅ Completed |
| **05** | [`05-CloudShield-Production-Gateway`](./05-CloudShield-Production-Gateway) | Security Gateway, HTTPS/TLS, Rate Limiting, OWASP Hardening | ✅ Completed |
| **06** | [`06-AsyncQueue-LoadBalancer-Messenger`](./06-AsyncQueue-LoadBalancer-Messenger) | Redis Async Queue, Idempotency, Worker Retries & DLQ, Nginx `least_conn` LB | ✅ Completed |
| **07** | [`07-OmniChain-Enterprise-Core`](./07-OmniChain-Enterprise-Core) | Multi-Warehouse Inventory, Cloud Logistics, Saga-Ready Orchestrator & Rollback | ✅ Completed |
| **08** | [`08-Hyperscale-Enterprise-Platform`](./08-Hyperscale-Enterprise-Platform) | AI Vector Search, Distributed Saga, Kafka, K8s HPA, Prometheus/Grafana/OTel, Multi-Region | ✅ Completed |

## End-to-End Platform Architecture

```mermaid
flowchart TB
    Portal[03 OmniStore Portal] --> Shield[05 CloudShield Gateway]
    Shield --> Auth[02 CoreAuth & Order API]
    Shield --> Search[04 Search & Media Engine]
    Shield --> LB[06 Nginx Load Balancer]
    LB --> Queue[06 Async Queue & DLQ Workers]
    Auth --> Core[07 OmniChain Enterprise Core<br/>Multi-Warehouse + Logistics]
    Core --> Hyper[08 Hyperscale Platform<br/>AI Vector Search + Distributed Saga]
    Hyper --> Kafka[(Apache Kafka KRaft)]
    Hyper --> K8s[Kubernetes HPA<br/>eu-west-1 & us-east-1]
    Hyper --> Obs[Prometheus + Grafana + OpenTelemetry]
```

## Architecture Decision Records (ADRs)
- [ADR 0003: Async Queue, DLQ & Load Balancing](./06-AsyncQueue-LoadBalancer-Messenger/docs/adr/0003-async-queue-dlq-and-load-balancing.md)
- [ADR 0004: Event-Driven Commerce & Cloud Logistics Orchestration](./07-OmniChain-Enterprise-Core/docs/adr/0004-enterprise-commerce-logistics-orchestration.md)
- [ADR 0005: Hyperscale Architecture — Kafka, AI Vector Search, Saga, K8s HPA & Multi-Region](./08-Hyperscale-Enterprise-Platform/docs/adr/0005-hyperscale-kafka-saga-vector-k8s-multiregion.md)

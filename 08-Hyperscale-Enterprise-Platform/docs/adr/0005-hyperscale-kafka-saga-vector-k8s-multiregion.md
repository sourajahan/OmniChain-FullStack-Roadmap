# ADR 0005: Hyperscale Architecture — Kafka, AI Vector Search, Saga, K8s HPA & Multi-Region

## Status
Accepted

## Context
To scale OmniChain to global enterprise workloads (Amazon/Google-level reliability), the platform requires semantic AI search, distributed transaction safety across microservices, horizontal autoscaling, full-stack observability, and zero-downtime multi-region deployments.

## Decision
1. **AI Vector Search:** Provide deterministic vector embeddings and cosine-similarity ranking behind `/api/v1/search/semantic` (compatible with Elasticsearch/kNN vector backends).
2. **Distributed Saga Pattern:** Coordinate multi-service transactions with explicit forward steps and reverse compensating actions, emitting Kafka-ready event envelopes.
3. **Observability (Prometheus + Grafana + OpenTelemetry):** Expose Prometheus text-format metrics at `/metrics`, propagate W3C `traceparent` headers, and ship OTel Collector & Prometheus scrape configs.
4. **Kubernetes & Multi-Region Zero-Downtime:** Define Kustomize base + regional overlays (`eu-west-1`, `us-east-1`) with `RollingUpdate` (`maxUnavailable: 0`), `HorizontalPodAutoscaler`, and `PodDisruptionBudget`.

## Consequences
- **Positive:** Active-active multi-region readiness, automated scaling under load, and end-to-end distributed tracing.
- **Negative:** Higher operational complexity requiring strict schema versioning and SLO monitoring.

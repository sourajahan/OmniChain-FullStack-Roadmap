# ADR 0003: Asynchronous Message Queue, Dead-Letter Queue & Load Balancing

## Status
Accepted

## Context
Synchronous APIs degrade under traffic spikes and fail when downstream notification/messaging providers experience latency. We need horizontal scalability, fault isolation, and guaranteed delivery semantics.

## Decision
1. **Idempotent Producer API:** Clients submit messages with an `Idempotency-Key` header. Duplicate keys return the existing job record instead of enqueueing duplicate work.
2. **Async Queue + Worker + DLQ:** Jobs are enqueued into a Redis-backed broker (with an in-memory fallback for isolated unit testing). Workers process jobs with retry tracking and move permanently failing jobs into a Dead-Letter Queue (DLQ) for inspection and replay.
3. **Horizontal Load Balancing:** Nginx fronts multiple stateless API replicas using `least_conn` routing, passive health checks (`max_fails`, `fail_timeout`), and `X-Upstream-Instance` headers for observability.

## Consequences
- **Positive:** Decoupled ingestion and processing, zero-downtime scaling of API and worker replicas, and safe failure recovery via DLQ.
- **Negative:** Eventual consistency requires clients to poll job status or subscribe to completion events.

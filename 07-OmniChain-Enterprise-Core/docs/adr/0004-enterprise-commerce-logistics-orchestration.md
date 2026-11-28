# ADR 0004: Event-Driven Commerce & Cloud Logistics Orchestration

## Status
Accepted

## Context
An enterprise commerce and logistics platform must coordinate inventory reservation across multiple warehouses, payment capture, and carrier shipment dispatch without leaving orphaned stock reservations or inconsistent order states when downstream steps fail.

## Decision
1. **Modular Domain Boundaries:** Separate Inventory, Logistics, Event Bus, and Order Orchestration into decoupled domain modules behind a unified FastAPI Enterprise Core.
2. **Compensating Orchestration (Saga-Ready):** Execute checkout as `Reserve Inventory -> Capture Payment -> Dispatch Shipment`. Any failure after inventory reservation triggers an automatic compensating release (`release_stock`) and emits an `OrderCompensated` domain event.
3. **Idempotent Checkout:** Enforce `Idempotency-Key` deduplication on `POST /api/v1/orders` so network retries never double-charge or double-ship.
4. **Immutable Domain Event Log:** Emit structured events for every state transition to enable seamless Kafka streaming and observability in Phase 8.

## Consequences
- **Positive:** Strong consistency guarantees across commerce and logistics domains with full auditability.
- **Negative:** Requires explicit compensating actions for every side-effecting step in the order lifecycle.

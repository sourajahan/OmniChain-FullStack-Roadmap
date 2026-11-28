from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
import uuid


@dataclass
class SagaRecord:
    saga_id: str
    order_id: str
    status: str
    completed_steps: list[str] = field(default_factory=list)
    compensated_steps: list[str] = field(default_factory=list)
    kafka_events: list[dict[str, Any]] = field(default_factory=list)
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class DistributedSagaOrchestrator:
    """Executes forward Saga steps and runs reverse compensations on failure."""

    STEPS = ("reserve_inventory", "authorize_payment", "schedule_logistics")

    def __init__(self) -> None:
        self._sagas: dict[str, SagaRecord] = {}

    def _emit_kafka_envelope(self, record: SagaRecord, topic: str, event_type: str, step: str) -> None:
        record.kafka_events.append(
            {
                "topic": topic,
                "event_id": str(uuid.uuid4()),
                "event_type": event_type,
                "saga_id": record.saga_id,
                "order_id": record.order_id,
                "step": step,
                "timestamp": datetime.now(timezone.utc).isoformat(),
            }
        )

    def execute(self, order_id: str, fail_at_step: str | None = None) -> dict[str, Any]:
        record = SagaRecord(saga_id=f"SAGA-{uuid.uuid4().hex[:8].upper()}", order_id=order_id, status="RUNNING")

        for step in self.STEPS:
            if fail_at_step == step:
                record.status = "COMPENSATED"
                record.error = f"Step '{step}' failed in downstream microservice"
                self._emit_kafka_envelope(record, "omnichain.saga.events", "SagaStepFailed", step)
                for done_step in reversed(record.completed_steps):
                    comp_name = f"compensate_{done_step}"
                    record.compensated_steps.append(comp_name)
                    self._emit_kafka_envelope(record, "omnichain.saga.compensations", "SagaStepCompensated", comp_name)
                self._sagas[record.saga_id] = record
                return record.to_dict()

            record.completed_steps.append(step)
            self._emit_kafka_envelope(record, "omnichain.saga.events", "SagaStepCompleted", step)

        record.status = "COMPLETED"
        self._sagas[record.saga_id] = record
        return record.to_dict()

    def get(self, saga_id: str) -> dict[str, Any] | None:
        rec = self._sagas.get(saga_id)
        return rec.to_dict() if rec else None

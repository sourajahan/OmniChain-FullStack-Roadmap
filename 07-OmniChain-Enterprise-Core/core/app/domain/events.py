from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from typing import Any
import uuid


@dataclass(frozen=True)
class DomainEvent:
    event_id: str
    event_type: str
    aggregate_id: str
    payload: dict[str, Any]
    occurred_at: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class EventBus:
    """In-memory immutable domain event log ready for Kafka streaming in Phase 8."""

    def __init__(self) -> None:
        self._events: list[DomainEvent] = []

    def publish(self, event_type: str, aggregate_id: str, payload: dict[str, Any]) -> DomainEvent:
        event = DomainEvent(
            event_id=str(uuid.uuid4()),
            event_type=event_type,
            aggregate_id=aggregate_id,
            payload=payload,
        )
        self._events.append(event)
        return event

    def list_events(self, aggregate_id: str | None = None) -> list[dict[str, Any]]:
        items = self._events if not aggregate_id else [e for e in self._events if e.aggregate_id == aggregate_id]
        return [e.to_dict() for e in items]

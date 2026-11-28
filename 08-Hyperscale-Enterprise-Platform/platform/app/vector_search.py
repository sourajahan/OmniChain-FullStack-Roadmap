import hashlib
import math
import re
from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class VectorDocument:
    doc_id: str
    title: str
    category: str
    text: str
    vector: tuple[float, ...]


def embed_text(text: str, dims: int = 32) -> tuple[float, ...]:
    """Deterministic lightweight semantic hashing embedding (cosine-ready)."""
    vec = [0.0] * dims
    tokens = re.findall(r"[a-z0-9]+", text.lower())
    for token in tokens:
        digest = hashlib.sha256(token.encode("utf-8")).digest()
        idx = int.from_bytes(digest[:2], "big") % dims
        sign = 1.0 if (digest[2] % 2 == 0) else -1.0
        vec[idx] += sign
    norm = math.sqrt(sum(v * v for v in vec)) or 1.0
    return tuple(round(v / norm, 6) for v in vec)


def cosine_similarity(a: tuple[float, ...], b: tuple[float, ...]) -> float:
    return round(sum(x * y for x, y in zip(a, b, strict=True)), 6)


class VectorSearchEngine:
    """In-memory AI vector search index compatible with Elasticsearch/kNN backends."""

    def __init__(self) -> None:
        self._docs: list[VectorDocument] = []
        self._seed_catalog()

    def _seed_catalog(self) -> None:
        seeds = [
            ("SKU-K8S-EDGE", "Kubernetes Edge Server", "infrastructure", "kubernetes autoscaling multi region zero downtime cluster"),
            ("SKU-KAFKA-HUB", "Kafka Event Streaming Appliance", "messaging", "apache kafka real time event streaming saga distributed transactions"),
            ("SKU-GPU-AI", "AI Vector Inference Node", "ai", "elasticsearch vector search semantic embeddings neural inference gpu"),
            ("SKU-OTEL-BOX", "Observability Telemetry Gateway", "observability", "prometheus grafana opentelemetry distributed tracing metrics"),
        ]
        for doc_id, title, category, text in seeds:
            self.index_document(doc_id, title, category, text)

    def index_document(self, doc_id: str, title: str, category: str, text: str) -> dict[str, Any]:
        combined = f"{title} {category} {text}"
        doc = VectorDocument(doc_id=doc_id, title=title, category=category, text=text, vector=embed_text(combined))
        self._docs = [d for d in self._docs if d.doc_id != doc_id]
        self._docs.append(doc)
        return {"doc_id": doc.doc_id, "title": doc.title, "category": doc.category}

    def search(self, query: str, top_k: int = 3) -> list[dict[str, Any]]:
        q_vec = embed_text(query)
        scored = [
            {
                "doc_id": doc.doc_id,
                "title": doc.title,
                "category": doc.category,
                "score": cosine_similarity(q_vec, doc.vector),
            }
            for doc in self._docs
        ]
        scored.sort(key=lambda item: item["score"], reverse=True)
        return scored[:top_k]

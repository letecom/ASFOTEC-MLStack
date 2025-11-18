"""Thread-safe in-memory metrics collector for FastAPI endpoints."""

from __future__ import annotations

from collections import deque
from statistics import mean
from threading import Lock
from typing import Deque, Dict


class MetricsCollector:
    def __init__(self, max_samples: int = 1000) -> None:
        self._lock = Lock()
        self._max_samples = max_samples
        self._state: Dict[str, Dict[str, object]] = {}

    def _ensure_endpoint(self, name: str) -> Dict[str, object]:
        if name not in self._state:
            self._state[name] = {
                'count': 0,
                'errors': 0,
                'latencies': deque(maxlen=self._max_samples),
            }
        return self._state[name]

    def record(self, name: str, latency_ms: float, success: bool = True) -> None:
        with self._lock:
            bucket = self._ensure_endpoint(name)
            bucket['count'] = int(bucket['count']) + 1
            if not success:
                bucket['errors'] = int(bucket['errors']) + 1
            latencies: Deque[float] = bucket['latencies']  # type: ignore[assignment]
            latencies.append(latency_ms)

    def snapshot(self) -> Dict[str, Dict[str, float]]:
        with self._lock:
            result: Dict[str, Dict[str, float]] = {}
            for name, data in self._state.items():
                latencies = list(data['latencies'])  # type: ignore[arg-type]
                avg_latency = mean(latencies) if latencies else 0.0
                p95_latency = self._percentile(latencies, 95) if latencies else 0.0
                result[name] = {
                    'count': int(data['count']),
                    'errors': int(data['errors']),
                    'avg_latency_ms': round(avg_latency, 2),
                    'p95_latency_ms': round(p95_latency, 2),
                }
            return result

    @staticmethod
    def _percentile(values: list[float], percentile: float) -> float:
        if not values:
            return 0.0
        ordered = sorted(values)
        k = (len(ordered) - 1) * (percentile / 100)
        f = int(k)
        c = min(f + 1, len(ordered) - 1)
        if f == c:
            return ordered[int(k)]
        d0 = ordered[f] * (c - k)
        d1 = ordered[c] * (k - f)
        return d0 + d1


metrics_collector = MetricsCollector()

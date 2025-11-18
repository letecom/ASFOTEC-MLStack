from typing import Dict

from .metrics_collector import metrics_collector


class MetricsService:
    """Expose in-memory metrics snapshots for HTTP handlers."""

    def get_overview(self) -> Dict[str, Dict[str, float]]:
        return metrics_collector.snapshot()

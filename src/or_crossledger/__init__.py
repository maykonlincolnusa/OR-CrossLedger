"""Public API for OR CrossLedger."""

from .grouping import reconcile_groups
from .reconciliation import reconcile

__version__ = "0.3.0"


def project_info() -> dict[str, str]:
    return {
        "name": "OR CrossLedger",
        "focus": "Cross-ledger normalization and reconciliation",
        "status": "reference-prototype",
    }


__all__ = ["project_info", "reconcile", "reconcile_groups"]


"""Starter package for OR CrossLedger."""

from .reconciliation import reconcile

__version__ = "0.1.0"


def project_info() -> dict[str, str]:
    return {
        "name": "OR CrossLedger",
        "focus": "Cross-ledger normalization and reconciliation",
        "status": "starter",
    }


__all__ = ["project_info", "reconcile"]


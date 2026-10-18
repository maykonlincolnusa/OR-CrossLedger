"""Validated boundary used by the CLI and HTTP adapter."""
from .reconciliation import reconcile


def run(payload):
    if not isinstance(payload, dict) or set(payload) - set(["left","right","tolerance_seconds"]):
        raise ValueError("request must be an object containing only documented fields")
    return reconcile(payload.get('left'), payload.get('right'), payload.get('tolerance_seconds', 60))

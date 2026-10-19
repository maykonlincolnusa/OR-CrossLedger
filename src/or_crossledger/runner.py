"""Validated boundary used by the CLI and HTTP adapter."""
from .grouping import reconcile_groups
from .reconciliation import reconcile


def run(payload):
    if not isinstance(payload, dict) or set(payload) - set(["left","right","tolerance_seconds","action","max_group_size","max_combinations"]):
        raise ValueError("request must be an object containing only documented fields")
    payload = dict(payload)
    action = payload.pop("action", "one_to_one")
    if action == "groups":
        return reconcile_groups(**payload)
    if action != "one_to_one" or set(payload) - {"left", "right", "tolerance_seconds"}:
        raise ValueError("unknown action or unexpected group option")
    return reconcile(payload.get('left'), payload.get('right'), payload.get('tolerance_seconds', 60))

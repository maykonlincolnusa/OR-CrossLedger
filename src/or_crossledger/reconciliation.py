"""Conservative matching across two payment ledgers."""

from __future__ import annotations

from datetime import datetime, timedelta
from decimal import Decimal


def reconcile(
    left: list[dict[str, object]],
    right: list[dict[str, object]],
    tolerance_seconds: int = 60,
) -> dict[str, list[object]]:
    available = set(range(len(right)))
    matches: list[dict[str, str]] = []
    unmatched_left: list[str] = []
    tolerance = timedelta(seconds=tolerance_seconds)

    for source in left:
        candidates = []
        source_time = datetime.fromisoformat(str(source["occurred_at"]))
        for index in available:
            target = right[index]
            if str(source["currency"]) != str(target["currency"]):
                continue
            if Decimal(str(source["amount"])) != Decimal(str(target["amount"])):
                continue
            delta = abs(datetime.fromisoformat(str(target["occurred_at"])) - source_time)
            if delta <= tolerance:
                candidates.append((delta, index))
        if not candidates:
            unmatched_left.append(str(source["id"]))
            continue
        _, matched_index = min(candidates)
        available.remove(matched_index)
        matches.append({"left_id": str(source["id"]), "right_id": str(right[matched_index]["id"])})

    return {
        "matches": matches,
        "unmatched_left": unmatched_left,
        "unmatched_right": [str(right[index]["id"]) for index in sorted(available)],
    }


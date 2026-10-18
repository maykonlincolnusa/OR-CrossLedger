"""Conservative, permutation-invariant reconciliation with explicit ambiguity."""
from __future__ import annotations

from datetime import timedelta

from .validation import currency, instant, integer, money, text, unique_rows


def normalize_ledger(rows):
    normalized = []
    for row in unique_rows(rows):
        item = {
            **row, "amount": format(money(row.get("amount")), "f"),
            "currency": currency(row.get("currency")),
            "occurred_at": instant(row.get("occurred_at")).isoformat(),
        }
        if "reference" in item:
            text(item["reference"], "reference")
        normalized.append(item)
    return sorted(normalized, key=lambda row: row["id"])


def reconcile(left, right, tolerance_seconds=60):
    integer(tolerance_seconds, "tolerance_seconds", 0, 86400)
    left, right = normalize_ledger(left), normalize_ledger(right)
    edges = {}
    reverse = {row["id"]: [] for row in right}
    for source in left:
        candidates = []
        for target in right:
            if source["currency"] != target["currency"] or money(source["amount"]) != money(target["amount"]):
                continue
            if abs(instant(source["occurred_at"]) - instant(target["occurred_at"])) > timedelta(seconds=tolerance_seconds):
                continue
            # If either side supplies a reference, both must supply the same one.
            if ("reference" in source or "reference" in target) and source.get("reference") != target.get("reference"):
                continue
            for field in ("source_account_id", "destination_account_id"):
                if (field in source or field in target) and source.get(field) != target.get(field):
                    break
            else:
                candidates.append(target["id"])
                reverse[target["id"]].append(source["id"])
        edges[source["id"]] = candidates
    matches, ambiguous = [], []
    for source in left:
        candidates = edges[source["id"]]
        if len(candidates) == 1 and len(reverse[candidates[0]]) == 1:
            matches.append({"left_id": source["id"], "right_id": candidates[0],
                            "basis": "REFERENCE" if "reference" in source else "UNIQUE_AMOUNT_CURRENCY_TIME",
                            "review_required": "reference" not in source})
        elif candidates:
            ambiguous.append({"left_id": source["id"], "candidate_right_ids": candidates})
    matched_left = {r["left_id"] for r in matches}
    matched_right = {r["right_id"] for r in matches}
    return {
        "matches": matches, "ambiguous": ambiguous,
        "unmatched_left": [r["id"] for r in left if r["id"] not in matched_left],
        "unmatched_right": [r["id"] for r in right if r["id"] not in matched_right],
        "metrics": {"left_count": len(left), "right_count": len(right), "matched_count": len(matches),
                    "ambiguous_count": len(ambiguous)},
    }


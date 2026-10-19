"""Bounded many-to-one settlement reconciliation."""
from itertools import combinations

from .reconciliation import normalize_ledger
from .validation import instant, integer, money


def reconcile_groups(left, right, tolerance_seconds=300, max_group_size=3,
                     max_combinations=10000):
    integer(tolerance_seconds, "tolerance_seconds", 0, 86400)
    integer(max_group_size, "max_group_size", 2, 5)
    integer(max_combinations, "max_combinations", 1, 100000)
    left, right = normalize_ledger(left), normalize_ledger(right)
    candidates, work, truncated = {}, 0, False
    for target in right:
        target_candidates = []
        eligible = [item for item in left if item["currency"] == target["currency"]
                    and abs((instant(item["occurred_at"]) - instant(target["occurred_at"])).total_seconds())
                    <= tolerance_seconds
                    and not (("reference" in item or "reference" in target)
                             and item.get("reference") != target.get("reference"))]
        for size in range(2, min(max_group_size, len(eligible)) + 1):
            for group in combinations(eligible, size):
                if work >= max_combinations:
                    truncated = True
                    break
                work += 1
                if sum((money(item["amount"]) for item in group), money("0", allow_zero=True)) == money(target["amount"]):
                    target_candidates.append([item["id"] for item in group])
            if truncated:
                break
        candidates[target["id"]] = target_candidates
        if truncated:
            break
    proposed = {target_id: groups[0] for target_id, groups in candidates.items()
                if len(groups) == 1}
    owners = {}
    for target_id, group in proposed.items():
        for left_id in group:
            owners.setdefault(left_id, set()).add(target_id)
    unique, ambiguous = [], []
    for target_id, groups in sorted(candidates.items()):
        conflicts = sorted({other for group in groups for left_id in group
                            for other in owners.get(left_id, set()) if other != target_id})
        if len(groups) == 1 and not conflicts:
            unique.append({"left_ids": groups[0], "right_id": target_id,
                           "basis": "GROUP_SUM_CURRENCY_TIME", "review_required": True})
        elif groups:
            ambiguous.append({"right_id": target_id, "candidate_left_id_groups": groups,
                              "competing_right_ids": conflicts})
    return {"matches": unique, "ambiguous": ambiguous, "truncated": truncated,
            "combinations_evaluated": work}

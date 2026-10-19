from or_crossledger.grouping import reconcile_groups


def row(identifier, amount):
    return {"id": identifier, "amount": amount, "currency": "CHF",
            "occurred_at": "2026-01-01T10:00:00Z", "reference": "batch-1"}


def test_reconciles_unique_many_to_one_settlement():
    result = reconcile_groups([row("a", "40"), row("b", "60")], [row("settled", "100")])
    assert result["matches"][0]["left_ids"] == ["a", "b"]
    assert result["matches"][0]["review_required"] is True


def test_keeps_competing_groups_ambiguous():
    result = reconcile_groups([row("a", "40"), row("b", "60"), row("c", "50"), row("d", "50")],
                              [row("settled", "100")])
    assert result["matches"] == []
    assert len(result["ambiguous"][0]["candidate_left_id_groups"]) == 2


def test_does_not_reuse_same_left_group_for_two_settlements():
    result = reconcile_groups([row("a", "40"), row("b", "60")],
                              [row("settled-1", "100"), row("settled-2", "100")])
    assert result["matches"] == []
    assert {item["right_id"] for item in result["ambiguous"]} == {"settled-1", "settled-2"}

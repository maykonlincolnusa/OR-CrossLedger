import unittest

from or_crossledger import project_info, reconcile


def row(identifier, reference=None):
    value = {"id": identifier, "amount": "10.00", "currency": "BRL",
             "occurred_at": "2026-01-01T10:00:00+00:00"}
    if reference:
        value["reference"] = reference
    return value


class ProjectTest(unittest.TestCase):
    def test_reference_match_does_not_require_review(self):
        match = reconcile([row("a", "pix-e2e")], [row("b", "pix-e2e")])["matches"][0]
        self.assertFalse(match["review_required"])
        self.assertEqual(project_info()["status"], "reference-prototype")

    def test_ambiguous_candidates_remain_unmatched(self):
        result = reconcile([row("a")], [row("b"), row("c")])
        self.assertEqual(result["matches"], [])
        self.assertEqual(result["ambiguous"][0]["candidate_right_ids"], ["b", "c"])

    def test_does_not_mix_currencies(self):
        target = row("b")
        target["currency"] = "USD"
        self.assertEqual(reconcile([row("a")], [target])["matches"], [])


if __name__ == "__main__":
    unittest.main()

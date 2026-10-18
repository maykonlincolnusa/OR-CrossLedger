import unittest

from or_crossledger import project_info, reconcile


class ProjectSmokeTest(unittest.TestCase):
    def test_project_metadata(self) -> None:
        self.assertEqual(project_info()["status"], "starter")

    def test_reconciles_nearby_payment(self) -> None:
        left = [{"id": "a", "amount": "10.00", "currency": "BRL", "occurred_at": "2026-01-01T10:00:00+00:00"}]
        right = [{"id": "b", "amount": "10", "currency": "BRL", "occurred_at": "2026-01-01T10:00:20+00:00"}]
        self.assertEqual(reconcile(left, right)["matches"], [{"left_id": "a", "right_id": "b"}])



if __name__ == "__main__":
    unittest.main()


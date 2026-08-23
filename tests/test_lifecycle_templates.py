import unittest

from src.lifecycle_templates import template_for


class LifecycleDecisionTest(unittest.TestCase):
    def test_processed_content_selects_digital_asset_delivery(self):
        selected = template_for("processed")
        self.assertEqual(selected.name, "creator_asset_delivery")
        self.assertEqual(selected.subject, "Your digital asset is ready")


if __name__ == "__main__":
    unittest.main()

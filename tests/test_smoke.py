import unittest

import discordrpc


class ImportSmokeTests(unittest.TestCase):
    def test_package_imports(self):
        self.assertTrue(hasattr(discordrpc, "RPC"))

    def test_public_exports_present(self):
        for name in ("RPC", "button", "Activity", "StatusDisplay", "User", "Event"):
            self.assertTrue(hasattr(discordrpc, name), f"missing public export {name}")


if __name__ == "__main__":
    unittest.main(verbosity=2)

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

loader = unittest.TestLoader()
suite = loader.discover(os.path.dirname(__file__), pattern="test_*.py")
result = unittest.TextTestRunner(verbosity=2).run(suite)

if not result.wasSuccessful():
    sys.exit(1)

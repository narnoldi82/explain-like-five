import unittest
from factory_agentcore_probe import value

class ValueTest(unittest.TestCase):
    def test_value(self):
        self.assertEqual(value(), 1)

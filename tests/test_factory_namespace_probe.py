import importlib.util
import os
import unittest


class TestFactoryNamespaceProbe(unittest.TestCase):
    def test_probe_assertion_passes(self):
        """Verify that factory_namespace_probe.py executes without raising AssertionError."""
        probe_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            "factory_namespace_probe.py",
        )
        spec = importlib.util.spec_from_file_location("factory_namespace_probe", probe_path)
        module = importlib.util.module_from_spec(spec)
        # Executing the module runs `assert 1 + 1 == 2`; no exception means it passed.
        spec.loader.exec_module(module)

    def test_one_plus_one_equals_two(self):
        """Direct sanity check that the arithmetic the probe asserts is correct."""
        self.assertEqual(1 + 1, 2)


if __name__ == "__main__":
    unittest.main()

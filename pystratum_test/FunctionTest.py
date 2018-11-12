"""
PyStratum
"""
from pystratum_test.TestDataLayer import TestDataLayer
from pystratum_test.StratumTestCase import StratumTestCase


class FunctionTest(StratumTestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Stored routine with designation type function executes a stored function and return result.
        """
        ret = TestDataLayer.tst_test_function(2, 3)
        self.assertEqual(5, ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test2(self):
        """
        Stored routine with designation type function execute stored function and return result.
        """
        ret = TestDataLayer.tst_test_function(3, 4)
        self.assertNotEqual(5, ret)

# ----------------------------------------------------------------------------------------------------------------------

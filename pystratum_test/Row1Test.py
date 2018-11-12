"""
PyStratum
"""
from pystratum_test.TestDataLayer import TestDataLayer

from pystratum_test.StratumTestCase import StratumTestCase


class Row1Test(StratumTestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Stored routine with designation type row1 must return 1 row and 1 row only.
        """
        ret = TestDataLayer.tst_test_row1(1)
        self.assertIsInstance(ret, dict)

    # ------------------------------------------------------------------------------------------------------------------
    def test2(self):
        """
        An exception must be thrown when a stored routine with designation type row1 returns 0 rows.
        @expectedException Exception
        """
        with self.assertRaises(Exception):
            TestDataLayer.tst_test_row1(0)

    # ------------------------------------------------------------------------------------------------------------------
    def test3(self):
        """
        An exception must be thrown when a stored routine with designation type row1 returns more than 1 rows.
        @expectedException Exception
        """
        with self.assertRaises(Exception):
            TestDataLayer.tst_test_row1(2)

# ----------------------------------------------------------------------------------------------------------------------

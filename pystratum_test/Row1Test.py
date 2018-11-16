"""
PyStratum
"""
from pystratum.exception.ResultException import ResultException

from pystratum_test.TestDataLayer import TestDataLayer

from pystratum_test.StratumTestCase import StratumTestCase


class Row1Test(StratumTestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def test01(self):
        """
        Stored routine with designation type row1 must return 1 row and 1 row only.
        """
        ret = TestDataLayer.tst_test_row1(1)
        self.assertIsInstance(ret, dict)

    # ------------------------------------------------------------------------------------------------------------------
    def test02(self):
        """
        An exception must be thrown when a stored routine with designation type row1 returns 0 rows.
        """
        with self.assertRaises(Exception):
            TestDataLayer.tst_test_row1(0)

    # ------------------------------------------------------------------------------------------------------------------
    def test03(self):
        """
        An exception must be thrown when a stored routine with designation type row1 returns more than 1 rows.
        """
        with self.assertRaises(Exception):
            TestDataLayer.tst_test_row1(2)

    # ------------------------------------------------------------------------------------------------------------------
    def test11a(self):
        """
        Test with query selecting 1 row with arguments.
        """
        sql = 'select %s as "hello" from [dbo].[TST_FOO2] where tst_c00 <= %d'
        ret = TestDataLayer.execute_row1(sql, ('hello', 1))
        self.assertIsInstance(ret, dict)

    # ------------------------------------------------------------------------------------------------------------------
    def test11c(self):
        """
        Test with query selecting 1 row without arguments.
        """
        sql = 'select * from [dbo].[TST_FOO2] where tst_c00 <= 1'
        ret = TestDataLayer.execute_row1(sql)
        self.assertIsInstance(ret, dict)

    # ------------------------------------------------------------------------------------------------------------------
    def test12(self):
        """
        An exception must be thrown when a query returns 0 rows.
        """
        with self.assertRaises(ResultException):
            sql = 'select * from [dbo].[TST_FOO2] where tst_c00 <= 0'
            TestDataLayer.execute_row1(sql)

    # ------------------------------------------------------------------------------------------------------------------
    def test13(self):
        """
        An exception must be thrown when a query returns 0 rows.
        """
        with self.assertRaises(ResultException):
            sql = 'select * from [dbo].[TST_FOO2] where tst_c00 <= 2'
            TestDataLayer.execute_row1(sql)


# ----------------------------------------------------------------------------------------------------------------------

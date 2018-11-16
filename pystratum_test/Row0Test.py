"""
PyStratum
"""
from pystratum.exception.ResultException import ResultException

from pystratum_test.TestDataLayer import TestDataLayer
from pystratum_test.StratumTestCase import StratumTestCase


class Row0Test(StratumTestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def test01(self):
        """
        Stored routine with designation type row0 must return None.
        """
        ret = TestDataLayer.tst_test_row0(0)
        self.assertIsNone(ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test02(self):
        """
        Stored routine with designation type row0 must return 1 row.
        """
        ret = TestDataLayer.tst_test_row0(1)
        self.assertIsInstance(ret, dict)

    # ------------------------------------------------------------------------------------------------------------------
    def test03(self):
        """
        An exception must be thrown when a stored routine with designation type row0 returns more than 1 rows.
        """
        with self.assertRaises(ResultException):
            TestDataLayer.tst_test_row0(2)

    # ------------------------------------------------------------------------------------------------------------------
    def test11a(self):
        """
        A query selecting 0 rows with arguments must return None.
        """
        sql = 'select %s as "hello" from [dbo].[TST_FOO2] where tst_c00 <= %d'
        ret = TestDataLayer.execute_row0(sql, ('hello', 0))
        self.assertIsNone(ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test11b(self):
        """
        A query selecting 0 rows without arguments must return None.
        """
        sql = 'select * from [dbo].[TST_FOO2] where tst_c00 <= 0'
        ret = TestDataLayer.execute_row0(sql)
        self.assertIsNone(ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test13(self):
        """
        An exception must be thrown when a query returns more than 1 rows.
        """
        with self.assertRaises(ResultException):
            sql = 'select * from [dbo].[TST_FOO2] where tst_c00 <= 2'
            TestDataLayer.execute_row0(sql)

# ----------------------------------------------------------------------------------------------------------------------

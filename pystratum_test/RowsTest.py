"""
PyStratum
"""
from pystratum_test.TestDataLayer import TestDataLayer

from pystratum_test.StratumTestCase import StratumTestCase


class RowsTest(StratumTestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def test01(self):
        """
        Stored routine with designation type rows must return an empty array when no rows are selected.
        """
        ret = TestDataLayer.tst_test_rows(0)
        self.assertIsInstance(ret, list)
        self.assertEqual(0, len(ret))

    # ------------------------------------------------------------------------------------------------------------------
    def test02(self):
        """
        Stored routine with designation type rows must return an array with 1 row when only 1 row is selected.
        """
        ret = TestDataLayer.tst_test_rows(1)
        self.assertIsInstance(ret, list)
        self.assertEqual(1, len(ret))

    # ------------------------------------------------------------------------------------------------------------------
    def test03(self):
        """
        Stored routine with designation type rows must return an array with 3 rows when 3 rows are selected.
        """
        ret = TestDataLayer.tst_test_rows(3)
        self.assertIsInstance(ret, list)
        self.assertEqual(3, len(ret))

    # ------------------------------------------------------------------------------------------------------------------
    def test13a(self):
        """
        Test with query selecting 3 rows with arguments.
        """
        sql = 'select * from [dbo].[TST_FOO2] where [tst_c00] <= %d'
        ret = TestDataLayer.execute_rows(sql, 3)
        self.assertIsInstance(ret, list)
        self.assertEqual(3, len(ret))

    # ------------------------------------------------------------------------------------------------------------------
    def test13b(self):
        """
        Test with query selecting 3 rows with arguments as tuple.
        """
        sql = 'select * from [dbo].[TST_FOO2] where [tst_c00] <= %d'
        ret = TestDataLayer.execute_rows(sql, (3,))
        self.assertIsInstance(ret, list)
        self.assertEqual(3, len(ret))

    # ------------------------------------------------------------------------------------------------------------------
    def test13c(self):
        """
        Test with query selecting 3 rows without arguments.
        """
        sql = 'select * from [dbo].[TST_FOO2] where [tst_c00] <= 3'
        ret = TestDataLayer.execute_rows(sql)
        self.assertIsInstance(ret, list)
        self.assertEqual(3, len(ret))

# ----------------------------------------------------------------------------------------------------------------------

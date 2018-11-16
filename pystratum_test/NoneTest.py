"""
PyStratum
"""
from pystratum_test.TestDataLayer import TestDataLayer
from pystratum_test.StratumTestCase import StratumTestCase


class NoneTest(StratumTestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def test_none1(self):
        """
        SQL without selecting rows.
        """
        sql = 'insert into [TST_LABEL]([tst_test], [tst_label]) values(%s, %s)'
        ret = TestDataLayer.execute_none(sql, ('test_none1', None))
        self.assertIsNone(ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test_tst_test_none0(self):
        """
        Stored routine with designation type none with arguments.
        """
        ret = TestDataLayer.tst_test_none0('tst_test_none0', None)
        self.assertIsNone(ret)

    # ------------------------------------------------------------------------------------------------------------------
    def test_tst_test_none1(self):
        """
        Stored routine with designation type none without arguments..
        """
        ret = TestDataLayer.tst_test_none1()
        self.assertIsNone(ret)

# ----------------------------------------------------------------------------------------------------------------------

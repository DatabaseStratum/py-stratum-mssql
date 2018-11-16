"""
PyStratum
"""
import unittest

from pystratum_test.TestDataLayer import TestDataLayer


class StratumTestCase(unittest.TestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def setUp(self):
        TestDataLayer.connect(server='192.168.1.23',
                              user='test',
                              password='test',
                              database='test')

    # ------------------------------------------------------------------------------------------------------------------
    def tearDown(self):
        TestDataLayer.disconnect()

# ----------------------------------------------------------------------------------------------------------------------

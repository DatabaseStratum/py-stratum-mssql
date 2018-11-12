"""
PyStratum
"""
import unittest

from pystratum_test.TestDataLayer import TestDataLayer


class StratumTestCase(unittest.TestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def setUp(self):
        TestDataLayer.connect('192.168.1.23', 'test', 'test', 'test')

    # ------------------------------------------------------------------------------------------------------------------
    def tearDown(self):
        TestDataLayer.disconnect()

# ----------------------------------------------------------------------------------------------------------------------

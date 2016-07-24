"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
import unittest

from test.DataLayer import DataLayer


class StratumTestCase(unittest.TestCase):
    # ------------------------------------------------------------------------------------------------------------------
    def setUp(self):
        DataLayer.connect('192.168.137.7', 'test', 'test', 'test')

    # ------------------------------------------------------------------------------------------------------------------
    def tearDown(self):
        DataLayer.disconnect()

# ----------------------------------------------------------------------------------------------------------------------

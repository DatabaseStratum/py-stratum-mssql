import sys
import unittest
from configparser import ConfigParser
from io import StringIO
from typing import Optional

from pystratum_mssql.MsSqlDefaultConnector import MsSqlDefaultConnector
from test.TestDataLayer import TestDataLayer


class StratumTestCase(unittest.TestCase):
    def __init__(self, method_name):
        """
        Object constructor.
        """
        super().__init__(method_name)

        config = ConfigParser()
        config.read('test/etc/credentials.cfg')

        params = {'host':     self.__get_option(config, 'database', 'host', fallback='localhost'),
                  'user':     self.__get_option(config, 'database', 'user'),
                  'password': self.__get_option(config, 'database', 'password'),
                  'database': self.__get_option(config, 'database', 'database')}

        self._dl: TestDataLayer = TestDataLayer(MsSqlDefaultConnector(params))
        """
        The generated data layer.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def setUp(self):
        self._dl.connect()

        self.held, sys.stdout = sys.stdout, StringIO()

    # ------------------------------------------------------------------------------------------------------------------
    def tearDown(self):
        sys.stdout = self.held
        self._dl.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def __get_option(config: ConfigParser,
                     section: str,
                     option: str,
                     fallback: Optional[str] = None) -> str:
        """
        Reads an option for a configuration file.

        :param configparser.ConfigParser config: The main config file.
        :param str section: The name of the section op the option.
        :param str option: The name of the option.
        :param str|None fallback: The fallback value of the option if it is not set in either configuration files.

        :rtype: str

        :raise KeyError:
        """
        return_value = config.get(section, option, fallback=fallback)

        if fallback is None and return_value is None:
            raise KeyError("Option '{0!s}' is not found in section '{1!s}'.".format(option, section))

        return return_value

# ----------------------------------------------------------------------------------------------------------------------

from configparser import ConfigParser
from typing import Dict, Optional, Union

from pystratum_backend.StratumStyle import StratumStyle

from pystratum_mssql.MsSqlDefaultConnector import MsSqlDefaultConnector
from pystratum_mssql.MsSqlMetadataDataLayer import MsSqlMetadataDataLayer


class MsSqlWorker:
    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io: StratumStyle, config: ConfigParser):
        """
        Object constructor.

        :param PyStratumStyle io: The output decorator.
        """

        self._io: StratumStyle = io
        """
        The output decorator.
        """

        self._config: ConfigParser = config
        """
        The configuration object.
        """

        self._dl = MsSqlMetadataDataLayer(io, MsSqlDefaultConnector(self.__read_configuration_file()))
        """
        The metadata layer.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def connect(self) -> None:
        """
        Connects to the database.
        """
        self._dl.connect()

    # ------------------------------------------------------------------------------------------------------------------
    def disconnect(self) -> None:
        """
        Disconnects from the database.
        """
        self._dl.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    def __read_configuration_file(self) -> Dict[str, Union[str, int]]:
        """
        Reads connections parameters from the configuration file.
        """
        params = {'host':     self.__get_option(self._config, 'database', 'host', fallback='localhost'),
                  'user':     self.__get_option(self._config, 'database', 'user'),
                  'password': self.__get_option(self._config, 'database', 'password'),
                  'database': self.__get_option(self._config, 'database', 'database')}

        return params

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

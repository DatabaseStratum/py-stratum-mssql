"""
PyStratum
"""
from pystratum.Connection import Connection
from pystratum.MetadataDataLayer import MetadataDataLayer

from pystratum_mssql.MsSqlMetadataDataLayer import MsSqlMetadataDataLayer


class MsSqlConnection(Connection):
    """
    Class for connecting to SQL Server instances and reading SQl Server specific connection parameters from
    configuration files.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io):
        """
        Object constructor.

        :param pystratum.style.PyStratumStyle.PyStratumStyle io: The output decorator.
        """
        Connection.__init__(self, io)
        """
        Object constructor.
        """
        self._host = ''
        """
        The hostname of the SQL Server instance.

        :type: str
        """

        self._user = ''
        """
        User name.

        :type: str
        """

        self._password = ''
        """
        Password required for singing on to the SQL Server instance.

        :type: str
        """

        self._database = ''
        """
        The database name.

        :type: str
        """

    # ------------------------------------------------------------------------------------------------------------------
    def connect(self):
        """
        Connects to the database.
        """
        MetadataDataLayer.io = self._io
        MsSqlMetadataDataLayer.connect(server=self._host,
                                       user=self._user,
                                       password=self._password,
                                       database=self._database)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def disconnect():
        """
        Disconnects from the database.
        """
        MsSqlMetadataDataLayer.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, filename):
        """
        Reads connections parameters from the configuration file.

        :param str filename: The path to the configuration file.
        """
        config, config_supplement = self._read_configuration(filename)

        self._host = self._get_option(config, config_supplement, 'database', 'host')
        self._user = self._get_option(config, config_supplement, 'database', 'user')
        self._password = self._get_option(config, config_supplement, 'database', 'password')
        self._database = self._get_option(config, config_supplement, 'database', 'database')

# ----------------------------------------------------------------------------------------------------------------------

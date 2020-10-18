import pymssql
from typing import Dict, Optional, Union, Any

from pystratum_mssql.MsSqlConnector import MsSqlConnector
from pystratum_mssql.MsSqlDataLayer import MsSqlDataLayer


class MsSqlDefaultConnector(MsSqlConnector):
    """
    Connects to a MySQL instance using user name and password.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, params: Dict[str, Union[str, int]]):
        """
        Object constructor.
        
        :param params: The connection parameters.
        """

        self._params: Dict[str, Union[str, int]] = params
        """
        The connection parameters.
        """

        self._connection: Optional[Any] = None
        """
        The connection between Python and the MySQL instance.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def connect(self) -> Any:
        """
        Connects to the MySQL instance.
        """
        self._connection = pymssql.connect(**self._params)

        # Install our own message handler.
        self._connection._conn.set_msghandler(MsSqlDataLayer.stratum_msg_handler)

        # Set the default settings.
        cursor = self._connection.cursor()
        cursor.execute('set nocount on')
        cursor.execute('set ansi_nulls on')
        cursor.close()

        return self._connection

    # ------------------------------------------------------------------------------------------------------------------
    def disconnect(self) -> None:
        """
        Disconnects from the MySQL instance.
        """
        if self._connection:
            self._connection.close()
            self._connection = None

# ----------------------------------------------------------------------------------------------------------------------

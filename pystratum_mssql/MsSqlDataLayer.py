import csv
import re
import sys
from time import gmtime, strftime
from typing import Any, Dict, List, Optional

from pystratum_middle.exception.ResultException import ResultException

from pystratum_mssql.MsSqlConnector import MsSqlConnector


class MsSqlDataLayer:
    """
    Class for connecting to a SQL Server instance and executing SQL statements. Also, a parent class for classes with
    static wrapper methods for executing stored procedures and functions.
    """
    # ------------------------------------------------------------------------------------------------------------------
    _suppress_superfluous_messages = True
    """
    If set superfluous messages like below will be suppressed:
    * "Warning: Null value is eliminated by an aggregate or other SET operation."
    * The module ... depends on the missing object .... The module will still be created; however, it cannot run
      successfully until the object exists.

    :type: bool
    """

    line_buffered = True
    """
    If True log messages from stored procedures with designation type 'log' are line buffered (Note: In python
    sys.stdout is buffered by default).

    :type: bool
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, connector: MsSqlConnector):
        """
        Object constructor.
        """

        self.__connector: MsSqlConnector = connector
        """
        The object for connecting to a MySQL instance.
        """

        self.__conn: Optional[Any] = None
        """
        The connection between Python and the MySQL instance.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def autocommit(self, status: bool) -> None:
        """
        Sets auto commit mode.
        See http://pymssql.org/en/stable/ref/pymssql.html#pymssql.Connection.autocommit.

        :param bool status: True: Auto commit on. False: Auto commit off.
        """
        self.__conn.autocommit(status)

    # ------------------------------------------------------------------------------------------------------------------
    def commit(self) -> None:
        """
        Commits the current transaction.
        See http://pymssql.org/en/stable/ref/pymssql.html#pymssql.Connection.commit.
        """
        self.__conn.commit()

    # ------------------------------------------------------------------------------------------------------------------
    def connect(self) -> None:
        """
        Connects to a MS SQL Server instance.
        """
        self.__conn = self.__connector.connect()

    # ------------------------------------------------------------------------------------------------------------------
    def disconnect(self) -> None:
        """
        Disconnects from the MS SQL Server instance.
        See http://pymssql.org/en/stable/ref/pymssql.html#pymssql.Connection.close.
        """
        self.__conn = None
        self.__connector.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    def execute_csv(self, sql: str, filename: str, dialect: str = 'unix', encoding: str = 'utf-8') -> int:
        file = open(filename, 'w', encoding=encoding)
        csv_file = csv.writer(file, dialect=dialect)

        # Run the query.
        cursor = self.__conn.cursor(as_dict=False)
        cursor.execute(sql)

        # Store all rows in CSV format in the file.
        n = 0
        for row in cursor:
            csv_file.writerow(row)
            n += 1

        # Close the CSV file and the cursor.
        file.close()
        cursor.close()

        return n

    # ------------------------------------------------------------------------------------------------------------------
    def execute_log(self, sql: str, *params) -> int:
        """
        Executes a query with log statements. Returns the number of lines in the log.

        :param str sql: The SQL statement.
        :param iterable params: The parameters.

        :rtype: int
        """
        cursor = self.__conn.cursor()
        cursor.execute(sql, params)

        n = 0
        next_set = True
        while next_set:
            stamp = strftime('%Y-%m-%d %H:%M:%S', gmtime())
            for row in cursor:
                print(stamp, end='')
                for field in row:
                    print(' %s' % field, end='')
                print('', flush=self.line_buffered)
                n += 1

            next_set = cursor.nextset()

        cursor.close()

        return n

    # ------------------------------------------------------------------------------------------------------------------
    def execute_none(self, sql: str, *params) -> None:
        """
        Executes a query that does not select any rows.

        :param str sql: The SQL statement.
        :param iterable params: The parameters.

        :rtype: None
        """
        cursor = self.__conn.cursor()
        cursor.execute(sql, *params)
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------
    def execute_row0(self, sql, *params) -> Optional[Dict[str, Any]]:
        """
        Executes a query that selects 0 or 1 row. Returns the selected row or None.

        :param str sql: The SQL statement.
        :param iterable params: The parameters.

        :rtype: None|dict[str,*]
        """
        cursor = self.__conn.cursor(as_dict=True)
        cursor.execute(sql, *params)
        rows = cursor.fetchall()
        cursor.close()

        n = len(rows)
        if n == 1:
            return rows[0]
        elif n == 0:
            return None
        else:
            raise ResultException('0 or 1', n, sql)

    # ------------------------------------------------------------------------------------------------------------------
    def execute_row1(self, sql: str, *params) -> Dict[str, Any]:
        """
        Executes a query that selects 1 row. Returns the selected row.

        :param str sql: The SQL statement.
        :param iterable params: The parameters.

        :rtype: dict[str,*]
        """
        cursor = self.__conn.cursor(as_dict=True)
        cursor.execute(sql, *params)
        rows = cursor.fetchall()
        cursor.close()

        n = len(rows)
        if n != 1:
            raise ResultException('1', n, sql)

        return rows[0]

    # ------------------------------------------------------------------------------------------------------------------
    def execute_rows(self, sql: str, *params) -> List[Dict[str, Any]]:
        """
        Executes a query that selects 0 or more rows. Returns the selected rows (an empty list if no rows
        are selected).

        :param str sql: The SQL statement.
        :param iterable params: The parameters.

        :rtype: list[dict[str,*]]
        """
        cursor = self.__conn.cursor(as_dict=True)
        cursor.execute(sql, *params)
        rows = cursor.fetchall()
        cursor.close()

        return rows

    # ------------------------------------------------------------------------------------------------------------------
    def execute_singleton0(self, sql: str, *params) -> Any:
        """
        Executes a query that selects 0 or 1 row with 1 column. Returns the value of selected column or None.

        :param str sql: The SQL statement.
        :param iterable params: The parameters.

        :rtype: *
        """
        cursor = self.__conn.cursor()
        cursor.execute(sql, *params)
        rows = cursor.fetchall()
        cursor.close()

        n = len(rows)
        if n == 1:
            return rows[0][0]
        elif n == 0:
            return None
        else:
            raise ResultException('0 or 1', n, sql)

    # ------------------------------------------------------------------------------------------------------------------
    def execute_singleton1(self, sql: str, *params) -> Any:
        """
        Executes a query that selects 1 row with 1 column. Returns the value of the selected column.

        :param str sql:The SQL statement.
        :param iterable params: The parameters.

        :rtype: *
        """
        cursor = self.__conn.cursor()
        cursor.execute(sql, *params)
        rows = cursor.fetchall()
        cursor.close()

        n = len(rows)
        if n != 1:
            raise ResultException('1', n, sql)

        return rows[0][0]

    # ------------------------------------------------------------------------------------------------------------------
    def execute_sp_none(self, sql: str, *params) -> None:
        """
        Executes a stored routine that does not select any rows.

        :param str sql: The SQL calling the stored procedure.
        :param iterable params: The parameters for the stored procedure.

        :rtype: None
        """
        cursor = self.__conn.cursor()
        cursor.execute(sql, params)
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------
    def execute_sp_row0(self, sql: str, *params) -> Optional[Dict[str, Any]]:
        """
        Executes a stored procedure that selects 0 or 1 row. Returns the selected row or None.

        :param str sql: The SQL call the the stored procedure.
        :param iterable params: The parameters for the stored procedure.

        :rtype: None|dict[str,*]
        """
        cursor = self.__conn.cursor(as_dict=True)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        n = len(rows)
        if n == 1:
            return rows[0]
        elif n == 0:
            return None
        else:
            raise ResultException('0 or 1', n, sql)

    # ------------------------------------------------------------------------------------------------------------------
    def execute_sp_row1(self, sql: str, *params) -> Dict[str, Any]:
        """
        Executes a stored procedure that selects 1 row. Returns the selected row.

        :param str sql: The SQL calling the the stored procedure.
        :param iterable params: The parameters for the stored procedure.

        :rtype: dict[str,*]
        """
        cursor = self.__conn.cursor(as_dict=True)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        n = len(rows)
        if n != 1:
            raise ResultException('1', n, sql)

        return rows[0]

    # ------------------------------------------------------------------------------------------------------------------
    def execute_sp_rows(self, sql: str, *params) -> List[Dict[str, Any]]:
        """
        Executes a stored procedure that selects 0 or more rows. Returns the selected rows (an empty list if no rows
        are selected).

        :param str sql: The SQL calling the the stored procedure.
        :param iterable params: The parameters for the stored procedure.

        :rtype: list[dict[str,*]]
        """
        cursor = self.__conn.cursor(as_dict=True)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        return rows

    # ------------------------------------------------------------------------------------------------------------------
    def execute_sp_singleton0(self, sql: str, *params) -> Any:
        """
        Executes a stored procedure that selects 0 or 1 row with 1 column. Returns the value of selected column or None.

        :param str sql: The SQL calling the stored procedure.
        :param iterable params: The parameters for the stored procedure.

        :rtype: *
        """
        cursor = self.__conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        n = len(rows)
        if n == 1:
            return rows[0][0]
        elif n == 0:
            return None
        else:
            raise ResultException('0 or 1', n, sql)

    # ------------------------------------------------------------------------------------------------------------------
    def execute_sp_singleton1(self, sql: str, *params) -> Any:
        """
        Executes a stored routine with designation type "table", i.e a stored routine that is expected to select 1 row
        with 1 column.

        :param str sql: The SQL calling the the stored procedure.
        :param iterable params: The parameters for the stored procedure.

        :rtype: * The value of the selected column.
        """
        cursor = self.__conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        n = len(rows)
        if n != 1:
            raise ResultException('1', n, sql)

        return rows[0][0]

    # ------------------------------------------------------------------------------------------------------------------
    def rollback(self) -> None:
        """
        Rolls back the current transaction.
        See http://pymssql.org/en/stable/ref/pymssql.html#pymssql.Connection.rollback.
        """
        self.__conn.rollback()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def stratum_msg_handler(msgstate: str, severity: int, srvname: str, procname: str, line: int, msgtext: bin) -> None:
        """
        Custom message handler suppressing some superfluous messages.
        """
        if severity > 0:
            print("Error at line %d: %s" % (line, msgtext.decode("utf-8")), file=sys.stderr)
        else:
            msg = msgtext.decode("utf-8")

            # Suppress bogus messages if flag is set.
            if MsSqlDataLayer._suppress_superfluous_messages:
                # @todo Make this method more flexible by using two lists. One with strings and one on regex to
                # suppress.
                if msg == 'Warning: Null value is eliminated by an aggregate or other SET operation.':
                    return

                if re.match(
                        "^The module \'.*\' depends on the missing object \'.*\'. The module will still be created; "
                        "however, it cannot run successfully until the object exists.$",
                        msg):
                    return

            print(msg)

# ----------------------------------------------------------------------------------------------------------------------

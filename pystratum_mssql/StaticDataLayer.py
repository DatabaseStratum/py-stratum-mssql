"""
PyStratum
"""
import csv
import pymssql
import re
import sys
from time import strftime, gmtime

from pystratum.exception.ResultException import ResultException


class StaticDataLayer:
    """
    Class for connecting to a SQL Server instance and executing SQL statements. Also, a parent class for classes with
    static wrapper methods for executing stored procedures and functions.
    """
    # ------------------------------------------------------------------------------------------------------------------
    __conn = None
    """
    The SQL connection.

    :type: Object
    """

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
    @staticmethod
    def autocommit(status):
        """
        Sets auto commit mode.
        See http://pymssql.org/en/stable/ref/pymssql.html#pymssql.Connection.autocommit.

        :param bool status: True: Auto commit on. False: Auto commit off.
        """
        StaticDataLayer.__conn.autocommit(status)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def commit():
        """
        Commits the current transaction.
        See http://pymssql.org/en/stable/ref/pymssql.html#pymssql.Connection.commit.
        """
        StaticDataLayer.__conn.commit()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def connect(**kwargs):
        # Connect to the SQL-Server
        StaticDataLayer.__conn = pymssql.connect(**kwargs)

        # Install our own message handler.
        StaticDataLayer.__conn._conn.set_msghandler(StaticDataLayer.stratum_msg_handler)

        # Set the default settings.
        cursor = StaticDataLayer.__conn.cursor()
        cursor.execute('set nocount on')
        cursor.execute('set ansi_nulls on')
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def disconnect():
        """
        Disconnects from the MS SQL Server instance.
        See http://pymssql.org/en/stable/ref/pymssql.html#pymssql.Connection.close.
        """
        StaticDataLayer.__conn.close()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_csv(sql, filename, dialect='unix', encoding='utf-8'):
        # Open the CSV file.
        file = open(filename, 'w', encoding=encoding)
        csv_file = csv.writer(file, dialect=dialect)

        # Run the query.
        cursor = StaticDataLayer.__conn.cursor(as_dict=False)
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
    @staticmethod
    def execute_log(sql, *params):
        cursor = StaticDataLayer.__conn.cursor()
        cursor.execute(sql, params)

        n = 0
        next_set = True
        while next_set:
            stamp = strftime('%Y-%m-%d %H:%M:%S', gmtime())
            for row in cursor:
                print(stamp, end='')
                for field in row:
                    print(' %s' % field, end='')
                print('', flush=StaticDataLayer.line_buffered)
                n += 1

            next_set = cursor.nextset()

        cursor.close()

        return n

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_none(sql, *params):
        cursor = StaticDataLayer.__conn.cursor()
        cursor.execute(sql, *params)
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_row0(sql, *params):
        cursor = StaticDataLayer.__conn.cursor(as_dict=True)
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
    @staticmethod
    def execute_row1(sql, *params):
        cursor = StaticDataLayer.__conn.cursor(as_dict=True)
        cursor.execute(sql, *params)
        rows = cursor.fetchall()
        cursor.close()

        n = len(rows)
        if n != 1:
            raise ResultException('1', n, sql)

        return rows[0]

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_rows(sql, *params):
        cursor = StaticDataLayer.__conn.cursor(as_dict=True)
        cursor.execute(sql, *params)
        rows = cursor.fetchall()
        cursor.close()

        return rows

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_singleton0(sql, *params):
        cursor = StaticDataLayer.__conn.cursor()
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
    @staticmethod
    def execute_singleton1(sql, *params):
        cursor = StaticDataLayer.__conn.cursor()
        cursor.execute(sql, *params)
        rows = cursor.fetchall()
        cursor.close()

        n = len(rows)
        if n != 1:
            raise ResultException('1', n, sql)

        return rows[0][0]

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_none(sql, *params):
        cursor = StaticDataLayer.__conn.cursor()
        cursor.execute(sql, params)
        cursor.close()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_row0(sql, *params):
        cursor = StaticDataLayer.__conn.cursor(as_dict=True)
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
    @staticmethod
    def execute_sp_row1(sql, *params):
        cursor = StaticDataLayer.__conn.cursor(as_dict=True)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        n = len(rows)
        if n != 1:
            raise ResultException('1', n, sql)

        return rows[0]

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_rows(sql, *params):
        cursor = StaticDataLayer.__conn.cursor(as_dict=True)
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        return rows

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_sp_singleton0(sql, *params):
        cursor = StaticDataLayer.__conn.cursor()
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
    @staticmethod
    def execute_sp_singleton1(sql, *params):
        cursor = StaticDataLayer.__conn.cursor()
        cursor.execute(sql, params)
        rows = cursor.fetchall()
        cursor.close()

        n = len(rows)
        if n != 1:
            raise ResultException('1', n, sql)

        return rows[0][0]

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_table(sql, *params):
        # @todo methods for showing table
        raise NotImplementedError

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def rollback():
        """
        Rolls back the current transaction.
        See http://pymssql.org/en/stable/ref/pymssql.html#pymssql.Connection.rollback.
        """
        StaticDataLayer.__conn.rollback()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def stratum_msg_handler(msgstate, severity, srvname, procname, line, msgtext):
        """
        Custom message handler suppressing some superfluous messages.
        """
        if severity > 0:
            print("Error at line %d: %s" % (line, msgtext.decode("utf-8")), file=sys.stderr)
        else:
            msg = msgtext.decode("utf-8")

            # Suppress bogus messages if flag is set.
            if StaticDataLayer._suppress_superfluous_messages:
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

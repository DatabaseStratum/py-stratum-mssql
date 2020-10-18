from configparser import ConfigParser
from typing import Any, Dict, Optional

from pystratum_backend.StratumStyle import StratumStyle
from pystratum_common.backend.CommonRoutineLoaderWorker import CommonRoutineLoaderWorker

from pystratum_mssql.backend.MsSqlWorker import MsSqlWorker
from pystratum_mssql.helper.MsSqlRoutineLoaderHelper import MsSqlRoutineLoaderHelper


class MsSqlRoutineLoaderWorker(MsSqlWorker, CommonRoutineLoaderWorker):
    """
    Class for loading stored routines into a SQL Server instance from pseudo SQL files.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io: StratumStyle, config: ConfigParser):
        """
        Object constructor.

        :param PyStratumStyle io: The output decorator.
        """
        MsSqlWorker.__init__(self, io, config)
        CommonRoutineLoaderWorker.__init__(self, io, config)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_column_type(self) -> None:
        """
        Selects schema, table, column names and the column types from the SQL Server instance and saves them as replace
        pairs.
        """
        rows = self._dl.get_all_table_columns()
        for row in rows:
            key = '@{0}.{1}.{2}%type@'.format(row['schema_name'], row['table_name'], row['column_name'])
            key = key.lower()

            value = self._derive_data_type(row)

            self._replace_pairs[key] = value

        self._io.text('Selected {0} column types for substitution'.format(len(rows)))

    # ------------------------------------------------------------------------------------------------------------------
    def create_routine_loader_helper(self,
                                     routine_name: str,
                                     pystratum_old_metadata: Optional[Dict],
                                     rdbms_old_metadata: Optional[Dict]) -> MsSqlRoutineLoaderHelper:
        """
        Creates a Routine Loader Helper object.

        :param str routine_name: The name of the routine.
        :param dict pystratum_old_metadata: The old metadata of the stored routine from PyStratum.
        :param dict rdbms_old_metadata:  The old metadata of the stored routine from MS SQL Server.

        :rtype: MsSqlRoutineLoaderHelper
        """
        return MsSqlRoutineLoaderHelper(self._io,
                                        self._dl,
                                        self._source_file_names[routine_name],
                                        self._source_file_encoding,
                                        pystratum_old_metadata,
                                        self._replace_pairs,
                                        rdbms_old_metadata)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_old_stored_routine_info(self) -> None:
        """
        Retrieves information about all stored routines.
        """
        rows = self._dl.get_routines()
        self._rdbms_old_metadata = {}
        for row in rows:
            self._rdbms_old_metadata[row['schema_name'] + '.' + row['routine_name']] = row

    # ------------------------------------------------------------------------------------------------------------------
    def _drop_obsolete_routines(self) -> None:
        """
        Drops obsolete stored routines (i.e. stored routines that exits but for which we don't have a source file).
        """
        for routine_name, values in self._rdbms_old_metadata.items():
            if routine_name not in self._source_file_names:
                if values['routine_type'].strip() == 'P':
                    routine_type = 'procedure'
                elif values['routine_type'].strip() in ('FN', 'TF'):
                    routine_type = 'function'
                else:
                    raise Exception("Unknown routine type '{0}'".format(values['routine_type']))

                self._io.writeln("Dropping {0} <dbo>{1}.{2}</dbo>".format(routine_type,
                                                                          values['schema_name'],
                                                                          values['routine_name']))
                self._dl.drop_stored_routine(routine_type, values['schema_name'], values['routine_name'])

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _derive_data_type(column: Dict[str, Any]) -> str:
        """
        Returns the proper SQL declaration of a data type of a column.

        :param dict column: The column of which the field is based.

        :rtype: str
        """
        data_type = column['data_type']

        if data_type in ['bigint',
                         'int',
                         'smallint',
                         'tinyint',
                         'bit',
                         'money',
                         'smallmoney',
                         'float',
                         'real',
                         'date',
                         'datetime',
                         'datetime2',
                         'datetimeoffset',
                         'smalldatetime',
                         'time',
                         'text',
                         'ntext',
                         'binary',
                         'image',
                         'xml',
                         'geography',
                         'geometry',
                         'sysname'
                         ]:
            return data_type

        if data_type in ['decimal', 'numeric']:
            return 'decimal({0:d},{1:d})'.format(column['precision'], column['scale'])

        if data_type == 'char':
            return 'char({0:d})'.format(column['max_length'])

        if data_type == 'varchar':
            if column['max_length'] == -1:
                return 'varchar(max)'

            return 'varchar({0:d})'.format(column['max_length'])

        if data_type == 'nchar':
            return 'nchar({0:d})'.format(int(column['max_length'] / 2))

        if data_type == 'nvarchar':
            if column['max_length'] == -1:
                return 'nvarchar(max)'

            return 'nvarchar({0:d})'.format(int(column['max_length'] / 2))

        if data_type == 'varbinary':
            return 'varbinary({0:d})'.format(column['max_length'])

        raise Exception("Unexpected data type '{0}'".format(data_type))

# ----------------------------------------------------------------------------------------------------------------------

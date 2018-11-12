"""
PyStratum
"""
from pystratum.RoutineLoader import RoutineLoader

from pystratum_mssql.MsSqlConnection import MsSqlConnection
from pystratum_mssql.MsSqlMetadataDataLayer import MsSqlMetadataDataLayer
from pystratum_mssql.MsSqlRoutineLoaderHelper import MsSqlRoutineLoaderHelper


class MsSqlRoutineLoader(MsSqlConnection, RoutineLoader):
    """
    Class for loading stored routines into a SQL Server instance from pseudo SQL files.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io):
        """
        Object constructor.

        :param pystratum.style.PyStratumStyle.PyStratumStyle io: The output decorator.
        """
        RoutineLoader.__init__(self, io)
        MsSqlConnection.__init__(self, io)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_column_type(self):
        """
        Selects schema, table, column names and the column types from the SQL Server instance and saves them as replace
        pairs.
        """
        rows = MsSqlMetadataDataLayer.get_all_table_columns()
        for row in rows:
            key = '@{0}.{1}.{2}%type@'.format(row['schema_name'], row['table_name'], row['column_name'])
            key = key.lower()

            value = self._derive_data_type(row)

            self._replace_pairs[key] = value

        self._io.text('Selected {0} column types for substitution'.format(len(rows)))

    # ------------------------------------------------------------------------------------------------------------------
    def create_routine_loader_helper(self, routine_name, pystratum_old_metadata, rdbms_old_metadata):
        """
        Creates a Routine Loader Helper object.

        :param str routine_name: The name of the routine.
        :param dict pystratum_old_metadata: The old metadata of the stored routine from PyStratum.
        :param dict rdbms_old_metadata:  The old metadata of the stored routine from MS SQL Server.

        :rtype: pystratum.mssql.MsSqlRoutineLoaderHelper.MsSqlRoutineLoaderHelper
        """
        return MsSqlRoutineLoaderHelper(self._source_file_names[routine_name],
                                        self._source_file_encoding,
                                        pystratum_old_metadata,
                                        self._replace_pairs,
                                        rdbms_old_metadata,
                                        self._io)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_old_stored_routine_info(self):
        """
        Retrieves information about all stored routines.
        """
        rows = MsSqlMetadataDataLayer.get_routines()
        self._rdbms_old_metadata = {}
        for row in rows:
            self._rdbms_old_metadata[row['schema_name'] + '.' + row['routine_name']] = row

    # ------------------------------------------------------------------------------------------------------------------
    def _drop_obsolete_routines(self):
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
                MsSqlMetadataDataLayer.drop_stored_routine(routine_type, values['schema_name'], values['routine_name'])

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def _derive_data_type(column):
        """
        Returns the proper SQL declaration of a data type of a column.

        :param dict column: The column of which the field is based.

        :rtype: str
        """
        data_type = column['data_type']

        if data_type == 'bigint':
            return data_type

        if data_type == 'int':
            return data_type

        if data_type == 'smallint':
            return data_type

        if data_type == 'tinyint':
            return data_type

        if data_type == 'bit':
            return data_type

        if data_type == 'money':
            return data_type

        if data_type == 'smallmoney':
            return data_type

        if data_type == 'decimal':
            return 'decimal({0:d},{1:d})'.format(column['precision'], column['scale'])

        if data_type == 'numeric':
            return 'decimal({0:d},{1:d})'.format(column['precision'], column['scale'])

        if data_type == 'float':
            return data_type

        if data_type == 'real':
            return data_type

        if data_type == 'date':
            return data_type

        if data_type == 'datetime':
            return data_type

        if data_type == 'datetime2':
            return data_type

        if data_type == 'datetimeoffset':
            return data_type

        if data_type == 'smalldatetime':
            return data_type

        if data_type == 'time':
            return data_type

        if data_type == 'char':
            return 'char({0:d})'.format(column['max_length'])

        if data_type == 'varchar':
            if column['max_length'] == -1:
                return 'varchar(max)'

            return 'varchar({0:d})'.format(column['max_length'])

        if data_type == 'text':
            return data_type

        if data_type == 'nchar':
            return 'nchar({0:d})'.format(int(column['max_length'] / 2))

        if data_type == 'nvarchar':
            if column['max_length'] == -1:
                return 'nvarchar(max)'

            return 'nvarchar({0:d})'.format(int(column['max_length'] / 2))

        if data_type == 'ntext':
            return data_type

        if data_type == 'binary':
            return data_type

        if data_type == 'varbinary':
            return 'varbinary({0:d})'.format(column['max_length'])

        if data_type == 'image':
            return data_type

        if data_type == 'xml':
            return data_type

        if data_type == 'geography':
            return data_type

        if data_type == 'geometry':
            return data_type

        raise Exception("Unexpected data type '{0}'".format(data_type))

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename):
        """
        Reads parameters from the configuration file.

        :param str config_filename: The name of the configuration file.
        """
        RoutineLoader._read_configuration_file(self, config_filename)
        MsSqlConnection._read_configuration_file(self, config_filename)

# ----------------------------------------------------------------------------------------------------------------------

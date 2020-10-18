"""
PyStratum
"""
import os
import re
from configparser import ConfigParser
from typing import Any, Dict

from pystratum_backend.StratumStyle import StratumStyle
from pystratum_common.backend.CommonConstantWorker import CommonConstantWorker
from pystratum_common.Util import Util

from pystratum_mssql.backend.MsSqlWorker import MsSqlWorker


class MsSqlConstantWorker(MsSqlWorker, CommonConstantWorker):
    """
    Class for creating constants based on column widths, and auto increment columns and labels for SQL Server
    databases.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io: StratumStyle, config: ConfigParser):
        """
        Object constructor.

        :param io: The output decorator.
        """
        MsSqlWorker.__init__(self, io, config)
        CommonConstantWorker.__init__(self, io, config)

        self._columns: Dict[str, Any] = {}
        """
        All columns in the database.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def _get_old_columns(self) -> None:
        """
        Reads from file constants_filename the previous table and column names, the width of the column,
        and the constant name (if assigned) and stores this data in old_columns.
        """
        if os.path.exists(self._constants_filename):
            with open(self._constants_filename, 'r') as f:
                line_number = 0
                for line in f:
                    line_number += 1
                    if line != "\n":
                        p = re.compile(r'\s*(?:([a-zA-Z0-9_]+)\.)?([a-zA-Z0-9_]+)\.'
                                       r'([a-zA-Z0-9_]+)\s+(\d+)\s*(\*|[a-zA-Z0-9_]+)?\s*')
                        matches = p.findall(line)

                        if matches:
                            matches = matches[0]
                            schema_name = str(matches[0])
                            table_name = str(matches[1])
                            column_name = str(matches[2])
                            length = str(matches[3])
                            constant_name = str(matches[4])

                            if constant_name:
                                column_info = {'schema_name':   schema_name,
                                               'table_name':    table_name,
                                               'column_name':   column_name,
                                               'length':        length,
                                               'constant_name': constant_name}
                            else:
                                column_info = {'schema_name': schema_name,
                                               'table_name':  table_name,
                                               'column_name': column_name,
                                               'length':      length}

                            if schema_name in self._old_columns:
                                if table_name in self._old_columns[schema_name]:
                                    if column_name in self._old_columns[schema_name][table_name]:
                                        pass
                                    else:
                                        self._old_columns[schema_name][table_name][column_name] = column_info
                                else:
                                    self._old_columns[schema_name][table_name] = {column_name: column_info}
                            else:
                                self._old_columns[schema_name] = {table_name: {column_name: column_info}}

    # ------------------------------------------------------------------------------------------------------------------
    def _get_columns(self) -> None:
        """
        Retrieves metadata all columns in the database.
        """
        rows = self._dl.get_all_table_columns()
        for row in rows:
            row['length'] = MsSqlConstantWorker.derive_field_length(row)

            if row['schema_name'] in self._columns:
                if row['table_name'] in self._columns[row['schema_name']]:
                    if row['column_name'] in self._columns[row['schema_name']][row['table_name']]:
                        pass
                    else:
                        self._columns[row['schema_name']][row['table_name']][row['column_name']] = row
                else:
                    self._columns[row['schema_name']][row['table_name']] = {row['column_name']: row}
            else:
                self._columns[row['schema_name']] = {row['table_name']: {row['column_name']: row}}

    # ------------------------------------------------------------------------------------------------------------------
    def _enhance_columns(self) -> None:
        """
        Enhances old_columns as follows:
        If the constant name is *, is is replaced with the column name prefixed by prefix in uppercase.
        Otherwise the constant name is set to uppercase.
        """
        if self._old_columns:
            for schema_name, schema in sorted(self._old_columns.items()):
                for table_name, table in sorted(schema.items()):
                    for column_name, column in sorted(table.items()):
                        if 'constant_name' in column:
                            if column['constant_name'].strip() == '*':
                                constant_name = str(self._prefix + column['column_name']).upper()
                                self._old_columns[schema_name][table_name][column_name]['constant_name'] = constant_name
                            else:
                                constant_name = str(
                                        self._old_columns[schema_name][table_name][column_name][
                                            'constant_name']).upper()
                                self._old_columns[schema_name][table_name][column_name]['constant_name'] = constant_name

    # ------------------------------------------------------------------------------------------------------------------
    def _merge_columns(self) -> None:
        """
        Preserves relevant data in old_columns into columns.
        """
        if self._old_columns:
            for schema_name, schema in sorted(self._old_columns.items()):
                for table_name, table in sorted(schema.items()):
                    for column_name, column in sorted(table.items()):
                        if 'constant_name' in column:
                            try:
                                self._columns[schema_name][table_name][column_name]['constant_name'] = \
                                    column['constant_name']
                            except KeyError:
                                # Either the column or table is not present anymore.
                                self._io.warning('Dropping constant {0} because column is not present anymore'.
                                                 format(column['constant_name']))

    # ------------------------------------------------------------------------------------------------------------------
    def _write_columns(self) -> None:
        """
        Writes table and column names, the width of the column, and the constant name (if assigned) to
        constants_filename.
        """
        content = ''

        for schema_name, schema in sorted(self._columns.items()):
            for table_name, table in sorted(schema.items()):
                width1 = 0
                width2 = 0

                key_map = {}
                for column_name, column in table.items():
                    key_map[column['column_id']] = column_name
                    width1 = max(len(str(column['column_name'])), width1)
                    width2 = max(len(str(column['length'])), width2)

                for col_id, column_name in sorted(key_map.items()):
                    if table[column_name]['length'] is not None:
                        if 'constant_name' in table[column_name]:
                            line_format = "%s.%s.%-{0:d}s %{1:d}d %s\n".format(int(width1), int(width2))
                            content += line_format % (schema_name,
                                                      table[column_name]['table_name'],
                                                      table[column_name]['column_name'],
                                                      table[column_name]['length'],
                                                      table[column_name]['constant_name'])
                        else:
                            line_format = "%s.%s.%-{0:d}s %{1:d}d\n".format(int(width1), int(width2))
                            content += line_format % (schema_name,
                                                      table[column_name]['table_name'],
                                                      table[column_name]['column_name'],
                                                      table[column_name]['length'])

                content += "\n"""

        # Save the columns, width, and constants to the filesystem.
        Util.write_two_phases(self._constants_filename, content, self._io)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_labels(self) -> None:
        """
        Gets all primary key labels from the database.
        """
        tables = self._dl.get_label_tables(self._label_regex)

        for table in tables:
            rows = self._dl.get_labels_from_table(table['database'],
                                                  table['schema_name'],
                                                  table['table_name'],
                                                  table['id'],
                                                  table['label'])
            for row in rows:
                if row['label'] not in self._labels:
                    self._labels[row['label']] = row['id']
                else:
                    # todo improve exception.
                    Exception("Duplicate label '%s'")

    # ------------------------------------------------------------------------------------------------------------------
    def _fill_constants(self) -> None:
        """
        Merges columns and labels (i.e. all known constants) into constants.
        """
        for schema_name, schema in sorted(self._columns.items()):
            for table_name, table in sorted(schema.items()):
                for column_name, column in sorted(table.items()):
                    if 'constant_name' in column:
                        self._constants[column['constant_name']] = column['length']

        for label, label_id in sorted(self._labels.items()):
            self._constants[label] = label_id

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def derive_field_length(column: Dict[str, Any]) -> int:
        """
        Returns the width of a field based based on the data type of column.

        :param dict column: Info about the column.

        :rtype: int
        """
        data_type = column['data_type']

        if data_type in ['bigint',
                         'int',
                         'smallint',
                         'tinyint',
                         'money',
                         'smallmoney',
                         'decimal',
                         'numeric',
                         'float',
                         'real',
                         'date',
                         'datetime',
                         'datetime2',
                         'datetimeoffset',
                         'smalldatetime',
                         'time']:
            return column['precision']

        if data_type in ['bit',
                         'char',
                         'binary',
                         'varbinary',
                         'sysname']:
            return column['max_length']

        if data_type == 'varchar':
            if column['max_length'] == -1:
                # This is a varchar(max) data type.
                return 2147483647

            return column['max_length']

        if data_type == 'nvarchar':
            if column['max_length'] == -1:
                # This is a nvarchar(max) data type.
                return 1073741823

            return column['max_length'] / 2

        if data_type in ['text', 'image', 'xml']:
            return 2147483647

        if data_type == 'nchar':
            return column['max_length'] / 2

        if data_type == 'ntext':
            return 1073741823

        if data_type in ['geography', 'geometry']:
            if column['max_length'] == -1:
                return 2147483647

        raise Exception("Unexpected data type '{0}'".format(data_type))

# ----------------------------------------------------------------------------------------------------------------------

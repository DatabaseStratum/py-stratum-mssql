"""
PyStratum
"""

from pystratum.helper.DataTypeHelper import DataTypeHelper


class MsSqlDataTypeHelper(DataTypeHelper):
    """
    Utility class for deriving information based on a SQL Server data type.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def column_type_to_python_type(self, data_type_info):
        """
        Returns the corresponding Python data type of a SQL Server data type.

        :param dict data_type_info: The SQL Server data type metadata.

        :rtype: str
        """
        if data_type_info['data_type'] in ['bigint',
                                           'bit',
                                           'int',
                                           'smallint',
                                           'tinyint']:
            return 'int'

        if data_type_info['data_type'] == 'decimal':
            return 'int' if data_type_info['numeric_scale'] == 0 else 'float'

        if data_type_info['data_type'] in ['float',
                                           'real']:
            return 'float'

        if data_type_info['data_type'] in ['char',
                                           'date',
                                           'datetime',
                                           'datetime2',
                                           'datetimeoffset',
                                           'money',
                                           'nchar',
                                           'ntext',
                                           'nvarchar',
                                           'smalldatetime',
                                           'smallmoney',
                                           'text',
                                           'time',
                                           'timestamp',
                                           'tinytext',
                                           'varchar',
                                           'xml']:
            return 'str'

        if data_type_info['data_type'] in ['binary',
                                           'image',
                                           'varbinary']:
            return 'bytes'

        raise RuntimeError('Unknown data type {0}'.format(data_type_info['data_type']))

# ----------------------------------------------------------------------------------------------------------------------

import re

from pystratum_backend.StratumStyle import StratumStyle
from pystratum_common.exception.LoaderException import LoaderException
from pystratum_common.helper.DataTypeHelper import DataTypeHelper
from pystratum_common.helper.RoutineLoaderHelper import RoutineLoaderHelper

from pystratum_mssql.helper.MsSqlDataTypeHelper import MsSqlDataTypeHelper
from pystratum_mssql.MsSqlMetadataDataLayer import MsSqlMetadataDataLayer


class MsSqlRoutineLoaderHelper(RoutineLoaderHelper):
    """
    Class for loading a single stored routine into a SQL Server instance from a (pseudo) SQL file.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self,
                 io: StratumStyle,
                 dl: MsSqlMetadataDataLayer,
                 routine_filename,
                 routine_file_encoding,
                 pystratum_old_metadata,
                 replace_pairs,
                 rdbms_old_metadata):
        """
        Object constructor.

        :param str routine_filename: The filename of the source of the stored routine.
        :param str routine_file_encoding: The encoding of the source file.
        :param dict pystratum_old_metadata: The metadata of the stored routine from PyStratum.
        :param dict[str,str] replace_pairs: A map from placeholders to their actual values.
        :param dict rdbms_old_metadata: The old metadata of the stored routine from MS SQL Server.
        :param pystratum.style.PyStratumStyle.PyStratumStyle io: The output decorator.
        """
        RoutineLoaderHelper.__init__(self,
                                     io,
                                     routine_filename,
                                     routine_file_encoding,
                                     pystratum_old_metadata,
                                     replace_pairs,
                                     rdbms_old_metadata)

        self._routine_base_name: str = ''
        """
        The name of the stored routine without schema name.
        """

        self._routines_schema_name: str = ''
        """
        The name of the schema of the stored routine.
        """

        self._dl: MsSqlMetadataDataLayer = dl
        """
        The metadata layer.
        """

    # ------------------------------------------------------------------------------------------------------------------
    def _drop_routine(self) -> None:
        """
        Drops the stored routine if it exists.
        """
        if self._rdbms_old_metadata:
            if self._rdbms_old_metadata['routine_type'].strip() == 'P':
                routine_type = 'procedure'
            elif self._rdbms_old_metadata['routine_type'].strip() in ('FN', 'TF'):
                routine_type = 'function'
            else:
                raise Exception("Unknown routine type '{0}'.".format(self._rdbms_old_metadata['routine_type']))

            self._dl.drop_stored_routine(routine_type,
                                         self._rdbms_old_metadata['schema_name'],
                                         self._routine_base_name)

    # ------------------------------------------------------------------------------------------------------------------
    def _get_bulk_insert_table_columns_info(self) -> None:
        """
        Gets the column names and column types of the current table for bulk insert.
        """
        raise NotImplementedError()

    # ------------------------------------------------------------------------------------------------------------------
    def _get_data_type_helper(self) -> DataTypeHelper:
        """
        Returns a data type helper object for SQL Server.

        :rtype: pystratum.helper.DataTypeHelper.DataTypeHelper
        """
        return MsSqlDataTypeHelper()

    # ------------------------------------------------------------------------------------------------------------------
    def _get_name(self) -> None:
        """
        Extracts the name of the stored routine and the stored routine type (i.e. procedure or function) source.
        """
        p = re.compile(r"create\s+(procedure|function)\s+(?:(\w+)\.([a-zA-Z0-9_]+))", re.IGNORECASE)
        matches = p.findall(self._routine_source_code)

        if matches:
            self._routine_type = matches[0][0].lower()
            self._routines_schema_name = matches[0][1]
            self._routine_base_name = matches[0][2]

            if self._routine_name != (matches[0][1] + '.' + matches[0][2]):
                raise LoaderException(
                        'Stored routine name {0}.{1} does not match filename in file {2}'.format(matches[0][1],
                                                                                                 matches[0][2],
                                                                                                 self._source_filename))

        if not self._routine_type:
            raise LoaderException('Unable to find the stored routine name and type in file {0}'.
                                  format(self._source_filename))

    # ------------------------------------------------------------------------------------------------------------------
    def _get_routine_parameters_info(self) -> None:
        """
        Retrieves information about the stored routine parameters from the meta data of SQL Server.
        """
        routine_parameters = self._dl.get_routine_parameters(self._routines_schema_name,
                                                             self._routine_base_name)
        if len(routine_parameters) != 0:
            for routine_parameter in routine_parameters:
                if routine_parameter['parameter_name']:
                    parameter_name = routine_parameter['parameter_name'][1:]
                    value = routine_parameter['type_name']

                    self._parameters.append({'name':                 parameter_name,
                                             'data_type':            routine_parameter['type_name'],
                                             'numeric_precision':    routine_parameter['precision'],
                                             'numeric_scale':        routine_parameter['scale'],
                                             'data_type_descriptor': value})

    # ------------------------------------------------------------------------------------------------------------------
    def _is_start_of_stored_routine(self, line: str) -> bool:
        """
        Returns True if a line is the start of the code of the stored routine.

        :param str line: The line with source code of the stored routine.

        :rtype: bool
        """
        return re.match(r'^\s*create\s+(procedure|function)', line, re.IGNORECASE) is not None

    # ------------------------------------------------------------------------------------------------------------------
    def _is_start_of_stored_routine_body(self, line: str) -> bool:
        """
        Returns True if a line is the start of the body of the stored routine.

        :param str line: The line with source code of the stored routine.

        :rtype: bool
        """
        return re.match(r'^\s*as', line, re.IGNORECASE) is not None

    # ------------------------------------------------------------------------------------------------------------------
    def _load_routine_file(self) -> None:
        """
        Loads the stored routine into the SQL Server instance.
        """
        self._io.text('Loading {0} <dbo>{1}</dbo>'.format(self._routine_type, self._routine_name))

        self._set_magic_constants()

        routine_source = []
        i = 0
        for line in self._routine_source_code_lines:
            new_line = line
            self._replace['__LINE__'] = "'%d'" % (i + 1)
            for search, replace in self._replace.items():
                tmp = re.findall(search, new_line, re.IGNORECASE)
                if tmp:
                    new_line = new_line.replace(tmp[0], replace)
            routine_source.append(new_line)
            i += 1

        routine_source = "\n".join(routine_source)

        self._unset_magic_constants()

        if self._rdbms_old_metadata:
            if self._pystratum_old_metadata and self._pystratum_old_metadata['designation'] == \
                    self._pystratum_metadata['designation']:
                p = re.compile(r'(create\s+(procedure|function))', re.IGNORECASE)
                matches = p.findall(routine_source)
                if matches:
                    routine_source = routine_source.replace(matches[0][0], 'alter %s' % matches[0][1])
                else:
                    raise LoaderException("Unable to find the stored routine type in modified source of file '{0}'".
                                          format(self._source_filename))
            else:
                self._drop_routine()

        self._dl.execute_none(routine_source)
        self._dl.commit()

    # ------------------------------------------------------------------------------------------------------------------
    def _must_reload(self) -> bool:
        """
        Returns True if the source file must be load or reloaded. Otherwise returns False.

        :rtype: bool
        """
        if not self._pystratum_old_metadata:
            return True

        if self._pystratum_old_metadata['timestamp'] != self._m_time:
            return True

        if self._pystratum_old_metadata['replace']:
            for key, value in self._pystratum_old_metadata['replace'].items():
                if key.lower() not in self._replace_pairs or self._replace_pairs[key.lower()] != value:
                    return True

        if not self._rdbms_old_metadata:
            return True

        return False

    # ------------------------------------------------------------------------------------------------------------------
    def _update_metadata(self) -> None:
        """
        Updates the metadata of the stored routine.
        """
        # Update general metadata.
        RoutineLoaderHelper._update_metadata(self)

        # Update SQL Server specific metadata.
        self._pystratum_metadata['schema_name'] = self._routines_schema_name

        # Update SQL Server specific metadata.
        self._pystratum_metadata['routine_base_name'] = self._routine_base_name

# ----------------------------------------------------------------------------------------------------------------------

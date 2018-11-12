"""
PyStratum
"""
from pystratum.RoutineWrapperGenerator import RoutineWrapperGenerator

from pystratum_mssql.MsSqlConnection import MsSqlConnection
from pystratum_mssql.wrapper import create_routine_wrapper


class MsSqlRoutineWrapperGenerator(MsSqlConnection, RoutineWrapperGenerator):
    """
    Class for generating a class with wrapper methods for calling stored routines in a SQL Server database.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def __init__(self, io):
        """
        Object constructor.

        :param pystratum.style.PyStratumStyle.PyStratumStyle io: The output decorator.
        """
        MsSqlConnection.__init__(self, io)
        RoutineWrapperGenerator.__init__(self, io)

    # ------------------------------------------------------------------------------------------------------------------
    def _read_configuration_file(self, config_filename):
        """
        Reads parameters from the configuration file.

        :param str config_filename: The name of the configuration file.
        """
        MsSqlConnection._read_configuration_file(self, config_filename)
        RoutineWrapperGenerator._read_configuration_file(self, config_filename)

    # ------------------------------------------------------------------------------------------------------------------
    def _write_routine_function(self, routine):
        """
        Generates a complete wrapper method for a stored routine.

        :param dict routine: The metadata of the stored routine.
        """
        wrapper = create_routine_wrapper(routine, self._lob_as_string_flag)
        self._code += wrapper.write_routine_method(routine)

# ----------------------------------------------------------------------------------------------------------------------

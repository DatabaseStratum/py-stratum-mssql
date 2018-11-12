"""
PyStratum
"""
from pystratum.wrapper.Singleton0Wrapper import Singleton0Wrapper

from pystratum_mssql.wrapper.MsSqlWrapper import MsSqlWrapper


class MsSqlSingleton0Wrapper(MsSqlWrapper, Singleton0Wrapper):
    """
    Wrapper method generator for stored procedures that are selecting 0 or 1 row with one column only.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_singleton0({0})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------

"""
PyStratum
"""
from pystratum.wrapper.Singleton1Wrapper import Singleton1Wrapper

from pystratum_mssql.wrapper.MsSqlWrapper import MsSqlWrapper


class MsSqlSingleton1Wrapper(MsSqlWrapper, Singleton1Wrapper):
    """
    Wrapper method generator for stored procedures that are selecting 1 row with one column only.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line(
            'return StaticDataLayer.execute_singleton1({0})'.format(str(self._generate_command(routine))))

# ----------------------------------------------------------------------------------------------------------------------

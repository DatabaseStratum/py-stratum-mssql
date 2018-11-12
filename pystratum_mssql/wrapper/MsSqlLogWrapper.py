"""
PyStratum
"""
from pystratum.wrapper.LogWrapper import LogWrapper

from pystratum_mssql.wrapper.MsSqlWrapper import MsSqlWrapper


class MsSqlLogWrapper(MsSqlWrapper, LogWrapper):
    """
    Wrapper method generator for stored procedures with designation type log.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_log({0})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------

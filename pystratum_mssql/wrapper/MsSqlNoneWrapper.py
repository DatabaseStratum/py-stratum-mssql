"""
PyStratum
"""
from pystratum.wrapper.NoneWrapper import NoneWrapper

from pystratum_mssql.wrapper.MsSqlWrapper import MsSqlWrapper


class MsSqlNoneWrapper(MsSqlWrapper, NoneWrapper):
    """
    Wrapper method generator for stored procedures without any result set.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_sp_none({0})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------

"""
PyStratum
"""
from pystratum.wrapper.FunctionsWrapper import FunctionsWrapper

from pystratum_mssql.wrapper.MsSqlWrapper import MsSqlWrapper


class MsSqlFunctionsWrapper(MsSqlWrapper, FunctionsWrapper):
    """
    Wrapper method generator for stored functions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_sp_singleton1({0})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------

from typing import Any, Dict

from pystratum_common.wrapper.FunctionsWrapper import FunctionsWrapper

from pystratum_mssql.wrapper.MsSqlWrapper import MsSqlWrapper


class MsSqlFunctionsWrapper(MsSqlWrapper, FunctionsWrapper):
    """
    Wrapper method generator for stored functions.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine: Dict[str, Any]) -> None:
        self._write_line('return self.execute_sp_singleton1({0})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------

from typing import Any, Dict

from pystratum_common.wrapper.NoneWrapper import NoneWrapper

from pystratum_mssql.wrapper.MsSqlWrapper import MsSqlWrapper


class MsSqlNoneWrapper(MsSqlWrapper, NoneWrapper):
    """
    Wrapper method generator for stored procedures without any result set.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine: Dict[str, Any]) -> None:
        self._write_line('return self.execute_sp_none({0})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------

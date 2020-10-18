from typing import Any, Dict

from pystratum_common.wrapper.RowsWrapper import RowsWrapper

from pystratum_mssql.wrapper.MsSqlWrapper import MsSqlWrapper


class MsSqlRowsWrapper(MsSqlWrapper, RowsWrapper):
    """
    Wrapper method generator for stored procedures that are selecting 0, 1, or more rows.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine: Dict[str, Any]) -> None:
        self._write_line('return self.execute_sp_rows({0})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------

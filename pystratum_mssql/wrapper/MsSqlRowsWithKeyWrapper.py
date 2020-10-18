from typing import Any, Dict

from pystratum_common.wrapper.RowsWithKeyWrapper import RowsWithKeyWrapper

from pystratum_mssql.wrapper.MsSqlWrapper import MsSqlWrapper


class MsSqlRowsWithKeyWrapper(RowsWithKeyWrapper, MsSqlWrapper):
    """
    Wrapper method generator for stored procedures whose result set must be returned using tree structure using a
    combination of unique columns.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_execute_rows(self, routine: Dict[str, Any]) -> None:
        self._write_line('rows = self.execute_sp_rows({0})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------

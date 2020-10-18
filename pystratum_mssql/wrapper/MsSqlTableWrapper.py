from typing import Any, Dict

from pystratum_common.wrapper.TableWrapper import TableWrapper

from pystratum_mssql.wrapper.MsSqlWrapper import MsSqlWrapper


class MsSqlTableWrapper(MsSqlWrapper, TableWrapper):
    """
    Wrapper method generator for printing the result set of stored procedures in a table format.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine: Dict[str, Any]) -> None:
        self._write_line('return self.execute_table({0})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------

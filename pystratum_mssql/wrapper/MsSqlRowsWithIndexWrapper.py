"""
PyStratum
"""
from pystratum_mssql.wrapper.MsSqlWrapper import MsSqlWrapper
from pystratum.wrapper.RowsWithIndexWrapper import RowsWithIndexWrapper as BaseRowsWithIndexWrapper


class MsSqlRowsWithIndexWrapper(BaseRowsWithIndexWrapper, MsSqlWrapper):
    """
    Wrapper method generator for stored procedures whose result set must be returned using tree structure using a
    combination of non-unique columns.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_execute_rows(self, routine):
        self._write_line('rows = StaticDataLayer.execute_rows({0})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------

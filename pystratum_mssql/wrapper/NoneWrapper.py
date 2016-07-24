"""
PyStratum

Copyright 2015-2016 Set Based IT Consultancy

Licence MIT
"""
from pystratum_mssql.wrapper.MsSqlWrapper import MsSqlWrapper


class NoneWrapper(MsSqlWrapper):
    """
    Wrapper method generator for stored procedures without any result set.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def _write_result_handler(self, routine):
        self._write_line('return StaticDataLayer.execute_none({0!s})'.format(self._generate_command(routine)))

# ----------------------------------------------------------------------------------------------------------------------

from typing import Any, Dict, List, Optional, Union

from pystratum_mssql.MsSqlDataLayer import MsSqlDataLayer


class TestDataLayer(MsSqlDataLayer):
    """
    The stored routines wrappers.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def tst_magic_constant01(self):
        return self.execute_sp_singleton1('exec [dbo].[tst_magic_constant01]')

    # ------------------------------------------------------------------------------------------------------------------
    def tst_magic_constant02(self):
        return self.execute_sp_singleton1('exec [dbo].[tst_magic_constant02]')

    # ------------------------------------------------------------------------------------------------------------------
    def tst_magic_constant03(self):
        return self.execute_sp_singleton1('exec [dbo].[tst_magic_constant03]')

    # ------------------------------------------------------------------------------------------------------------------
    def tst_magic_constant04(self):
        return self.execute_sp_singleton1('exec [dbo].[tst_magic_constant04]')

    # ------------------------------------------------------------------------------------------------------------------
    def tst_parameter_types01(self, p_tst_bigint: Optional[int], p_tst_binary: Optional[bytes], p_tst_bit: Optional[int], p_tst_char: Optional[str], p_tst_date: Optional[str], p_tst_datetime: Optional[str], p_tst_datetime2: Optional[str], p_tst_datetimeoffset: Optional[str], p_tst_decimal: Optional[float], p_tst_float: Optional[float], p_tst_int: Optional[int], p_tst_money: Optional[str], p_tst_nchar: Optional[str], p_tst_numeric: Optional[float], p_tst_nvarchar: Optional[str], p_tst_real: Optional[float], p_tst_smalldatetime: Optional[str], p_tst_smallint: Optional[int], p_tst_smallmoney: Optional[str], p_tst_time: Optional[str], p_tst_tinyint: Optional[int], p_tst_varbinary: Optional[bytes], p_tst_varchar: Optional[str]):
        return self.execute_sp_none('exec [dbo].[tst_parameter_types01] %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s', p_tst_bigint, p_tst_binary, p_tst_bit, p_tst_char, p_tst_date, p_tst_datetime, p_tst_datetime2, p_tst_datetimeoffset, p_tst_decimal, p_tst_float, p_tst_int, p_tst_money, p_tst_nchar, p_tst_numeric, p_tst_nvarchar, p_tst_real, p_tst_smalldatetime, p_tst_smallint, p_tst_smallmoney, p_tst_time, p_tst_tinyint, p_tst_varbinary, p_tst_varchar)

    # ------------------------------------------------------------------------------------------------------------------
    def tst_parameter_types02(self, tst_bigint: Optional[int], tst_int: Optional[int], tst_smallint: Optional[int], tst_tinyint: Optional[int], tst_bit: Optional[int], tst_money: Optional[str], tst_smallmoney: Optional[str], tst_decimal: Optional[float], tst_numeric: Optional[float], tst_float: Optional[float], tst_real: Optional[float], tst_date: Optional[str], tst_datetime: Optional[str], tst_datetime2: Optional[str], tst_datetimeoffset: Optional[str], tst_smalldatetime: Optional[str], tst_time: Optional[str], tst_char: Optional[str], tst_varchar: Optional[str], tst_text: Optional[str], tst_nchar: Optional[str], tst_nvarchar: Optional[str], tst_ntext: Optional[str], tst_binary: Optional[bytes], tst_varbinary: Optional[bytes], tst_image: Optional[bytes], tst_xml: Optional[str]):
        return self.execute_sp_none('exec [dbo].[tst_parameter_types02] %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s', tst_bigint, tst_int, tst_smallint, tst_tinyint, tst_bit, tst_money, tst_smallmoney, tst_decimal, tst_numeric, tst_float, tst_real, tst_date, tst_datetime, tst_datetime2, tst_datetimeoffset, tst_smalldatetime, tst_time, tst_char, tst_varchar, tst_text, tst_nchar, tst_nvarchar, tst_ntext, tst_binary, tst_varbinary, tst_image, tst_xml)

    # ------------------------------------------------------------------------------------------------------------------
    def tst_test_function(self, p_a: Optional[int], p_b: Optional[int]):
        return self.execute_sp_singleton1('select [dbo].[tst_test_function](%s, %s)', p_a, p_b)

    # ------------------------------------------------------------------------------------------------------------------
    def tst_test_none0(self, p_tst_test: Optional[str], p_tst_label: Optional[str]):
        return self.execute_sp_none('exec [dbo].[tst_test_none0] %s, %s', p_tst_test, p_tst_label)

    # ------------------------------------------------------------------------------------------------------------------
    def tst_test_none1(self):
        return self.execute_sp_none('exec [dbo].[tst_test_none1]')

    # ------------------------------------------------------------------------------------------------------------------
    def tst_test_row0(self, p_count: Optional[int]):
        return self.execute_sp_row0('exec [dbo].[tst_test_row0] %s', p_count)

    # ------------------------------------------------------------------------------------------------------------------
    def tst_test_row1(self, p_count: Optional[int]):
        return self.execute_sp_row1('exec [dbo].[tst_test_row1] %s', p_count)

    # ------------------------------------------------------------------------------------------------------------------
    def tst_test_rows(self, p_count: Optional[int]):
        return self.execute_sp_rows('exec [dbo].[tst_test_rows] %s', p_count)

    # ------------------------------------------------------------------------------------------------------------------
    def tst_test_rows_with_index1(self, p_count: Optional[int]):
        ret = {}
        rows = self.execute_sp_rows('exec [dbo].[tst_test_rows_with_index1] %s', p_count)
        for row in rows:
            if row['tst_c01'] in ret:
                if row['tst_c02'] in ret[row['tst_c01']]:
                    ret[row['tst_c01']][row['tst_c02']].append(row)
                else:
                    ret[row['tst_c01']][row['tst_c02']] = [row]
            else:
                ret[row['tst_c01']] = {row['tst_c02']: [row]}

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def tst_test_rows_with_key1(self, p_count: Optional[int]):
        ret = {}
        rows = self.execute_sp_rows('exec [dbo].[tst_test_rows_with_key1] %s', p_count)
        for row in rows:
            if row['tst_c01'] in ret:
                if row['tst_c02'] in ret[row['tst_c01']]:
                    if row['tst_c03'] in ret[row['tst_c01']][row['tst_c02']]:
                        raise Exception('Duplicate key for %s.' % str((row['tst_c01'], row['tst_c02'], row['tst_c03'])))
                    else:
                        ret[row['tst_c01']][row['tst_c02']][row['tst_c03']] = row
                else:
                    ret[row['tst_c01']][row['tst_c02']] = {row['tst_c03']: row}
            else:
                ret[row['tst_c01']] = {row['tst_c02']: {row['tst_c03']: row}}

        return ret

    # ------------------------------------------------------------------------------------------------------------------
    def tst_test_singleton0(self, p_count: Optional[int]):
        return self.execute_sp_singleton0('exec [dbo].[tst_test_singleton0] %s', p_count)

    # ------------------------------------------------------------------------------------------------------------------
    def tst_test_singleton1(self, p_count: Optional[int]):
        return self.execute_sp_singleton1('exec [dbo].[tst_test_singleton1] %s', p_count)


# ----------------------------------------------------------------------------------------------------------------------

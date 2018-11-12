from pystratum_mssql.wrapper.MsSqlFunctionsWrapper import MsSqlFunctionsWrapper
from pystratum_mssql.wrapper.MsSqlLogWrapper import MsSqlLogWrapper
from pystratum_mssql.wrapper.MsSqlNoneWrapper import MsSqlNoneWrapper
from pystratum_mssql.wrapper.MsSqlRow0Wrapper import MsSqlRow0Wrapper
from pystratum_mssql.wrapper.MsSqlRow1Wrapper import MsSqlRow1Wrapper
from pystratum_mssql.wrapper.MsSqlRowsWithIndexWrapper import MsSqlRowsWithIndexWrapper
from pystratum_mssql.wrapper.MsSqlRowsWithKeyWrapper import MsSqlRowsWithKeyWrapper
from pystratum_mssql.wrapper.MsSqlRowsWrapper import MsSqlRowsWrapper
from pystratum_mssql.wrapper.MsSqlSingleton0Wrapper import MsSqlSingleton0Wrapper
from pystratum_mssql.wrapper.MsSqlSingleton1Wrapper import MsSqlSingleton1Wrapper


def create_routine_wrapper(routine, lob_as_string_flag):
    """
    A factory for creating the appropriate object for generating a wrapper method for a stored routine.
    
    :param dict[str,str] routine: The metadata of the sored routine. 
    :param bool lob_as_string_flag: If True BLOBs and CLOBs must be treated as strings.

    :rtype: pystratum.mssql.wrapper.MsSqlWrapper.MsSqlWrapper
    """
    if routine['designation'] == 'none':
        wrapper = MsSqlNoneWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'row0':
        wrapper = MsSqlRow0Wrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'row1':
        wrapper = MsSqlRow1Wrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'rows':
        wrapper = MsSqlRowsWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'rows_with_index':
        wrapper = MsSqlRowsWithIndexWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'rows_with_key':
        wrapper = MsSqlRowsWithKeyWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'singleton0':
        wrapper = MsSqlSingleton0Wrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'singleton1':
        wrapper = MsSqlSingleton1Wrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'function':
        wrapper = MsSqlFunctionsWrapper(routine, lob_as_string_flag)
    elif routine['designation'] == 'log':
        wrapper = MsSqlLogWrapper(routine, lob_as_string_flag)
    else:
        raise Exception("Unknown routine type '{0!s}'.".format(routine['designation']))

    return wrapper

    # ----------------------------------------------------------------------------------------------------------------------

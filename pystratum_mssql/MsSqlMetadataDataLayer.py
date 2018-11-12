"""
PyStratum
"""
from pystratum.MetadataDataLayer import MetadataDataLayer

from pystratum_mssql.StaticDataLayer import StaticDataLayer


class MsSqlMetadataDataLayer(MetadataDataLayer):
    """
    Data layer for retrieving metadata and loading stored routines.
    """
    __dl = None
    """
    The connection to the SQL Server instance.

    :type: pystratum_mssql.StaticDataLayer.StaticDataLayer|None
    """

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def connect(server, user, password, database):
        """
        Connects to a SQL Server instance.
        """
        MsSqlMetadataDataLayer.__dl = StaticDataLayer()
        MsSqlMetadataDataLayer.__dl.connect(server, user, password, database)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def disconnect():
        """
        Disconnects from the SQL Server instance.
        """
        MsSqlMetadataDataLayer.__dl.disconnect()

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def drop_stored_routine(routine_type, schema_name, routine_name):
        """
        Drops a stored routine if it exists.

        :param str routine_type: The type of the routine (i.e. procedure or function).
        :param str schema_name: The name of the schema.
        :param str routine_name: The name of the routine.
        """
        sql = "drop {0} [{1}].[{2}]".format(routine_type, schema_name, routine_name)

        MsSqlMetadataDataLayer.execute_none(sql)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def drop_temporary_table(table_name):
        """
        Drops a temporary table.

        :param str table_name: The name of the table.
        """
        sql = 'drop temporary table `{0}`'.format(table_name)

        MsSqlMetadataDataLayer.execute_none(sql)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_none(query):
        """
        Executes a query that does not select any rows.

        :param str query: The query.

        :rtype: int
        """
        MsSqlMetadataDataLayer._log_query(query)

        return MsSqlMetadataDataLayer.__dl.execute_none(query)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def execute_rows(query):
        """
        Executes a query that selects 0 or more rows. Returns the selected rows (an empty list if no rows are selected).

        :param str query: The query.

        :rtype: list[dict[str,*]]
        """
        MsSqlMetadataDataLayer._log_query(query)

        return MsSqlMetadataDataLayer.__dl.execute_rows(query)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_all_table_columns():
        """
        Selects metadata of all columns of all tables.

        :rtype: list[dict[str,*]]
        """
        sql = """
select scm.name                   as schema_name
,      tab.name                   as table_name
,      col.name                   as column_name
,      isnull(stp.name,utp.name)  as data_type
,      col.max_length
,      col.precision
,      col.scale
,      col.column_id
from            sys.columns col
inner join      sys.types   utp  on  utp.user_type_id = col.user_type_id and
                                     utp.system_type_id = col.system_type_id
left outer join sys.types   stp  on  utp.is_user_defined = 1 and
                                     stp.is_user_defined = 0 and
                                     utp.system_type_id = stp.system_type_id and
                                     utp.user_type_id <> stp.user_type_id  and
                                     stp.user_type_id = stp.system_type_id
inner join      sys.tables  tab  on  col.object_id = tab.object_id
inner join      sys.schemas scm  on  tab.schema_id = scm.schema_id
where tab.type in ('U','S','V')
order by  scm.name
,         tab.name
,         col.column_id
"""

        return MsSqlMetadataDataLayer.execute_rows(sql)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_label_tables(regex):
        """
        Selects metadata of tables with a label column.

        :param str regex: The regular expression for columns which we want to use.

        :rtype: list[dict[str,*]]
        """
        sql = """
select scm.name  schema_name
,      tab.name  table_name
,      cl1.name  label
,      cl2.name  id
from       sys.schemas     scm
inner join sys.tables      tab  on  tab.[schema_id] = scm.[schema_id]
inner join sys.all_columns cl1  on  cl1.[object_id] = tab.[object_id]
inner join sys.all_columns cl2  on  cl2.[object_id] = tab.[object_id]
where cl1.name like '{0}'
and   cl2.is_identity = 1""".format(regex)

        return MsSqlMetadataDataLayer.execute_rows(sql)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_labels_from_table(database_name, schema_name, table_name, id_column_name, label_column_name):
        """
        Selects all labels from a table with labels.

        :param str database_name: The name of the database.
        :param str schema_name: The name of the schema.
        :param str table_name: The name of the table.
        :param str id_column_name: The name of the auto increment column.
        :param str label_column_name: The name of the column with labels.

        :rtype: list[dict[str,*]]
        """
        sql = """
select tab.[{0!s}] id
,      tab.[{1!s}] label
from   [{2!s}].[{3!s}].[{4!s}] tab
where  nullif(tab.[{1!s}],'') is not null""".format(id_column_name,
                                                    label_column_name,
                                                    database_name,
                                                    schema_name,
                                                    table_name)

        return MsSqlMetadataDataLayer.execute_rows(sql)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_routine_parameters(schema_name, routine_name):
        """
        Selects metadata of the parameters of a stored routine.

        :param str schema_name: The name of the schema.
        :param str routine_name: The name of the routine.

        :rtype: list[dict[str,*]]
        """
        sql = """
select par.name      parameter_name
,      typ.name      type_name
,      typ.max_length
,      typ.precision
,      typ.scale
from       sys.schemas        scm
inner join sys.all_objects    prc  on  prc.[schema_id] = scm.[schema_id]
inner join sys.all_parameters par  on  par.[object_id] = prc.[object_id]
inner join sys.types          typ  on  typ.user_type_id = par.system_type_id
where scm.name = '%s'
and   prc.name = '%s'
order by par.parameter_id""" % (schema_name, routine_name)

        return MsSqlMetadataDataLayer.execute_rows(sql)

    # ------------------------------------------------------------------------------------------------------------------
    @staticmethod
    def get_routines():
        """
        Selects metadata of all routines.

        :rtype: list[dict[str,*]]
        """
        sql = """
select scm.name as schema_name
,      prc.name as routine_name
,      prc.type as routine_type
from       sys.all_objects  prc
inner join sys.schemas     scm  on   scm.schema_id = prc.schema_id
where prc.type in ('P','FN','TF')
and   scm.name <> 'sys'
and   prc.is_ms_shipped=0"""

        return MsSqlMetadataDataLayer.execute_rows(sql)

# ----------------------------------------------------------------------------------------------------------------------

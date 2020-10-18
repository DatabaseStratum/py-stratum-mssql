from cleo import CommandTester
from pystratum_cli import StratumApplication

from test.StratumTestCase import StratumTestCase


class AAATest(StratumTestCase):
    """
    This test must run before all other tests because this test loads the stored routines.
    """

    # ------------------------------------------------------------------------------------------------------------------
    def test0(self):
        """
        Create tables.
        """
        with open('test/ddl/create_tables.sql') as file:
            sql = file.read()
            self._dl.execute_none(sql)
            self._dl.commit()

        with open('test/ddl/insert_data.sql') as file:
            sql = file.read()
            self._dl.execute_none(sql)
            self._dl.commit()

    # ------------------------------------------------------------------------------------------------------------------
    def test1(self):
        """
        Runs the stratum command: loads the stored routines and generates the stored routine wrapper.
        """
        application = StratumApplication()
        command = application.find('stratum')
        command_tester = CommandTester(command)
        status = command_tester.execute([('command', command.get_name()),
                                         ('config_file', 'test/etc/stratum.cfg')])

        print(command_tester.get_display())

        self.assertEqual(0, status)

# ----------------------------------------------------------------------------------------------------------------------

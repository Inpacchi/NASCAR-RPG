import sys
from os.path import dirname, abspath
import unittest

from utilities import futil, gutil
from models.driver import Driver
from models.team import Team


class ModelTest(unittest.TestCase):
    def testDriverUtilities(self) -> None:
        """
        Tests core file utilities functions for driver model types.

        Tests the following core application functions:
            * convert_csv_to_json()
            * write_dict_to_json()
            * read_dict_from_json()
            * conversion from list to Driver model
            * conversion from Driver model to dictionary

        By default, the following core package functions are tested:
            * _json_file()
            * _csv_file()

        :return: None
        """

        print('========================= Begin Driver Utility Test =========================')
        futil.convert_csv_to_json('testdriver')

        drivers_from_csv = {}
        for driver in Driver.instances:
            drivers_from_csv[driver] = Driver.instances[driver].serialize()

        # Because driver models get stored in instances, clear it out before reading from JSON
        Driver.instances = {}

        futil.read_dict_from_json('testdriver')

        drivers_from_json = {}
        for driver in Driver.instances:
            drivers_from_json[driver] = Driver.instances[driver].serialize()

        # self.maxDiff = None
        self.assertEqual(drivers_from_csv, drivers_from_json, 'Dictionaries should be equal.')
        # Add clear for Drier.instances???
        print('========================= End Driver Utility Test =========================')

    def testTeamUtilities(self) -> None:
        """
        Tests core file utilities functions for team model types.

        Tests the following core application functions:
            * futil.convert_csv_to_json()
            * futil.write_dict_to_json()
            * futil.read_dict_from_json()
            * gutil.importDriversToTeam()
            * conversion from list to Team model
            * conversion from Team model to dictionary

        By default, the following core package functions are tested:
            * _json_file()
            * _csv_file()

        :return: None
        """

        print('\n\n\n========================= Begin Team Utility Test =========================')
        futil.convert_csv_to_json('testteam')

        gutil.importDriversToTeam('testteam', 'testdriver')

        teams_from_csv = {}
        for team in Team.instances:
            teams_from_csv[team] = Team.instances[team].serialize()

        Team.instances = {}

        futil.read_dict_from_json('testteam')

        teams_from_json = {}
        for team in Team.instances:
            teams_from_json[team] = Team.instances[team].serialize()

        # self.maxDiff = None
        self.assertEqual(teams_from_csv, teams_from_json, 'Dictionaries should be equal.')
        print('========================= End Team Utility Test =========================')

    def testDriverDatabaseUtilities(self) -> None:
        """
        Tests core database utilities functions for driver model types.

        TODO: Complete testDriverDatabseUtilities

        :return: None
        :rtype: None
        """

        return


if __name__ == '__main__':
    root_dir = dirname(dirname(abspath(__file__)))

    # Get project root and add it to system PATH if not already there
    if root_dir not in sys.path:
        sys.path = sys.path.append(root_dir)

    unittest.main()

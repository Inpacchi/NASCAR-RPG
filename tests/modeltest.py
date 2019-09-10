import sys
from os.path import dirname, abspath

import unittest

from models.driver import Driver
from models.team import Team
from utilities import futil, gutil


# TODO: Update tests to reflect new futil methods

class ModelTest(unittest.TestCase):
    def testDriverUtilities(self) -> None:
        """
        Tests core file utilities functions for driver model types.

        Tests the following core application functions:
            * convertCSVToJSON()
            * writeDictToJSON()
            * readDictFromJSON()
            * conversion from list to Driver model
            * conversion from Driver model to dictionary

        By default, the following core package functions are tested:
            * __JSONFile()
            * __CSVFile()
            * __headerDiff()

        :return: None
        """

        futil.convertCSVToJSON('testdriver')

        driversDictFromCSV = {}
        for driver in Driver.instances:
            driversDictFromCSV[driver] = Driver.instances[driver].__dict__

        # Because driver models get stored in instances, clear it out before reading from JSON
        Driver.instances = {}

        futil.readDictFromJSON('testdriver')

        driversDictFromJSON = {}
        for driver in Driver.instances:
            driversDictFromJSON[driver] = Driver.instances[driver].__dict__

        self.assertEqual(driversDictFromCSV, driversDictFromJSON, 'Dictionaries should be equal.')
        # Add clear for Drier.instances???

    def testTeamUtilities(self) -> None:
        """
        Tests core file utilities functions for team model types.

        Tests the following core application functions:
            * futil.convertCSVToJSON()
            * futil.writeDictToJSON()
            * futil.readDictFromJSON()
            * gutil.importDriversToTeam()
            * conversion from list to Team model
            * conversion from Team model to dictionary

        By default, the following core package functions are tested:
            * __JSONFile()
            * __CSVFile()
            * __headerDiff()

        :return: None
        """


        futil.convertCSVToJSON('testteam')

        gutil.importDriversToTeam('testteam', 'testdriver')

        teamsDictFromCSV = {}
        for team in Team.instances:
            teamsDictFromCSV[team] = teamsDictFromCSV[team].__dict__

        Team.instances = {}

        futil.readDictFromJSON('testteam')

        teamsDictFromJSON = {}
        for team in Team.instances:
            teamsDictFromJSON[team] = teamsDictFromJSON[team].__dict__

        self.assertEqual(teamsDictFromCSV, teamsDictFromJSON, 'Dictionaries should be equal.')


if __name__ == '__main__':
    rootDir = dirname(dirname(abspath(__file__)))

    # Get project root and add it to system PATH if not already there
    if rootDir not in sys.path:
        sys.path = sys.path.append(rootDir)

    unittest.main()

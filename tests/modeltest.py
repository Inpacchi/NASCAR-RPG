import sys
from os.path import dirname, abspath

import unittest

from utilities import futil, gutil


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

        driversDictCSV = {}
        driversDictJSON = {}

        tempDictCSV = futil.convertCSVToJSON('testdriver')

        for driver in tempDictCSV:
            driversDictCSV[driver] = tempDictCSV[driver].toDict()

        tempDictJSON = futil.readDictFromJSON('testdriver')

        for driver in tempDictJSON:
            driversDictJSON[driver] = tempDictJSON[driver].toDict()

        self.assertEqual(driversDictCSV, driversDictJSON, 'Dictionaries should be equal.')

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

        teamsDictCSV = {}
        teamsDictJSON = {}

        tempDictCSV = futil.convertCSVToJSON('testteam')

        gutil.importDriversToTeam('testteam', 'testdriver', None, tempDictCSV)

        for team in tempDictCSV:
            teamsDictCSV[team] = tempDictCSV[team].toDict()

        tempDictJSON = futil.readDictFromJSON('testteam')

        for team in tempDictJSON:
            teamsDictJSON[team] = tempDictJSON[team].toDict()

        self.assertEqual(teamsDictCSV, teamsDictJSON, 'Dictionaries should be equal.')


if __name__ == '__main__':
    rootDir = dirname(dirname(abspath(__file__)))

    # Get project root and add it to system PATH if not already there
    if rootDir not in sys.path:
        sys.path = sys.path.append(rootDir)

    unittest.main()

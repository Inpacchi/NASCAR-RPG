from typing import Union, TextIO
import os.path
import json
import csv

from sqlalchemy.exc import SQLAlchemyError

from models.driver import Driver
from models.team import Team
from webapp import db

MODEL_TYPE_DICT = {
    'driverSubset': {
        'driver',
        'currentdrivers'
    },
    'teamSubset': {
        'team',
        'charterteam'
    },
    'testSubset': {
        'testdriver',
        'testteam'
    },
    'miscSubset': {
        'standings',
        'tracks'
    },
    'schedules': {
        '2020schedule'
    }
}


def __JSONFile(modelType: str, filepath: str = None, filename: str = None, databaseError: str = None) -> TextIO:
    """
    Returns a JSON file based on given parameters.

    If filepath is specified, direct JSONPath to the the given filepath and filename (filename MUST be specified.)

    If filename is specified, direct JSONPath to the intended directory with the given filename.

    If databaseError is specified as 'y', this method was invoked from a database transaction and should
    direct JSONPath to a temporary file that stores all the uncommitted changes.

    Otherwise, take in a model type and attempt to open the relevant JSON file. If the file is not
    found, then it is is created.

    Once the file has been opened or created, it becomes the return value.

    :param modelType: Type of model being loaded
    :type modelType: string
    :param filepath: If specified, path to file to be used for I/O
    :type filepath: string
    :param filename: If specified, name of file to be used for I/O
    :type filename: string
    :param databaseError: 'Y' value denotes that the function is being invoked for a failed database commit
    :type databaseError: string
    :return: Raw JSON connection string
    :rtype: TextIO
    """

    if databaseError is not None and databaseError.lower() == 'y':
        if filename is not None:
            JSONPath = f'data/sqlite/{filename}.json'
        else:
            raise Exception('You cannot invoke databaseError without a filename!')
    elif filepath is not None and filename is not None:
        JSONPath = f'data/{filepath}/{filename}'
    elif filename is not None:
        if modelType.lower() in MODEL_TYPE_DICT.get('driverSubset'):
            JSONPath = f'data/json/drivers/{filename}.json'
        elif modelType.lower() in MODEL_TYPE_DICT.get('teamSubset'):
            JSONPath = f'data/json/teams/{filename}.json'
        elif modelType.lower() in MODEL_TYPE_DICT.get('testSubset'):
            JSONPath = f'../data/json/tests/{filename}.json'
        else:
            raise Exception('Incorrect model type!')
    else:
        if modelType.lower() == 'driver':
            JSONPath = 'data/json/drivers/drivers.json'
        elif modelType.lower() == 'currentdrivers':
            JSONPath = 'data/json/drivers/currentdrivers.json'
        elif modelType.lower() == 'team':
            JSONPath = 'data/json/teams/teams.json'
        elif modelType.lower() == 'charterteam':
            JSONPath = 'data/json/teams/charterteams.json'
        elif modelType.lower() == 'standings':
            JSONPath = 'data/json/standings.json'
        elif modelType.lower() == 'tracks':
            JSONPath = 'data/json/tracks.json'
        elif modelType.lower() == '2020schedule':
            JSONPath = 'data/json/seasons/2020/schedule.json'
        elif modelType.lower() == 'testdriver':
            JSONPath = 'data/tests/json/drivers/drivers.json'
        elif modelType.lower() == 'testteam':
            JSONPath = 'data/tests/json/teams/teams.json'
        else:
            raise Exception('Incorrect model type!')

    try:
        JSONFile = open(JSONPath, 'r+', encoding='utf-8-sig')
    except IOError:
        JSONFile = open(JSONPath, 'w+', encoding='utf-8-sig')

    return JSONFile


def __CSVFile(modelType: str, filename: str = None, conversion: str = None) -> TextIO:
    """
    Returns a CSV file based on given parameters.

    If conversion is specified as 'y', the intended usage is to store data as a CSV for database operations.
    CSVPath is directed towards a conversion directory such as to separate these files from regular data.

    If filename is specified, direct CSVPath to the intended directory with the given filename.

    Otherwise, take in a model type and attempt to open the relevant CSV file. If the file is not
    found, then it is created.

    Once the file has been opened or created, it becomes the return value.

    :param modelType: Type of model being loaded
    :type modelType: string
    :param filename: If specified, name of file to be used for I/O
    :type filename: string
    :param conversion: If specified, use conversion output path
    :type conversion: string
    :return: Raw CSV connection string
    :rtype: TextIO
    """

    if conversion is not None and conversion.lower() == 'y':
        CSVPath = f'data/sqlite/conversion/{filename}.csv'
    elif filename is not None:
        if modelType.lower() in MODEL_TYPE_DICT.get('driverSubset'):
            CSVPath = f'data/csv/drivers/{filename}.csv'
        elif modelType.lower() in MODEL_TYPE_DICT.get('teamSubset'):
            CSVPath = f'data/csv/teams/{filename}.csv'
        elif modelType.lower() in MODEL_TYPE_DICT.get('testSubset'):
            CSVPath = f'../data/csv/tests/{filename}.csv'
        else:
            raise Exception('You entered a filename, but did not enter a valid model type!')
    else:
        if modelType.lower() == 'driver':
            CSVPath = 'data/csv/drivers/drivers.csv'
        elif modelType.lower() == 'team':
            CSVPath = 'data/csv/teams/teams.csv'
        elif modelType.lower() == 'testdriver':
            CSVPath = 'data/tests/csv/drivers/drivers.csv'
        elif modelType.lower() == 'testteam':
            CSVPath = 'data/tests/csv/teams/teams.csv'
        else:
            raise Exception('Incorrect model type!')

    try:
        CSVFile = open(CSVPath, 'r+', encoding='utf-8-sig')
    except IOError:
        CSVFile = open(CSVPath, 'w+', encoding='utf-8-sig')

    return CSVFile


def __getCSVHeader(modelType: str) -> list:
    """
    Returns the relevant modelType CSV Header.

    :param modelType: Type of model being loaded
    :type modelType: string
    :return: list of column names
    :rtype: list
    """

    if modelType.lower() in (MODEL_TYPE_DICT.get('driverSubset').union('testdriver')):
        header = ['name', 'age', 'teamName', 'contractStatus', 'carNumber', 'shortRating', 'shortIntermediateRating',
                  'intermediateRating', 'superSpeedwayRating', 'restrictedTrackRating', 'roadCourseRating',
                  'overallRating', 'potential']
    elif modelType.lower() in (MODEL_TYPE_DICT.get('teamSubset').union('testteam')):
        header = ['name', 'owner', 'carManufacturer', 'equipmentRating', 'teamRating', 'raceRating', 'drivers']
    elif modelType.lower() == 'standings':
        header = ["qualifyingPosition", "finishingPosition", "lapsLed", "timesQualifyingRangeHit", "timesRaceRangeHit",
                  "fastestQualifyingLap"]
    elif modelType.lower() == 'tracks':
        header = ['name', 'length', 'type']
    elif modelType.lower() in MODEL_TYPE_DICT.get('schedules'):
        header = ['name', 'date', 'type', 'track', 'laps', 'stages', 'raceProcessed']
    else:
        raise Exception('Incorrect model type!')

    return header


def readDictFromJSON(modelType: str, filename: str = None, filepath: str = None) -> Union[None, dict]:
    """
    Reads a dictionary and either populates Model.Instances (if present) or returns the dictionary.

    If filepath is specified, open the JSON at the given filepath and filename (filename MUST be specified.)

    :param modelType: Type of model being loaded
    :type modelType: string
    :param filepath: If specified, path to JSON to be read from
    :type filepath: string
    :param filename: If specified, name of JSON to be read from
    :type filename: string
    :return: Dictionary if type is not a model
    :rtype: dictionary
    :return: None if type is a model
    :rtype: None
    """

    JSONFile = __JSONFile(modelType, filepath, filename, None)
    tempDict = json.load(JSONFile)
    JSONFile.close()

    if modelType.lower() in MODEL_TYPE_DICT.get('driverSubset').union('testdriver'):
        for model in tempDict:
            Driver(tempDict[model])
        return
    elif modelType.lower() in MODEL_TYPE_DICT.get('teamSubset').union(MODEL_TYPE_DICT.get('testSubset')):
        for model in tempDict:
            Team(tempDict[model])
        return
    elif modelType.lower() in (MODEL_TYPE_DICT.get('miscSubset').union(MODEL_TYPE_DICT.get('schedules'))):
        return tempDict


def writeDictToJSON(modelType: str, dataDict: dict, filename: str = None, databaseError: str = None) -> None:
    """
    Writes the model dictionary to the relevant model type JSON file.

    If databaseError is specified, direct output to a temporary file that stores all uncommitted
    changes (filename MUST be specified)

    Otherwise, take in a model type and model dictionary and attempt to write the models or
    dictionary to a JSON file.

    :param modelType: Type of model being written to
    :type modelType: string
    :param dataDict: Dictionary of data or models to be written to the JSON file
    :type dataDict: dict
    :param filename: If specified, name of file to be written to
    :type filename: string
    :param databaseError: 'Y' value denotes that the function is being invoked for a failed database commit
    :type databaseError: string
    :return: None
    :rtype: None
    """

    JSONFile = __JSONFile(modelType, None, filename, databaseError)

    # Clear the file
    JSONFile.seek(0)
    JSONFile.truncate(0)

    if modelType.lower() in MODEL_TYPE_DICT.get('driverSubset').union(MODEL_TYPE_DICT.get('teamSubset')).union(
            MODEL_TYPE_DICT.get('testSubset')):
        tempDict = {}

        for name in dataDict:
            tempDict[name] = dataDict[name].serialize()

        json.dump(tempDict, JSONFile, indent=4)
    elif modelType.lower() in MODEL_TYPE_DICT.get('miscSubset').union(MODEL_TYPE_DICT.get('schedules')):
        json.dump(dataDict, JSONFile, indent=4)

    JSONFile.close()
    print(f'\nJSON file for model type "{modelType}" created at {JSONFile.name}')


def convertCSVToJSON(modelType: str, filename: str = None) -> None:
    """
    Import lines from a CSV file as models and convert to dictionary format.

    :param modelType: Type of model being loaded
    :type modelType: string
    :param filename: If specified, the specific path to write the CSV file to
    :type filename: string
    :return: None
    :rtype: None
    """

    CSVFile = __CSVFile(modelType, filename)
    reader = csv.DictReader(CSVFile)
    next(reader)  # Skip the header lines

    if modelType in MODEL_TYPE_DICT.get('driverSubset'):
        for row in reader:
            Driver(row)
        writeDictToJSON(modelType, Driver.instances, filename)
    elif modelType in MODEL_TYPE_DICT.get('teamSubset'):
        for row in reader:
            Team(row)
        writeDictToJSON(modelType, Team.instances, filename)

    CSVFile.close()
    print(f'CSV file for model type "{modelType}" converted from {CSVFile.name}')


def convertDictToCSV(modelType: str, dataDict: dict = None, filename: str = None, conversion: str = None) -> None:
    """
    Convert regular dictionaries and model dictionaries to a CSV format.

    :param modelType: Type of model being written to
    :type modelType: string
    :param dataDict: If specified, a dictionary of values
    :type dataDict: dict
    :param filename: If specified, the specific path to write the CSV file to
    :type filename: string
    :param conversion: If specified, use conversion output path
    :type conversion: string
    :return: None
    :rtype: None
    """

    if dataDict is None and modelType.lower() in MODEL_TYPE_DICT.get('miscSubset').union(
            MODEL_TYPE_DICT.get('schedules')):
        dataDict = readDictFromJSON(modelType)
    elif not Driver.instances and dataDict is None:
        readDictFromJSON(modelType)

    CSVFile = __CSVFile(modelType, filename, conversion)

    writer = csv.DictWriter(CSVFile, fieldnames=__getCSVHeader(modelType))
    writer.writeheader()

    if modelType in MODEL_TYPE_DICT.get('driverSubset'):
        for driver in Driver.instances.values():
            writer.writerow(driver.serialize())
    elif modelType in MODEL_TYPE_DICT.get('teamSubset'):
        for team in Team.instances.values():
            writer.writerow(team.serialize())
    else:
        writer.writerows(dataDict.values())

    CSVFile.close()
    print(f'\nCSV file created at {CSVFile.name}')


def addCSVToDatabase(modelType: str, filename: str = None) -> None:
    """
    Add rows from a CSV to the database.

    If the commit should fail, the intended changes are written to a file so a commit can be tried again.

    TODO: Add if parameters for other data types.

    :param modelType: Type of model being loaded
    :type modelType: string
    :param filename: If specified, name of file to be used for I/O
    :type filename: string
    :return: None
    :rtype: None
    """

    # TODO: Add the ability to store multiple noncommittals and interactively chose between them.
    if os.path.exists('data/sqlite/uncommitted-db-session.json'):
        __retryCommit()
        return

    CSVFile = __CSVFile(modelType, filename)
    reader = csv.DictReader(CSVFile)
    next(reader)

    if modelType in MODEL_TYPE_DICT.get('driverSubset'):
        for row in reader:
            tempDriver = Driver(row)
            db.session.add(tempDriver)

        try:
            db.session.commit()
        except SQLAlchemyError:
            writeDictToJSON('driver', Driver.instances, 'uncommitted-db-session', 'y')
            db.session.rollback()
            raise SQLAlchemyError('Database commit failed! Uncommitted changes have been saved to '
                                  'data/sqlite/uncommitted-db-session.json')
    elif modelType in MODEL_TYPE_DICT.get('teamSubset'):
        for row in reader:
            tempTeam = Team(row)
            db.session.add(tempTeam)

        try:
            db.session.commit()
        except SQLAlchemyError:
            writeDictToJSON('driver', Team.instances, 'uncommitted-db-session', 'y')
            db.session.rollback()
            raise SQLAlchemyError('Database commit failed! Uncommitted changes have been saved to '
                                  'data/sqlite/uncommitted-db-session.json')


def __retryCommit(modelType: str) -> None:
    """
    Retries commit for uncommitted changes if file is found. If commit fails again, alert user to a fatal error.

    :param modelType: Type of model being loaded
    :type modelType: string
    :return: None
    :rtype: None
    """

    if modelType in MODEL_TYPE_DICT.get('driverSubset'):
        if Driver.instances != {}:
            Driver.instances = {}

        readDictFromJSON(modelType, 'data/sqlite', 'uncommitted-db-session')

        for driver in Driver.instances:
            db.session.add(Driver.instances[driver])
    elif modelType in MODEL_TYPE_DICT.get('teamSubset'):
        if Team.instances != {}:
            Team.instances = {}

        readDictFromJSON(modelType, 'data/sqlite', 'uncommitted-db-session')

        for team in Team.instances:
            db.session.add(Team.instances[team])

    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise SQLAlchemyError('Commit failed on retry! Fatal error occurred, please contact your system administrator.')

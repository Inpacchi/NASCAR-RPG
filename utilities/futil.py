from typing import Union, TextIO
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


# TODO: Add interactive file input functionality


def __JSONFile(modelType: str, filename: str = None, databaseError: str = None) -> TextIO:
    """
    Returns a JSON file based on model type.

    Pseudo-private method that takes in a model type and attempts to open the relevant JSON file. If the file is not
    found, then it is is created. Once the file has been opened or created, it becomes the return value.

    :param modelType: Type of model being loaded
    :type modelType: string
    :param filename: If specified, name of file to be used for I/O
    :type filename: string
    :param databaseError: 'Y' value denotes that the function is being invoked for a failed database commit
    :type databaseError: string
    :return: Raw JSON connection string
    :rtype: TextIO
    """

    if databaseError is not None and databaseError.lower() == 'y':
        JSONPath = f'data/sqlite/{filename}.json'
    elif filename is not None:
        if modelType.lower() in MODEL_TYPE_DICT.get('driverSubset'):
            JSONPath = f'data/json/drivers/{filename}.json'
        elif modelType.lower() in MODEL_TYPE_DICT.get('teamSubset'):
            JSONPath = f'data/json/teams/{filename}.json'
        elif modelType.lower() in MODEL_TYPE_DICT.get('testSubset'):
            JSONPath = f'../data/json/tests/{filename}.json'
        else:
            raise Exception('You entered a filename, but did not enter a valid model type!')
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
            JSONPath = '../data/tests/json/drivers.json'
        elif modelType.lower() == 'testteam':
            JSONPath = '../data/tests/json/teams.json'
        else:
            raise Exception('Incorrect model type!')

    try:
        JSONFile = open(JSONPath, 'r+', encoding='utf-8-sig')
    except IOError:
        JSONFile = open(JSONPath, 'w+', encoding='utf-8-sig')

    return JSONFile


def __CSVFile(modelType: str, filename: str = None, conversion: str = None) -> Union[str, TextIO]:
    """
    Returns a CSV file based on model type.

    Pseudo-private method that takes in a model type and attempts to open the relevant CSV file. If the file is not
    found, then it is created. Once the file has been opened or created, it becomes the return value.

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
            CSVPath = '../data/tests/csv/drivers/drivers.csv'
        elif modelType.lower() == 'testteam':
            CSVPath = '../data/tests/csv/teams/teams.csv'
        else:
            raise Exception('Incorrect model type!')

    try:
        CSVFile = open(CSVPath, 'r+', encoding='utf-8-sig')
    except IOError:
        CSVFile = open(CSVPath, 'w+', encoding='utf-8-sig')

    return CSVFile


def __getCSVHeader(modelType: str):
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


def readDictFromJSON(modelType: str, filepath: str = None) -> Union[None, dict]:
    """
    Returns a dictionary loaded directly from a JSON file.

    Package available method that returns a Python dictionary as defined in the relevant JSON file. The function will
    return either the dictionary converted into models or a directly loaded JSON dictionary.

    :param modelType: Type of model being loaded
    :type modelType: string
    :param filepath: If specified, override the default path generated from modelType with this parameter
    :type filepath: string
    :return: Dictionary if type is not a model
    :rtype: dictionary
    :return: None if type is a model
    :rtype: None
    """

    JSONFile = __JSONFile(modelType)
    tempDict = json.load(JSONFile)
    JSONFile.close()

    if modelType.lower() in MODEL_TYPE_DICT.get('driverSubset'):
        for model in tempDict:
            Driver(tempDict[model])
        return
    elif modelType.lower() in MODEL_TYPE_DICT.get('teamSubset'):
        for model in tempDict:
            Team(tempDict[model])
        return
    elif modelType.lower() in (MODEL_TYPE_DICT.get('miscSubset').union(MODEL_TYPE_DICT.get('schedules'))):
        return tempDict

    print(f'JSON file read from {JSONFile.name}')


def writeDictToJSON(modelType: str, dataDict: dict, filename: str = None, databaseError: str = None) -> None:
    """
    Writes the model dictionary to the relevant model type JSON file.

    Package available method that takes in a model type and model dictionary and attempts to write the models to a JSON
    file.

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

    if databaseError.lower() == 'y':
        JSONFile = __JSONFile(modelType, filename, '')
    else:
        JSONFile = __JSONFile(modelType, filename)

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
    print(f'\nJSON file created at {JSONFile.name}')


def convertCSVToJSON(modelType: str, filename: str = None) -> None:
    """
    Imports lines from a CSV file as models and converts to JSON format

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
    print(f'CSV file converted from {CSVFile.name}')


def convertDictToCSV(modelType: str, dataDict: dict = None, filename: str = None, conversion: str = None) -> None:
    """
    Converts regular dictionaries and model dictionaries to a CSV format.

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


def addCSVToDatabase(modelType: str, filename: str = None):
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

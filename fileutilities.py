from typing import Union, List, TextIO
from progressbar import ProgressBar, Bar, Percentage

from models.driver import Driver
from models.team import Team

import json
import csv
import os

# TODO: Add interactive file input functionality


def __JSONFile(modelType: str) -> TextIO:
    """
    Returns a JSON file based on model type.

    Pseudo-private method that takes in a model type and attempts to open the relevant JSON file. If the file is not
    found, then it is is created. Once the file has been opened or created, it becomes the return value.

    :param modelType: Type of model being loaded
    :type modelType: string
    :return: Raw JSON connection string
    :rtype: TextIO
    """

    if modelType.lower() == 'driver':
        JSONPath = 'data/json/drivers.json'
    elif modelType.lower() == 'team':
        JSONPath = 'data/json/teams.json'
    elif modelType.lower() == 'currentdrivers':
        JSONPath = 'data/json/currentdrivers.json'
    elif modelType.lower() == 'standings':
        JSONPath = 'data/json/standings.json'
    else:
        raise Exception('Incorrect model type!')

    try:
        JSONFile = open(JSONPath, 'r+')

        if os.stat(JSONPath).st_size == 0:
            os.remove(JSONPath)
            raise IOError

        print(modelType, "json found; reading from database...")
    except IOError:
        JSONFile = open(JSONPath, 'w+')

        print(modelType, "json not found; database has been created")

    return JSONFile


def __readModelListFromJSONFile(modelType: str, JSONFile: list) -> Union[None, List[Driver], List[Team]]:
    """
    DEPRECATED: Returns a list of models from model list based on model type.

    Pseudo-private method that takes in a model type, reads each model from the model list and returns them in a list
    of relevant model objects. If the model list is empty, that means the list and subsequent file was just created;
    hence there is no data to read and the function returns nothing.

    :param modelType: Type of model being loaded
    :type modelType: string
    :param JSONFile: JSON file with models
    :type JSONFile: list
    :return: Models initialized as their relevant objects
    :rtype: list
    """

    # There is no need for a validation message here as it is okay to not have data in the model list.
    if not JSONFile:
        return

    bar = createProgressBar().start()
    i = 0

    if modelType.lower() in ['driver', 'currentdrivers']:
        driverList = []

        for tempDriver in JSONFile:
            print(tempDriver)
            driverList.append(Driver(tempDriver))
            bar.update(i + 1)

        bar.finish()
        print()

        return driverList
    elif modelType.lower() == 'team':
        teamList = []

        for tempTeam in JSONFile:
            teamList.append(Team(tempTeam))
            bar.update(i + 1)

        bar.finish()
        print()

        return teamList
    else:
        raise Exception("Incorrect model type!")


def __CSVFile(modelType: str) -> Union[str, TextIO]:
    """
    Returns a CSV file based on model type.

    Pseudo-private method that takes in a model type and attempts to open the relevant CSV file. If the file is not
    found, then it is created. Once the file has been opened or created, it becomes the return value.

    :param modelType: Type of model being loaded
    :type modelType: string
    :return: Raw CSV connection string
    :rtype: TextIO
    """

    if modelType.lower() == 'driver':
        CSVPath = 'data/csv/drivers.csv'
    elif modelType.lower() == 'team':
        CSVPath = 'data/csv/teams.csv'
    else:
        raise Exception('Incorrect model type!')

    try:
        # Must define encoding='utf-8-sig' to function seamlessly with Excel sheets and exports.
        CSVFile = open(CSVPath, 'r', encoding='utf-8-sig')

        if os.stat(CSVPath).st_size == 0:
            os.remove(CSVPath)
            raise IOError
    except IOError:
        raise

    return CSVFile


def readModelListFromJSON(modelType: str) -> Union[None, List[Driver], List[Team]]:
    """
    DEPRECATED: Returns a list of models.

    Package available method that simplifies the function call.

    :param modelType: Type of model being loaded
    :type modelType: string
    :return: Models initialized as their relevant objects
    :rtype: list
    """

    return __readModelListFromJSONFile(modelType, json.load(__JSONFile(modelType)))


def writeModelListToJSON(modelType: str, modelList: list) -> None:
    """
    DEPRECATED: Writes the model list to the relevant model type JSON file.

    Package available method that takes in a model type and model list and attempts to write the models to a JSON file.
    Due to the nature of the JSON format, JSON files must first be read into memory and stored so that they can be
    properly modified. Once the JSON file is read and the models are properly initialized, the model list is
    serialized to JSON using the relevant class available toJSON() method and appended to the list. After the file is
    erased of all contents, this list is written to the file in JSON format.

    :param modelType: Type of model being loaded
    :type modelType: string
    :param modelList: Models loaded from JSON file
    :type modelList: list
    :return: None
    :rtype: None
    """

    if modelType.lower() not in ['driver', 'currentdrivers', 'team']:
        raise Exception("Incorrect model type!")

    JSONFile = __JSONFile(modelType)

    bar = createProgressBar().start()

    # If the first line is empty, assume the file is empty (it is not in the right format)
    if JSONFile.readline() != '':
        tempModelList = __readModelListFromJSONFile(modelType, json.load(JSONFile))

        i = 0

        print("Appending models...")

        for tempModel in tempModelList:
            modelList.append(tempModel)
            bar.update(i + 1)

        bar.finish()
        print()

    modelListJSON = []

    bar.start()
    i = 0

    for model in modelList:
        modelListJSON.append(json.loads(model.toJSON()))
        bar.update(i + 1)

    bar.finish()
    print()

    # Reset JSON current position to 0 (start of file)
    JSONFile.seek(0)

    # Clear the contents of the JSON
    JSONFile.truncate(0)

    # Write the JSON list to the JSON file with pretty print enabled
    json.dump(modelListJSON, JSONFile, indent=4)

    JSONFile.close()

    print("\n", modelType, "json has been updated")


def readDictFromJSON(modelType: str) -> dict:
    """
    Returns a dictionary loaded directly from a JSON file.

    Package available method that returns a Python dictionary as defined in the relevant JSON file. The function will
    return either the dictionary converted into models or a directly loaded JSON dictionary.

    :param modelType: Type of model being loaded
    :type modelType: string
    :return: Dictionary of models
    :rtype: dictionary
    """

    tempDict = json.load(__JSONFile(modelType))

    modelDict = {}

    if modelType.lower() in ['driver', 'currentdrivers']:
        for model in tempDict:
            modelDict[model] = Driver(tempDict[model])
    elif modelType.lower() == 'team':
        for model in tempDict:
            modelDict[model] = Team(tempDict[model])
    elif modelType.lower() == 'standings':
        modelDict.update(tempDict)

    return modelDict


def writeDictToJSON(modelType: str, modelDict: dict) -> None:
    """
    Writes the model dictionary to the relevant model type JSON file.

    Package available method that takes in a model type and model dictionary and attempts to write the models to a JSON
    file.

    :param modelType: Type of model being written to
    :type modelType: string
    :param modelDict: Dictionary of models to be written to the JSON file
    :type modelDict: dict
    :return: None
    :rtype: None
    """
    JSONFile = __JSONFile(modelType)

    # Clear the file
    JSONFile.seek(0)
    JSONFile.truncate(0)

    if modelType.lower() in ['driver', 'team', 'currentdrivers']:
        tempDict = {}

        for x in modelDict:
            tempDict[x] = modelDict[x].toDict()

        json.dump(tempDict, JSONFile, indent=4)
    elif modelType.lower() == 'standings':
        json.dump(modelDict, JSONFile, indent=4)

    JSONFile.close()


def convertCSVToJSON(modelType: str) -> None:
    """
    Converts the relevant CSV file to JSON format.

    Package available method that converts a CSV file into a JSON file.

    :param modelType: Type of model being loaded
    :type modelType: string
    :return: None
    :rtype: None
    """

    if modelType.lower() == 'driver':
        properHeader = ['Name', 'Age', 'Team Name', 'Contract Status', 'Car Number', 'Short Rating',
                        'Short Intermediate Rating',
                        'Intermediate Rating', 'Superspeedway Rating', 'Restrictor Plate Rating', 'Road Rating',
                        'Overall Rating', 'Potential Retain']
    elif modelType.lower() == 'team':
        properHeader = ['Name', 'Owner', 'Car Manufacturer', 'Equipment Rating', 'Team Rating', 'Race Rating']
    else:
        raise Exception('Incorrect model type!')

    csvHeader = []

    reader = csv.reader(__CSVFile(modelType))

    header = next(reader)

    for column in header:
        csvHeader.append(column)

    # TODO: Refine error checking and display messages when the headers don't match up.
    headerDiffList = headerDiff(properHeader, csvHeader)

    # Get the differences of the two lists; if they are not ordered correctly or have different column names,
    # don't do anything.
    if headerDiffList:
        print("Seems like the header is messed up. Check the CSV and try again.\n")
        # itemCount = 0
        # for item in headerDiffList:
        # if itemCount == 0 or itemCount % 2 == 0:
        # print("Expected:", headerDiffList[itemCount])
        # print("Got:", headerDiffList[itemCount + 1])
        # itemCount += 1
    else:
        print("The header in both files match! Importing models now...")

        modelList = []

        bar = createProgressBar()
        bar.start()
        i = 0

        if modelType.lower() == 'driver':
            for row in reader:
                modelList.append(Driver(row))
                bar.update(i + 1)
        elif modelType.lower() == 'team':
            for row in reader:
                modelList.append(Team(row))
                bar.update(i + 1)

        bar.finish()
        print()

        writeModelListToJSON(modelType, modelList)

        # TODO: Move file to archive and rename it according to what's already in the folder
        # os.rename('data/csv/drivers.csv', 'data/csv/archive/drivers.csv')


def headerDiff(properHeader: list, csvHeader: list) -> list:
    """
    Returns a list of differences between the two lists.

    :param properHeader: Values that the header file should be
    :type properHeader: list
    :param csvHeader: Header taken from the CSV file
    :type csvHeader: list
    :return: Differences between the two lists
    :rtype: list
    """
    return [i for i in properHeader + csvHeader if i not in properHeader or i not in csvHeader]


def createProgressBar() -> ProgressBar:
    """
    Simple function call to create a progress bar with the relevant parameters.

    Parameters are taken from the progressbar import statement.

    :return: Progress Bar with parameters
    :rtype: ProgressBar
    """

    return ProgressBar(max_value=20, widgets=[Bar('=', '[', ']'), ' ', Percentage()])

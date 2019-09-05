from random import randint
import potential
import fileutilities as futil

# Pseudo-Private Global Constants
__DRIVER_FACTOR = 1.25
__TEAM_FACTOR = 1.4

# Pseudo-Private Mutable Parameters
__rateRangesDict = {}
__standingsDict = {}
__endingRange = 0


def processStage(driversDict: dict) -> None:
    """
    Main entry method for race.py

    Package available method that handles all function calls and logic processing for the race package.

    :param driversDict: Dictionary of drivers to be processed through the race stages
    :type driversDict: dict
    :return: None
    :rtype: None
    """

    __populateRangesDict(driversDict)
    __populateStandingsDict(driversDict)
    __qualifying()
    __race()
    futil.writeDictToJSON('standings', __standingsDict)
    __processDriverPotential(driversDict)


def __populateRangesDict(driversDict: dict) -> None:
    """
    Populates the rateRangesDict with rate ranges to be used for race stage processing.

    :param driversDict: Dictionary of drivers to be processed through the race stages
    :type driversDict: dictionary
    :return: None
    :rtype: None
    """
    startingRange = 0

    for driver in driversDict:
        dictToAdd = {
            driver: {
                "startingRange": startingRange,
                "endingRange": 0
            }
        }

        # TODO: Finish team implementation
        # TODO: Check if driver is the only driver in teams driver list.

        startingRange += __calculateRange(driversDict[driver], 50)
        dictToAdd[driver]['endingRange'] = startingRange
        __rateRangesDict.update(dictToAdd)
        startingRange += 1

        # for team in teamsList:
        #     if driver.name in team.drivers:
        #         startingRange += calculateRange(driver, team)
        #         dictToAdd[driver.name]['endingRange'] = startingRange
        #         rateRangesDict.update(dictToAdd)
        #         startingRange += 1
        #         break

    global __endingRange
    __endingRange = startingRange


def __populateStandingsDict(driversDict: dict) -> None:
    """
    Populates the standingsDict with the standings generated during race stage processing.

    :param driversDict: Dictionary of drivers to be processed through the race stages
    :type driversDict: dictionary
    :return: None
    :rtype: None
    """

    for driver in driversDict:
        dictToAdd = {
            driver: {
                "qualifyingPosition": 0,
                "finishingPosition": 0,
                "lapsLed": 0,
                "timesQualifyingRangeHit": 0,
                "timesRaceRangeHit": 0
            }
        }

        __standingsDict.update(dictToAdd)


def __calculateRange(driver, team_overall, startingBonus=0):
    """
    TODO: Implement team functionality

    TODO: Complete docstring

    :param driver:
    :param team_overall:
    :param startingBonus:
    :return:
    """

    driverResult = pow(float(driver.overallRating), __DRIVER_FACTOR)
    teamResult = pow(team_overall, __TEAM_FACTOR)
    bonusResult = startingBonus * 50

    return round(((driverResult * teamResult) + bonusResult) / 100)

# def calculateRange(driver, team, startingBonus=0):
#     driverResult = pow(driver.overallRating, DRIVER_FACTOR)
#     teamResult = pow(team.overall, TEAM_FACTOR)
#     bonusResult = startingBonus * 50
#
#     return round(((driverResult * teamResult) + bonusResult) / 100)


def __qualifying() -> None:
    """
    Processes the qualifying stage of the race and writes the results to the standingsDict.

    :return: None
    :rtype: None
    """

    qualifyingPosition = 1

    while qualifyingPosition != len(__standingsDict) + 1:
        randomNumber = randint(0, __endingRange)

        for rateRange in __rateRangesDict:
            if __rateRangesDict[rateRange]['startingRange'] <= randomNumber <= __rateRangesDict[rateRange]['endingRange']:
                if __standingsDict[rateRange]['qualifyingPosition'] == 0:
                    __standingsDict[rateRange]['qualifyingPosition'] = qualifyingPosition
                    __standingsDict[rateRange]['timesQualifyingRangeHit'] += 1
                    qualifyingPosition += 1
                else:
                    __standingsDict[rateRange]['timesQualifyingRangeHit'] += 1


def __race() -> None:
    """
    Processes the actual race portion and writes the results to the standingsDict.

    :return: None
    :rtype: None
    """

    finishingPosition = 1

    while finishingPosition != len(__standingsDict) + 1:
        randomNumber = randint(0, __endingRange)

        for rateRange in __rateRangesDict:
            if __rateRangesDict[rateRange]['startingRange'] <= randomNumber <= __rateRangesDict[rateRange]['endingRange']:
                if __standingsDict[rateRange]['finishingPosition'] == 0:
                    __standingsDict[rateRange]['finishingPosition'] = finishingPosition
                    __standingsDict[rateRange]['timesRaceRangeHit'] += 1
                    finishingPosition += 1
                else:
                    __standingsDict[rateRange]['timesRaceRangeHit'] += 1


def __processDriverPotential(driversDict: dict) -> None:
    """
    Processes driver potential after the race stages has run.

    :param driversDict: Dictionary of drivers to be processed through the race stages
    :type driversDict: dictionary
    :return: None
    :rtype: None
    """

    global __standingsDict

    if not __standingsDict:
        __standingsDict = futil.readDictFromJSON('standings')

    potential.processStage(__standingsDict, driversDict)

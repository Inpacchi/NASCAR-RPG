from random import randint

from game import potential
from models.driver import Driver
from models.team import Team
from utilities import futil

# Pseudo-Private Global Constants
__DRIVER_FACTOR = 1.25
__TEAM_FACTOR = 1.4

# Pseudo-Private Mutable Parameters
__rateRangesDict = {}
__standingsDict = {}
__endingRange = 0


def processStage() -> None:
    """
    Main entry method for raceweekend.py

    Package available method that handles all function calls and logic processing for the race package.

    :return: None
    :rtype: None
    """

   #  scheduleDict = futil.readDictFromJSON('2020schedule')

    # for raceObject in scheduleDict:
    #     race = scheduleDict[raceObject]
    #     if race['raceProcessed'] == 'no':
    #         unprocessedRaces[raceIndex] = (race['name'])
    #         raceIndex += 1
            # if len(race['name']) > longestWordLength:
            #     longestWordLength = len(race['name']) + 10

    # futil.readDictFromJSON('currentdrivers')
    # futil.readDictFromJSON('teams')
    #
    # tracksDict = futil.readDictFromJSON('tracks')
    #
    # __populateRangesDict()
    # __populateStandingsDict()
    # __qualifying()
    # __race()
    # futil.writeDictToJSON('standings', __standingsDict)
    # __processDriverPotential()


def __populateRangesDict() -> None:
    """
    Populates the rateRangesDict with rate ranges to be used for race stage processing.

    :return: None
    :rtype: None
    """

    placementRange = 0
    for name in Driver.instances:
        driver = Driver.instances[name]

        dictToAdd = {
            driver.name: {
                "startingRange": placementRange,
                "endingRange": 0
            }
        }

        if driver.teamName != '':
            placementRange += __calculateRange(driver, Team.instances.get(driver.teamName))
            dictToAdd[driver.name]['endingRange'] = placementRange
            __rateRangesDict.update(dictToAdd)
            placementRange += 1
            break

    global __endingRange
    __endingRange = placementRange


def __calculateRange(driver: Driver, team: Team, startingBonus: int = 0) -> float:
    """
    Returns a range for each driver dependent upon their overall rating as well as their team rating and any bonuses.

    :param driver: Driver model object
    :type driver: Driver
    :param team: Team model object
    :type team: Team
    :param startingBonus: Any bonus to be added to the formula
    :type startingBonus: integer
    :return: Range to determine standings
    :rtype: float
    """

    trackRating = 0

    driverResult = pow(float(driver.overallRating), __DRIVER_FACTOR)
    teamResult = pow(team.raceRating, __TEAM_FACTOR)
    bonusResult = startingBonus * 50

    return round(((driverResult * teamResult) + bonusResult) / 100)


def __populateStandingsDict() -> None:
    """
    Populates the standingsDict with the standard standings that will be generated during race stage processing.

    :return: None
    :rtype: None
    """

    for driver in Driver.instances:
        dictToAdd = {
            driver: {
                "qualifyingPosition": 0,
                "finishingPosition": 0,
                "lapsLed": 0,
                "timesQualifyingRangeHit": 0,
                "timesRaceRangeHit": 0,
                "fastestQualifyingLap": 0
            }
        }

        __standingsDict.update(dictToAdd)


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
            if __rateRangesDict[rateRange]['startingRange'] <= randomNumber <= __rateRangesDict[rateRange][
                'endingRange']:
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
            if __rateRangesDict[rateRange]['startingRange'] <= randomNumber <= __rateRangesDict[rateRange][
                'endingRange']:
                if __standingsDict[rateRange]['finishingPosition'] == 0:
                    __standingsDict[rateRange]['finishingPosition'] = finishingPosition
                    __standingsDict[rateRange]['timesRaceRangeHit'] += 1
                    finishingPosition += 1
                else:
                    __standingsDict[rateRange]['timesRaceRangeHit'] += 1


def __processDriverPotential() -> None:
    """
    Processes driver potential after the race stages has run.

    :return: None
    :rtype: None
    """

    global __standingsDict

    if not __standingsDict:
        __standingsDict = futil.readDictFromJSON('standings')

    potential.processStage(__standingsDict, Driver.instances)

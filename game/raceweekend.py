from random import randint

from game import potential
from models.gameapp import Schedule, Track
from models.driver import Driver
from models.team import Team
from utilities import dbutil
from webapp import db

# Pseudo-Private Global Constants
__DRIVER_FACTOR = 1.25
__TEAM_FACTOR = 1.4

# Pseudo-Private Mutable Parameters
__rateRangesDict = {}
__standingsDict = {}
__endingRange = 0


def processStage(raceName: str = None, trackName: str = None) -> None:
    """
    Main entry method for raceweekend.py

    Package available method that handles all function calls and logic processing for the race package.

    :return: None
    :rtype: None
    """

    if raceName is not None:
        race = db.session.query(Schedule.trackId).filter(Schedule.name.like(f'%{raceName}%')).subquery()
        track = Track.query.filter(Track.id.in_(race)).first()
    elif trackName is not None:
        track = Track.query.filter(Track.name.like(f'%{trackName}%')).first()
    else:
        raise Exception('Either raceName or trackName must be specified!')

    drivers = Driver.query.all()

    __populateRangesDict(drivers, track)
    __populateStandingsDict(drivers)
    __qualifying()
    __race()
    dbutil.populateStandings(__standingsDict)
    # potential.processStage(__standingsDict, drivers)


def __populateRangesDict(drivers, track) -> None:
    """
    Populates the rateRangesDict with rate ranges to be used for race stage processing.

    :return: None
    :rtype: None
    """

    placementRange = 0
    for driver in drivers:
        dictToAdd = {
            driver.name: {
                "startingRange": placementRange,
                "endingRange": 0
            }
        }

        placementRange += __calculateRange(track, driver)
        dictToAdd[driver.name]['endingRange'] = placementRange
        __rateRangesDict.update(dictToAdd)
        placementRange += 1

    global __endingRange
    __endingRange = placementRange


def __calculateRange(track, driver: Driver, team: Team = None, startingBonus: int = 0) -> float:
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

    if track.type == 'short':
        driverResult = pow(float(driver.shortRating), __DRIVER_FACTOR)
    elif track.type == 'short-intermediate':
        driverResult = pow(float(driver.shortIntermediateRating), __DRIVER_FACTOR)
    elif track.type == 'intermediate':
        driverResult = pow(float(driver.intermediateRating), __DRIVER_FACTOR)
    elif track.type == 'superspeedway':
        driverResult = pow(float(driver.superSpeedwayRating), __DRIVER_FACTOR)
    elif track.type == 'restricted':
        driverResult = pow(float(driver.restrictedTrackRating), __DRIVER_FACTOR)
    elif track.type == 'road':
        driverResult = pow(float(driver.roadCourseRating), __DRIVER_FACTOR)
    else:
        raise Exception('Track type not defined')

    # teamResult = pow(team.raceRating, __TEAM_FACTOR)
    teamResult = pow(50, __TEAM_FACTOR)
    bonusResult = startingBonus * 50

    return round(((driverResult * teamResult) + bonusResult) / 100)


def __populateStandingsDict(drivers) -> None:
    """
    Populates the standingsDict with the standard standings that will be generated during race stage processing.

    :return: None
    :rtype: None
    """

    for driver in drivers:
        dictToAdd = {
            driver.name: {
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

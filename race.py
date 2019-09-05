from random import randint
import json
import potential

# Global Constant Parameters
DRIVER_FACTOR = 1.25
TEAM_FACTOR = 1.4

# Global Mutable Parameters
rateRangesDict = {}
standingsDict = {}
endingRange = 0


# def processStage(driversList, teamsList):
def processStage(driversList):
    # populateRangesDict(driversList)
    # populateStandingsDict(driversList)
    # qualifying()
    # race()
    # writeStandingsDictToFile()
    processDriverPotential(driversList, standingsDict)


# TODO: Fix driver class variable types

def calculateRange(driver, team_overall, startingBonus=0):
    driverResult = pow(float(driver.overallRating), DRIVER_FACTOR)
    teamResult = pow(team_overall, TEAM_FACTOR)
    bonusResult = startingBonus * 50

    return round(((driverResult * teamResult) + bonusResult) / 100)

# def calculateRange(driver, team, startingBonus=0):
#     driverResult = pow(driver.overallRating, DRIVER_FACTOR)
#     teamResult = pow(team.overall, TEAM_FACTOR)
#     bonusResult = startingBonus * 50
#
#     return round(((driverResult * teamResult) + bonusResult) / 100)


# def populateRangesDict(driversList, teamsList):
def populateRangesDict(driversList):
    startingRange = 0

    for driver in driversList:
        dictToAdd = {
            driver.name: {
                "startingRange": startingRange,
                "endingRange": 0
            }
        }

        startingRange += calculateRange(driver, 50)
        dictToAdd[driver.name]['endingRange'] = startingRange
        rateRangesDict.update(dictToAdd)
        startingRange += 1

        # for team in teamsList:
        #     # TODO: Check if driver is the only driver in teams driver list.
        #     if driver.name in team.drivers:
        #         startingRange += calculateRange(driver, team)
        #         dictToAdd[driver.name]['endingRange'] = startingRange
        #         rateRangesDict.update(dictToAdd)
        #         startingRange += 1
        #         break

    global endingRange
    endingRange = startingRange


# Populate with more standings criteria
def populateStandingsDict(driversList):
    for driver in driversList:
        dictToAdd = {
            driver.name: {
                "qualifyingPosition": 0,
                "finishingPosition": 0,
                "lapsLed": 0,
                "timesQualifyingRangeHit": 0,
                "timesRaceRangeHit": 0
            }
        }

        standingsDict.update(dictToAdd)


def qualifying():
    qualifyingPosition = 1

    while qualifyingPosition != len(standingsDict) + 1:
        randomNumber = randint(0, endingRange)

        for rateRange in rateRangesDict:
            if rateRangesDict[rateRange]['startingRange'] <= randomNumber <= rateRangesDict[rateRange]['endingRange']:
                if standingsDict[rateRange]['qualifyingPosition'] == 0:
                    standingsDict[rateRange]['qualifyingPosition'] = qualifyingPosition
                    standingsDict[rateRange]['timesQualifyingRangeHit'] += 1
                    qualifyingPosition += 1
                else:
                    standingsDict[rateRange]['timesQualifyingRangeHit'] += 1


def race():
    finishingPosition = 1

    while finishingPosition != len(standingsDict) + 1:
        randomNumber = randint(0, endingRange)

        for rateRange in rateRangesDict:
            if rateRangesDict[rateRange]['startingRange'] <= randomNumber <= rateRangesDict[rateRange]['endingRange']:
                if standingsDict[rateRange]['finishingPosition'] == 0:
                    standingsDict[rateRange]['finishingPosition'] = finishingPosition
                    standingsDict[rateRange]['timesRaceRangeHit'] += 1
                    finishingPosition += 1
                else:
                    standingsDict[rateRange]['timesRaceRangeHit'] += 1


def writeStandingsDictToFile():
    with open('data/json/standings.json', 'w') as standingsJSON:
        json.dump(standingsDict, standingsJSON, indent=4)


def processDriverPotential(driversList, standingsDict):
    if not standingsDict:
        getStandingsDict()

    potential.processStage(driversList, standingsDict)


def getStandingsDict():
    with open('data/json/standings.json', 'r') as standingsJSON:
        standingsDict.update(json.load(standingsJSON))
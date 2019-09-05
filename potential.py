import json
import fileutilities as futil

# Global Pseudo-Private Variable Declaration
__progressionDict = {}
__regressionDict = {}

__driverPotentialDict = {}


def processStage(standingsDict):
    driversDict = futil.readDictFromJSON('currentdrivers')
    __getPotentialDicts()
    __getDriverPotentialDict(driversDict)
    __calculateDriverPotential(driversDict, standingsDict)


def __getPotentialDicts():
    with open('data/json/progression.json', 'r') as progressionJSON:
        __progressionDict.update(json.load(progressionJSON))

    with open('data/json/regression.json', 'r') as regressionJSON:
        __regressionDict.update(json.load(regressionJSON))


def __getDriverPotentialDict(driversDict):
    for driver in driversDict:
        tempDict = {
            driver: {
                "age": driversDict[driver].age,
                "potential": driversDict[driver].potential
            }
        }

        __driverPotentialDict.update(tempDict)


# TODO: Update proper progression/regression training
def __calculateDriverPotential(driversDict, standingsDict):
    for driver in __driverPotentialDict:
        string = __driverPotentialDict[driver]['potential'].split(';')
        progression = string[0]
        ageRange = string[1]
        regression = string[2]

        standingPlacement = determineStandingPlacement(standingsDict[driver]['finishingPosition'])

        rate = __progressionDict[progression][standingPlacement]

        overallRating = float(driversDict[driver].overallRating)
        overallRating += rate
        driversDict[driver].overallRating = str(overallRating)

    futil.writeDictToJSON('currentdrivers', driversDict)


def determineStandingPlacement(finishingPosition):
    if finishingPosition == 1:
        return 'first'
    elif 2 <= finishingPosition <= 3:
        return 'top3'
    elif 4 <= finishingPosition <= 5:
        return 'top5'
    elif 6 <= finishingPosition <= 10:
        return 'top10'
    elif 11 <= finishingPosition <= 15:
        return 'top15'
    elif 16 <= finishingPosition <= 20:
        return 'top20'
    elif 21 <= finishingPosition <= 25:
        return 'top25'
    elif 26 <= finishingPosition <= 30:
        return 'top30'
    elif 31 <= finishingPosition <= 35:
        return 'top35'
    elif 36 <= finishingPosition <= 40:
        return 'top40'
    elif 41 <= finishingPosition:
        return 'DNF'
    elif finishingPosition == 'DNQ':
        return 'DNQ'

import json
from utilities import futil
from models.driver import Driver

# Global Pseudo-Private Variable Declaration
__progressionDict = {}
__regressionDict = {}

__driverPotentialDict = {}


def processStage(standingsDict, driversDict):
    __getPotentialDicts()
    __getDriverPotentialDict(driversDict)
    __calculateDriverPotential(driversDict, standingsDict)


def __getPotentialDicts():
    with open('data/json/potential/progression.json', 'r') as progressionJSON:
        __progressionDict.update(json.load(progressionJSON))

    with open('data/json/potential/regression.json', 'r') as regressionJSON:
        __regressionDict.update(json.load(regressionJSON))


def __getDriverPotentialDict():
    for driver in Driver.instances:
        tempDict = {
            driver: {
                "age": Driver.instances[driver].age,
                "potential": Driver.instances[driver].potential
            }
        }

        __driverPotentialDict.update(tempDict)


# TODO: Update proper progression/regression training
def __calculateDriverPotential(standingsDict):
    for driverName in __driverPotentialDict:
        driver = Driver.instances[driverName]

        string = __driverPotentialDict[driverName]['potential'].split(';')
        ageRange = string[1]

        standingPlacement = determineStandingPlacement(standingsDict[driverName]['finishingPosition'])
        rate = 0

        if driver.age < ageRange[0]:
            rate = __progressionDict[string[0]][standingPlacement]
        elif driver.age in ageRange:
            rate = __progressionDict['0p'][standingPlacement]
        elif driver.age > ageRange or driver.age > ageRange[1]:
            rate = __regressionDict[string[2]][standingPlacement]

        overallRating = float(Driver.instances[driverName].overallRating)
        overallRating += rate
        Driver.instances[driverName].overallRating = str(overallRating)

    futil.writeDictToJSON('currentdrivers', Driver.instances)


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

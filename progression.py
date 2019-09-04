import json

# Global Pseudo-Private Variable Declaration
__potentialDict = {}
__regressionDict = {}


def readPotential():
    with open('data/json/potential.json', 'r') as potentialJSON:
        __potentialDict.update(json.load(potentialJSON))

    with open('data/json/regression.json', 'r') as regressionJSON:
        __regressionDict.update(json.load(regressionJSON))


def getProgressionRates():
    progressionRates = []

    # for driver in driversList:
    #     progressionRates.append(driver.progressionRate)

    return progressionRates


def defineProgressionRate(driver):
    potential = ''
    ageRange = ''
    regression = ''

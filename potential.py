import json

# Global Pseudo-Private Variable Declaration
__progressionDict = {}
__regressionDict = {}


def __loadPotentialDicts():
    with open('data/json/potential.json', 'r') as potentialJSON:
        __progressionDict.update(json.load(potentialJSON))

    with open('data/json/regression.json', 'r') as regressionJSON:
        __regressionDict.update(json.load(regressionJSON))


def getPotentialRates():
    potentialRates = []

    # for driver in driversList:
    #     potentials.append(driver.potential)

    return potentials


def definePotential(driver):
    progression = ''
    ageRange = ''
    regression = ''

from timeit import default_timer as timer

from utilities import futil


def importDriversToTeam() -> None:
    """
    Populates the team dictionary with drivers.
    :return: None
    """

    driversDict = futil.readDictFromJSON('driver')
    teamsDict = futil.readDictFromJSON('team')

    for name in driversDict:
        driver = driversDict[name]
        if not driver.teamName == "" and driver.teamName in teamsDict:
            teamsDict[driver.teamName].drivers.append(driver.name)

    futil.writeDictToJSON('team', teamsDict)


def getFunctionTime() -> None:
    """
    Runs timeFunction() 25 times and gets the average time it takes to complete a subset of code.

    :return: None
    :rtype: None
    """

    timeAverages = []

    i = 0
    while i < 25:
        timeAverages.append(timeFunction())
        i += 1

    average = 0
    for time in timeAverages:
        average += time

    print(average / len(timeAverages))


def timeFunction() -> float:
    """
    Returns the total time taken to run the code

    :return: Total time
    :rtype: float
    """
    start = timer()
    # INSERT CODE HERE
    end = timer()
    return end - start

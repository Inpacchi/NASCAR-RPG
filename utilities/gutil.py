from timeit import default_timer as timer

from utilities import futil


def importDriversToTeam(teamType: str, driverType: str = None, driversDict: dict = None, teamsDict: dict = None) -> None:
    """
    Populates each Team model drivers list variable with their respective drivers.

    :return: None
    """

    if driverType is None and driversDict is None:
        raise Exception("You must define either a driver type or a driver dictionary!")
    elif driversDict is None:
        driversDict = futil.readDictFromJSON(driverType)

    if teamType is None and teamsDict is None:
        raise Exception("You must define either a team type or a team dictionary!")
    elif teamsDict is None:
        teamsDict = futil.readDictFromJSON(teamType)

    for name in driversDict:
        driver = driversDict[name]
        if not driver.teamName == "" and driver.teamName in teamsDict:
            teamsDict[driver.teamName].drivers.append(driver.name)

    futil.writeDictToJSON(teamType, teamsDict)


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

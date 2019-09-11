from timeit import default_timer as timer

from utilities import futil
from models.driver import Driver
from models.team import Team
from models.contract import Contract # Necessary for Driver object creation


def importDriversToTeam(teamType: str, driverType: str) -> None:
    """
    Populates each Team model drivers list variable with their respective drivers.

    :return: None
    """

    if Driver.instances == {}:
        futil.readDictFromJSON(driverType)

    if Team.instances == {}:
        futil.readDictFromJSON(teamType)

    for name in Driver.instances:
        driver = Driver.instances[name]
        if not driver.teamName == "" and driver.teamName in Team.instances:
            Team.instances[driver.teamName].drivers.append(driver)

    futil.writeDictToJSON(teamType, Team.instances)


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

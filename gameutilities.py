import fileutilities as futil


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
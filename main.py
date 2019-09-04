from models import *
import fileutilities as futil
import race
import json
import importlib

# Global Variables for Interactive Python
driversList = []
teamsList = []


def main():
    global driversList
    driversList = futil.readFromDriversJSON()

    global teamsList
    teamsList = futil.readFromTeamsJSON()


def printInfo():
    print("--- DRIVERS ---")
    for driverObject in driversList:
        driverObject.printInfo()

    # print("\n\n--- TEAMS ---")
    # for teamObject in teamsList:
    #     teamObject.printInfo()
    #     print()


# Overview: Ask user for parameters of driver and input to
# Driver class. Then call Driver.toString (?) or Driver.writeToJSON (?)
# to append data to drivers.json.
def createDrivers():
    # TODO
    print('Do nothing')

from models import *
import fileutilities as futil
import race
import json
import importlib

driversList = []
teamsList = []

def run():
    with open('data/json/teams.json', 'r') as teamsJSON:
        tempTeamsDict = json.load(teamsJSON)
        
        for tempTeam in tempTeamsDict:
            teamsList.append(team.Team(tempTeam))
            
    #race.processStage(driversList, teamsList)
    #fileutilities.writeDriversListToJSON(driversList)
    #futil.convertFromCSV()
    
def printInfo():
    for driver in driversList:
        print("--- DRIVERS ---")
        driver.toString()
        print()
    
    for team in teamsList:
        print("--- TEAMS ---")
        team.toString()
        print()

# Overview: Ask user for parameters of driver and input to 
# Driver class. Then call Driver.toString (?) or Driver.writeToJSON (?)
# to append data to drivers.json.
def createDrivers():
    # TODO
    print('Do nothing')
    

import random
import json

class Team:
    name = ""
    owner = ""
    overall = 0
    
    carManufacturer = ""
    
    equipmentRating = 0
    
    wins = 0
    dnf = 0
    
    sponsors = []
    drivers = []
    
    momentum = 0
    
    def __init__(self, team):
        self.name = team['Name']
        self.owner = team['Owner']
        self.overall = team['Overall']
        self.drivers = team['Drivers']
        
    # TODO replace str() with string.format()
    def toString(self):
        print("Team Name: " + self.name
            + "\nOwner: " + self.owner
            + "\nOverall: " + str(self.overall)
            + "\nDrivers: " + "".join(self.drivers))
        
    def writeToJSON(self):            
        with open('teams.json', 'w') as teamsJSON:
           json.dump(self, teamsJSON, indent = 4)
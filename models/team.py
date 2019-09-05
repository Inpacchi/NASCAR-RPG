import random
import json


class Team:
    name = ""
    owner = ""
    carManufacturer = ""

    equipmentRating = 0
    teamRating = 0
    raceRating = 0

    # TODO: Implement these features
    # wins = 0
    # dnf = 0
    # poles = 0
    # sponsors = []
    drivers = []

    momentum = 0

    def __init__(self, team):
        if type(team) == dict:
            self.name = team['name']
            self.owner = team['owner']
            self.carManufacturer = team['carManufacturer']
            self.equipmentRating = team['equipmentRating']
            self.teamRating = team['teamRating']
            self.raceRating = team['raceRating']
        else:
            self.name = team[0]
            self.owner = team[1]
            self.carManufacturer = team[2]
            self.equipmentRating = int(team[3])
            self.teamRating = int(team[4])
            self.raceRating = int(team[5])

    # TODO replace str() with string.format()
    def toString(self):
        print("Team Name:", self.name,
              "\nOwner:", self.owner,
              "\ncarManufacturer:", self.carManufacturer,
              "\nequipmentRating:", "".join(self.equipmentRating),
              "\nteamRating:", "".join(self.teamRating),
              "\nraceRating:", "".join(self.raceRating),
              "\nDrivers:", "".join(self.drivers))

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, indent=4)

    def toDict(self):
        return self.__dict__
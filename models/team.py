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
            self.drivers = team['drivers']
        else:  # Most likely coming from CSV, so no need to populate drivers
            self.name = team[0]
            self.owner = team[1]
            self.carManufacturer = team[2]
            self.equipmentRating = int(team[3])
            self.teamRating = int(team[4])
            self.raceRating = int(team[5])
            self.drivers = []

    def __str__(self):
        return (f'Team Name: {self.name}\n'
                f'Owner: {self.owner}\n'
                f'Car Manufacturer: {self.carManufacturer}\n'
                f'Equipment Rating: {self.equipmentRating}\n'
                f'Team Rating: {self.teamRating}\n'
                f'Race Rating: {self.raceRating}\n'
                f'Drivers: {self.drivers}\n')

    def toDict(self):
        return self.__dict__

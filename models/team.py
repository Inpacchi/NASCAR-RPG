import random
import json


class Team:
    instances = {}

    def __init__(self, team):
        self.name = team['name']
        self.owner = team['owner']
        self.carManufacturer = team['carManufacturer']
        self.equipmentRating = team['equipmentRating']
        self.teamRating = team['teamRating']
        self.raceRating = team['raceRating']
        self.drivers = team['drivers']

        Team.instances[self.name] = self

    def __str__(self):
        return (f'Team Name: {self.name}\n'
                f'Owner: {self.owner}\n'
                f'Car Manufacturer: {self.carManufacturer}\n'
                f'Equipment Rating: {self.equipmentRating}\n'
                f'Team Rating: {self.teamRating}\n'
                f'Race Rating: {self.raceRating}\n'
                f'Drivers: {self.drivers}\n')


class CharterTeam(Team):
    instances = {}
    CHARTER_DICT_PARAMETERS = ['number', 'placement', 'worth']

    def __init__(self, team, charterAmount, charterDict):
        super().__init__(team)
        self.charterAmount = charterAmount
        self.charterDict = {}
        self.charterDict.update(charterDict)
        CharterTeam.instances[self.name] = self

    def __str__(self):
        return (f'{super().__str__()}'
                f'Charter Amount: {self.charterAmount}\n'
                f'Charter Info: {self.charterDict}\n')

    def validateCharterDict(self):
        for charter in self.charterDict:
            if not all(parameter in self.charterDict[charter] for parameter in CharterTeam.CHARTER_DICT_PARAMETERS):
                raise Exception("Check the keys in charterDict and try again.")
        print('All charterDict parameters checked out!')

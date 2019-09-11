from webapp import db
from models.driver import Driver


def getDriverModels(driversList):
    driverModelsList = []

    for driver in driversList:
        if type(driver) in [dict, Driver]:
            driverModelsList.append(driver)
        else:
            return driversList
        # elif type(driver) == :
        #     driverModelsList.append(Driver.instances[driver])

    return driverModelsList


class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, nullable=False)
    owner = db.Column(db.String(32), index=True)
    carManufacturer = db.Column(db.String(32))
    equipmentRating = db.Column(db.Float, nullable=False)
    teamRating = db.Column(db.Float, nullable=False)
    raceRating = db.Column(db.Float, nullable=False)
    drivers = db.relationship('Driver', back_populates='team')

    instances = {}

    def __init__(self, team):
        self.name = team['name']
        self.owner = team['owner']
        self.carManufacturer = team['carManufacturer']
        self.equipmentRating = team['equipmentRating']
        self.teamRating = team['teamRating']
        self.raceRating = team['raceRating']

        if 'drivers' in team.keys():
            self.drivers = getDriverModels(team['drivers'])

        Team.instances[self.name] = self

    def __str__(self):
        return (f'Team Name: {self.name}\n'
                f'Owner: {self.owner}\n'
                f'Car Manufacturer: {self.carManufacturer}\n'
                f'Equipment Rating: {self.equipmentRating}\n'
                f'Team Rating: {self.teamRating}\n'
                f'Race Rating: {self.raceRating}\n'
                f'Drivers: {self.drivers}\n')

    def serialize(self):
        return {
            'name': self.name,
            'owner': self.owner,
            'carManufacturer': self.carManufacturer,
            'equipmentRating': self.equipmentRating,
            'teamRating': self.teamRating,
            'raceRating': self.raceRating,
            'drivers': self.drivers
        }



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

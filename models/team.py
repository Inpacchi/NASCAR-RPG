from webapp import db
from models.driver import Driver


class Team(db.Model):
    """
    Team Model Object

    id: A unique value identifying each time assigned when each team is committed to the database
    name: Name of the Team
    owner: Name of the Team owner
    carManufacturer: Name of the Team's car manufacturer
    equipmentRating: The rating of the team's equipment
    teamRating: The overall rating of the team
    raceRating: The average of equipment and team rating, which is applied to races
    drivers: Many-to-one relationship referring to each driver that is a member of the team
    instances: A dictionary that keeps track of each Team model object created
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, nullable=False)
    owner = db.Column(db.String(32), index=True)
    carManufacturer = db.Column(db.String(32))
    equipmentRating = db.Column(db.Float, nullable=False)
    teamRating = db.Column(db.Float, nullable=False)
    raceRating = db.Column(db.Float, nullable=False)
    drivers = db.relationship('Driver', back_populates='team')
    qualifyingResults = db.relationship('QualifyingResults')
    raceResults = db.relationship('RaceResults')

    instances = {}

    def __init__(self, team):
        self.name = team['name']
        self.owner = team['owner']
        self.carManufacturer = team['carManufacturer']
        self.equipmentRating = team['equipmentRating']
        self.teamRating = team['teamRating']
        self.raceRating = team['raceRating']

        if 'drivers' in team.keys():
            for driver in team['drivers']:
                if type(driver) in [dict, Driver]:
                    self.drivers.append(driver)
                else:
                    self.drivers = team['drivers']
                    break

        Team.instances[self.name] = self

    def __str__(self):
        return (f'Team Name: {self.name}\n'
                f'Owner: {self.owner}\n'
                f'Car Manufacturer: {self.carManufacturer}\n'
                f'Equipment Rating: {self.equipmentRating}\n'
                f'Team Rating: {self.teamRating}\n'
                f'Race Rating: {self.raceRating}\n'
                f'Drivers: {self.drivers}\n')

    def __repr__(self):
        return f'<gameapp.Team object for {self.name}'

    def serialize(self) -> dict:
        """
        Returns a JSON serializable object.

        :return: JSON object
        :rtype: dict
        """

        driversList = []
        for driver in self.drivers:
            driversList.append(driver.name)

        return {
            'name': self.name,
            'owner': self.owner,
            'carManufacturer': self.carManufacturer,
            'equipmentRating': float(self.equipmentRating),
            'teamRating': float(self.teamRating),
            'raceRating': float(self.raceRating),
            'drivers': driversList
        }


class CharterTeam(Team):
    """
    TODO: Define database parameters, may get integrated back into Team model object
    """
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

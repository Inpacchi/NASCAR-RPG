from webapp import db


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
    personnelRating = db.Column(db.Float, nullable=False)
    teamPerformance = db.Column(db.Float, nullable=False)
    drivers = db.relationship('TeamDrivers')
    rentals = db.relationship('TeamRentals')
    cars = db.relationship('TeamCars')
    qualifyingResults = db.relationship('QualifyingResults')
    raceResults = db.relationship('RaceResults')

    def __init__(self, team, switch = None):
        self.name = team['Name']
        self.carManufacturer = team['Manufacturer']
        self.equipmentRating = team['Equipment Rating']
        self.personnelRating = team['Personnel Rating']
        self.teamPerformance = team['Team Performance']

    def __str__(self):
        return (f'Team Name: {self.name}\n'
                f'Owner: {self.owner}\n'
                f'Car Manufacturer: {self.carManufacturer}\n'
                f'Equipment Rating: {self.equipmentRating}\n'
                f'Personnel Rating: {self.personnelRating}\n'
                f'Team Performance: {self.teamPerformance}\n')

    def __repr__(self):
        return f'<gameapp.Team object for {self.name}'

    def serialize(self) -> dict:
        """
        Returns a JSON serializable object.

        :return: JSON object
        :rtype: dict
        """

        return {
            'name': self.name,
            'owner': self.owner,
            'carManufacturer': self.carManufacturer,
            'equipmentRating': float(self.equipmentRating),
            'personnelRating': float(self.personnelRating),
            'teamPerformance': float(self.teamPerformance)
        }


class TeamRentals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    fromId = db.Column(db.Integer, db.ForeignKey('team.id'))
    toId = db.Column(db.Integer, db.ForeignKey('team.id'))
    equipmentBonus = db.Column(db.Integer)


class TeamCars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'))
    driverId = db.Column(db.Integer, db.ForeignKey('driver.id'))
    carNumber = db.Column(db.Integer)
    series = db.Column(db.String(32), index=True)


class TeamDrivers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'))
    driverId = db.Column(db.Integer, db.ForeignKey('driver.id'))
    series = db.Column(db.String(32), index=True)
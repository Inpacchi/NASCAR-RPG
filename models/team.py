from webapp import db


class Team(db.Model):
    """
    Team Model Object

    id: A unique value identifying each time assigned when each team is committed to the database
    name: Name of the Team
    owner: Name of the Team owner
    car_manufacturer: Name of the Team's car manufacturer
    equipment_rating: The rating of the team's equipment
    teamRating: The overall rating of the team
    raceRating: The average of equipment and team rating, which is applied to races
    drivers: Many-to-one relationship referring to each driver that is a member of the team
    instances: A dictionary that keeps track of each Team model object created
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, nullable=False)
    owner = db.Column(db.String(32), index=True)
    car_manufacturer = db.Column(db.String(32))
    equipment_rating = db.Column(db.Float, nullable=False)
    personnel_rating = db.Column(db.Float, nullable=False)
    team_performance = db.Column(db.Float, nullable=False)
    drivers = db.relationship('TeamDrivers')
    rentals = db.relationship('TeamRentals')
    cars = db.relationship('TeamCars')
    qualifying_results = db.relationship('QualifyingResults')
    race_results = db.relationship('RaceResults')

    def __init__(self, team, switch = None):
        self.name = team['Name']
        self.car_manufacturer = team['Manufacturer']
        self.equipment_rating = team['Equipment Rating']
        self.personnel_rating = team['Personnel Rating']
        self.team_performance = team['Team Performance']

    def __str__(self):
        return (f'Team Name: {self.name}\n'
                f'Owner: {self.owner}\n'
                f'Car Manufacturer: {self.car_manufacturer}\n'
                f'Equipment Rating: {self.equipment_rating}\n'
                f'Personnel Rating: {self.personnel_rating}\n'
                f'Team Performance: {self.team_performance}\n')

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
            'car_manufacturer': self.car_manufacturer,
            'equipment_rating': float(self.equipment_rating),
            'personnel_rating': float(self.personnel_rating),
            'team_performance': float(self.team_performance)
        }


class TeamRentals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    from_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    equipment_bonus = db.Column(db.Integer)


class TeamCars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    car_number = db.Column(db.Integer)
    series = db.Column(db.String(32), index=True)


class TeamDrivers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    series = db.Column(db.String(32), index=True)
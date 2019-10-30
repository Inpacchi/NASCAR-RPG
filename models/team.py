from models.driver import Driver
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
    car_manufacturer = db.Column(db.String(32), nullable=False)
    used_equipment_rating = db.Column(db.Float, nullable=False)
    actual_equipment_rating = db.Column(db.Float, nullable=False)
    personnel_rating = db.Column(db.Float, nullable=False)
    team_performance = db.Column(db.Float, nullable=False)
    notes = db.Column(db.String(128))
    equipment_rented_from = db.Column(db.Integer, db.ForeignKey('team.id'))
    drivers = db.relationship('TeamDrivers')
    cars = db.relationship('TeamCars')
    qualifying_results = db.relationship('QualifyingResults')
    race_results = db.relationship('RaceResults')

    def __init__(self, team):
        self.name = team['name']
        self.car_manufacturer = team['car_manufacturer']
        self.used_equipment_rating = team['used_equipment_rating']
        self.actual_equipment_rating = team['actual_equipment_rating']
        self.personnel_rating = team['personnel_rating']
        self.team_performance = team['team_performance']

        if team['notes'] is not None:
            self.notes = team['notes']

        if team['equipment_rented_from'] is not None:
            rental_team = team['equipment_rented_from']
            self.equipment_rented_from = Team.query.filter(Team.name.like(f'%{rental_team}%')).first().id

        if team['cup_cars'] is not None:
            cars = list(map(int, team['cup_cars'].split(',')))

            TeamCars('cup', cars, self.id)

        if team['xfinity_cars'] is not None:
        if team['gander_cars'] is not None:

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
    equipment_bonus = db.Column(db.Integer)
    from_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    to_id = db.Column(db.Integer, db.ForeignKey('team.id'))


class TeamCars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    series = db.Column(db.String(32), index=True)
    car_number = db.Column(db.Integer, index=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))

    def __init__(self, team_id, driver_id = None, car_number = None, cars = None, series = None):
        query = self.query.filter_by(team_id = team_id).first()

        if query is not None:
            self.handle_existing(query)
        else:
            self.handle_new()

        self.driver_id = driver_id
        self.team_id = team_id

        if car_number is not None:
            self.car_number = car_number

        if cars is not None:
            for car in cars:
                self.series = series
                self.car_number = car
                self.team_id = team_id

                if driver_id is not None:
                    self.driver_id = driver_id
                else:
                    self.driver_id = Driver

    def handle_new(self):
        print()

    def handle_existing(self, query):
        

class TeamDrivers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    series = db.Column(db.String(32), index=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))

    def __init__(self, driver_id, team_id):
        self.driver_id = driver_id
        self.team_id = team_id
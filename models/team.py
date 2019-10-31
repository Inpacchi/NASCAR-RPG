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
    name = db.Column(db.String(32), index=True, nullable=False, unique=True)
    owner = db.Column(db.String(32), index=True)
    car_manufacturer = db.Column(db.String(32), nullable=False)
    used_equipment_rating = db.Column(db.Float, nullable=False)
    actual_equipment_rating = db.Column(db.Float, nullable=False)
    personnel_rating = db.Column(db.Float, nullable=False)
    team_performance = db.Column(db.Float, nullable=False)
    notes = db.Column(db.String(128))
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
        if team['notes'] not in (None, ''):
            self.notes = team['notes']
        db.session.add(self)

    def __str__(self):
        return (f'Team Name: {self.name}\n'
                f'Owner: {self.owner}\n'
                f'Car Manufacturer: {self.car_manufacturer}\n'
                f'Equipment Rating: {self.equipment_rating}\n'
                f'Personnel Rating: {self.personnel_rating}\n'
                f'Team Performance: {self.team_performance}\n')

    def __repr__(self):
        return f'<gameapp.Team object for {self.name}>'

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

    def add_rental(self, equipment_lender_id):
        TeamRentals(equipment_lender_id, self.id, self.used_equipment_rating - self.actual_equipment_rating)

    def populate_cars(self, team):
        if team['cup_cars'] not in (None, ''):
            for car in team['cup_cars'].split(','):
                if car not in (None, ''):
                    TeamCars(car, self.id, series='cup')

        if team['xfinity_cars'] not in (None, ''):
            for car in team['xfinity_cars'].split(','):
                if car not in (None, ''):
                    TeamCars(car, self.id, series='xfinity')

        if team['gander_cars'] not in (None, ''):
            for car in team['gander_cars'].split(','):
                if car not in (None, ''):
                    TeamCars(car, self.id, series='truck')


class TeamRentals(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    equipment_bonus = db.Column(db.Integer)
    from_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    from_team = db.relationship('Team', foreign_keys=[from_id])
    to_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    to_team = db.relationship('Team', foreign_keys=[to_id])

    def __init__(self, from_id, to_id, equipment_bonus):
        if self.query.filter_by(from_id=from_id, to_id=to_id).scalar() is not None:
            row = self.query.filter_by(from_id=from_id, to_id=to_id).first()
            row.from_id = from_id
            row.to_id = to_id
            row.equipment_bonus = equipment_bonus
        else:
            self.from_id = from_id
            self.to_id = to_id
            self.equipment_bonus = equipment_bonus
            db.session.add(self)


class TeamCars(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    series = db.Column(db.String(32), index=True)
    car_number = db.Column(db.Integer, index=True)
    status = db.Column(db.String(2), index=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team = db.relationship('Team')
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    driver = db.relationship('Driver')

    def __init__(self, car_number, team_id, driver_id=None, series=None):
        if series is not None:
            car = int(car_number.split('p')[0])
            if TeamCars.query.filter_by(team_id=team_id, car_number=car, series=series).scalar() is not None:
                row = self.query.filter_by(series=series, car_number=car, team_id=team_id).first()
                row.update(car_number, team_id, series=series)
            else:
                self.update(car_number, team_id, series=series)
                db.session.add(self)
        elif driver_id is not None:
            if self.query.filter_by(team_id=team_id, driver_id=driver_id, car_number=car_number).scalar() is not None:
                row = self.query.filter_by(team_id=team_id, driver_id=driver_id, car_number=car_number).first()
                row.update(car_number, team_id, driver_id)
            else:
                self.update(car_number, team_id, driver_id)
                db.session.add(self)
        else:
            raise Exception('TeamCars requires a specific set of parameters that were not entered correctly')

    def update(self, car_number, team_id, driver_id=None, series=None):
        self.team_id = team_id
        if driver_id is not None:
            self.driver_id = driver_id
        if series is not None:
            self.series = series
        if 'p' in car_number:
            self.car_number = int(car_number.split('p')[0])
            self.status = 'pt'
        else:
            self.car_number = int(car_number)
            self.status = 'ft'


class TeamDrivers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    series = db.Column(db.String(32), index=True)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))

    def __init__(self, driver_id, team_id, series = None):
        if self.query.filter_by(team_id=team_id, driver_id=driver_id).scalar() is not None:
            row = self.query.filter_by(team_id=team_id, driver_id=driver_id).first()
            row.driver_id = driver_id
            row.team_id = team_id
            if series is not None:
                row.series = series
        else:
            self.driver_id = driver_id
            self.team_id = team_id
            if series is not None:
                self.series = series
            db.session.add(self)

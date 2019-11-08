from models.team import Team, TeamCars, TeamDrivers

from webapp import db


class Driver(db.Model):
    """
    Driver Model Object

    id: A unique value identifying each time assigned when each team is committed to the database
    name: Name of the Driver
    age: Age of the Driver
    team_id: Foreign key that associates a Team model object to the Driver
    team: Many-to-one relationship referring to the Driver's team
    contract: One-to-one relationship referring to the Driver's contract
    car_number: Number of the Driver's car
    short_rating: Short Track Rating
    short_intermediate_rating: Short-Intermediate Track Rating
    intermediate_rating: Intermediate Track Rating
    super_speedway_rating: Super Speedway Track Rating
    restricted_track_rating: Restricted (Super Speedway) Track Ratings
    road_course_rating: Road Course Rating
    overall_rating: An average of all the Driver's track ratings
    potential: The Driver's progression/peak/regression rate
    instances: A dictionary that keeps track of each Driver model object created
    """

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    short_rating = db.Column(db.Float, nullable=False)
    short_intermediate_rating = db.Column(db.Float, nullable=False)
    intermediate_rating = db.Column(db.Float, nullable=False)
    super_speedway_rating = db.Column(db.Float, nullable=False)
    restricted_track_rating = db.Column(db.Float, nullable=False)
    road_course_rating = db.Column(db.Float, nullable=False)
    overall_rating = db.Column(db.Float, nullable=False)
    potential = db.Column(db.String(16), nullable=False)
    qualifying_results = db.relationship('QualifyingResults')
    race_results = db.relationship('RaceResults')
    team = db.relationship('TeamDrivers')
    car = db.relationship('TeamCars')

    def __init__(self, driver):
        self.name = driver['name']
        self.age = driver['age']
        self.short_rating = driver['short_rating']
        self.short_intermediate_rating = driver['short_intermediate_rating']
        self.intermediate_rating = driver['intermediate_rating']
        self.super_speedway_rating = driver['super_speedway_rating']
        self.restricted_track_rating = driver['restricted_track_rating']
        self.road_course_rating = driver['road_course_rating']
        self.overall_rating = driver['overall_rating']
        self.potential = driver['potential']
        db.session.add(self)

    def add_team(self, driver):
        if driver['team_name'] not in [None, '']:
            name = driver['team_name']
            try:
                team_id = Team.query.filter(Team.name.like(f'%{name}%')).first().id
            except AttributeError as ae:
                raise Exception(f'Query for "{name}" returned no results') from ae
            if driver['car_number'] not in [None, '']:
                try:
                    car = TeamCars.query.filter_by(car_number=driver['car_number'], team_id=team_id).first()
                    car.driver_id = self.id
                except AttributeError as ae:
                    car_number = driver['car_number']
                    raise Exception(f'Query for "{name}" and car number "{car_number}" returned no results') from ae
                TeamDrivers(self.id, team_id, car.series)
            else:
                TeamDrivers(self.id, team_id)

    def __str__(self):
        return (f'Driver Name: {self.name}\n'
                f'Age: {self.age}\n'
                f'Short Track Rating: {self.short_rating}\n'
                f'Short-Intermediate Track Rating: {self.short_intermediate_rating}\n'
                f'Intermediate Track Rating: {self.intermediate_rating}\n'
                f'Superspeedway Track Rating: {self.super_speedway_rating}\n'
                f'Restricted (Super Speedway) Track Rating: {self.restricted_track_rating}\n'
                f'Road Course Rating: {self.road_course_rating}\n'
                f'Overall Rating: {self.overall_rating}\n'
                f'Potential: {self.potential}\n')

    def __repr__(self):
        return f'<gameapp.Driver object for {self.name}>'

    def serialize(self) -> dict:
        """
        Returns a JSON serializable object.

        :return: JSON object
        :rtype: dict
        """

        return {
            'name': self.name,
            'age': int(self.age),
            'teamName': self.teamName,
            'car_number': int(self.car_number),
            'short_rating': float(self.short_rating),
            'short_intermediate_rating': float(self.short_intermediate_rating),
            'intermediate_rating': float(self.intermediate_rating),
            'super_speedway_rating': float(self.super_speedway_rating),
            'restricted_track_rating': float(self.restricted_track_rating),
            'road_course_rating': float(self.road_course_rating),
            'overall_rating': float(self.overall_rating),
            'potential': self.potential
        }

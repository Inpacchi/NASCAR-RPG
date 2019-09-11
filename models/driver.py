from webapp import db


class Driver(db.Model):
    instances = {}

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), index=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'), index=True)
    team = db.relationship('Team', back_populates='drivers')
    contract = db.relationship('Contract', uselist=False, back_populates='driver')
    carNumber = db.Column(db.Integer, index=True)
    shortRating = db.Column(db.Float, nullable=False)
    shortIntermediateRating = db.Column(db.Float, nullable=False)
    intermediateRating = db.Column(db.Float, nullable=False)
    superSpeedwayRating = db.Column(db.Float, nullable=False)
    restrictedTrackRating = db.Column(db.Float, nullable=False)
    roadCourseRating = db.Column(db.Float, nullable=False)
    overallRating = db.Column(db.Float, nullable=False)
    potential = db.Column(db.String(16), nullable=False)

    def __init__(self, driver):
        self.name = driver['name']
        self.age = driver['age']
        self.teamName = driver['teamName']
        self.carNumber = driver['carNumber']
        self.shortRating = driver['shortRating']
        self.shortIntermediateRating = driver['shortIntermediateRating']
        self.intermediateRating = driver['intermediateRating']
        self.superSpeedwayRating = driver['superSpeedwayRating']
        self.restrictedTrackRating = driver['restrictedTrackRating']
        self.roadCourseRating = driver['roadCourseRating']
        self.overallRating = driver['overallRating']
        self.potential = driver['potential']

        Driver.instances[self.name] = self

    def __str__(self):
        return (f'Driver Name: {self.name}\n'
                f'Age: {self.age}\n'
                f'Team Name: {self.teamName}\n'
                f'Car Number: {self.carNumber}\n'
                f'Short Track Rating: {self.shortRating}\n'
                f'Short-Intermediate Track Rating: {self.shortIntermediateRating}\n'
                f'Intermediate Track Rating: {self.intermediateRating}\n'
                f'Superspeedway Track Rating: {self.superSpeedwayRating}\n'
                f'Restricted (Super Speedway) Track Rating: {self.restrictedTrackRating}\n'
                f'Road Course Rating: {self.roadCourseRating}\n'
                f'Overall Rating: {self.overallRating}\n'
                f'Potential: {self.potential}\n')

    def serialize(self):
        return {
            'name': self.name,
            'age': int(self.age),
            'teamName': self.teamName,
            'carNumber': int(self.carNumber),
            'shortRating': float(self.shortRating),
            'shortIntermediateRating': float(self.shortIntermediateRating),
            'intermediateRating': float(self.intermediateRating),
            'superSpeedwayRating': float(self.superSpeedwayRating),
            'restrictedTrackRating': float(self.restrictedTrackRating),
            'roadCourseRating': float(self.roadCourseRating),
            'overallRating': float(self.overallRating),
            'potential': self.potential
        }

from datetime import datetime

from webapp import db


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    length = db.Column(db.Float)
    type = db.Column(db.String(32))
    schedule = db.relationship('Schedule')

    def __init__(self, track):
        self.name = track['name']
        self.length = track['length']
        self.type = track['type']

    def __str__(self):
        return (f'Track Name: {self.name}\n'
                f'Length: {self.length}\n'
                f'Type: {self.type}\n')

    def __repr__(self):
        return f'<gameapp.Track object for {self.name}>'


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    date = db.Column(db.Date)
    type = db.Column(db.String(16))
    trackId = db.Column(db.Integer, db.ForeignKey('track.id'))
    laps = db.Column(db.Integer)
    stages = db.Column(db.String(32))
    # stages = db.Column(db.Array(db.Integer))  # PostgreSQL
    raceProcessed = db.Column(db.String(3))

    def __init__(self, schedule):
        self.name = schedule['name']
        self.date = datetime.strptime(schedule['date'], '%m/%d/%Y').date()
        self.type = schedule['type']
        self.trackId = Track.query.filter_by(name=schedule['track']).first().id
        self.laps = schedule['laps']
        self.stages = schedule['stages']
        self.raceProcessed = schedule['raceProcessed']

    def __str__(self):
        return (f'Race Name: {self.name}\n'
                f'Date: {self.date}\n'
                f'Type: {self.type}\n'
                f'Track: {Track.query.filter_by(id=self.id).first().name}'
                f'Laps: {self.laps}'
                f'Stages: {self.stages}'
                f'Race Processed? {self.raceProcessed}')

    def __repr__(self):
        return f'<gameapp.Schedule object for {self.name}>'


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(32), index=True)
    length = db.Column(db.Integer)
    salary = db.Column(db.Float)
    driverId = db.Column(db.Integer, db.ForeignKey('driver.id'))
    driver = db.relationship('Driver', uselist=False, back_populates='contract')

    def __str__(self):
        return (f'Status: {self.status}\n'
                f'Length: {self.length}\n'
                f'Salary: {self.salary}\n'
                f'Driver: {self.driver}\n')

    def __repr__(self):
        return f'<gameapp.Contract object for {self.driver}>'

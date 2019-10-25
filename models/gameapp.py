from datetime import datetime

from webapp import db


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    length = db.Column(db.Float)
    type = db.Column(db.String(32))
    #location = db.Column(db.String(64))
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
    qualifyingResults = db.relationship('QualifyingResults')
    raceResults = db.relationship('RaceResults')

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


class QualifyingResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raceId = db.Column(db.Integer, db.ForeignKey('schedule.id'))
    driverId = db.Column(db.Integer, db.ForeignKey('driver.id'))
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'))
    position = db.Column(db.Integer, index=True)
    fastestLap = db.Column(db.Float, index=True)
    rangeHits = db.Column(db.Integer)

    def __init__(self, driverId, standingsDict):
        self.driverId = driverId
        self.position = standingsDict['qualifyingPosition']
        self.rangeHits = standingsDict['timesQualifyingRangeHit']


class RaceResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raceId = db.Column(db.Integer, db.ForeignKey('schedule.id'))
    driverId = db.Column(db.Integer, db.ForeignKey('driver.id'))
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'))
    position = db.Column(db.Integer, index=True)
    lapsLed = db.Column(db.Integer, index=True)
    fastestLap = db.Column(db.Float, index=True)
    rangeHits = db.Column(db.Integer)

    def __init__(self, driverId, standingsDict):
        self.driverId = driverId
        self.position = standingsDict['finishingPosition']
        self.rangeHits = standingsDict['timesRaceRangeHit']


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    def __str__(self):
        return (f'Status: {self.status}\n'
                f'Length: {self.length}\n'
                f'Salary: {self.salary}\n'
                f'Driver: {self.driver}\n')

    def __repr__(self):
        return f'<gameapp.Contract object for {self.driver}>'

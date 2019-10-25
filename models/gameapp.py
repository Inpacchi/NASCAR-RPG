from datetime import datetime

from models.driver import Driver
from models.team import Team
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

    def __init__(self, standings, driverId, teamId = None):
        self.driverId = driverId
        self.position = standings['qualifyingPosition']
        self.rangeHits = standings['timesQualifyingRangeHit']

        if standings['raceId'] != 0:
            self.raceId = standings['raceId']

        if teamId is not None:
            self.teamId = teamId

    def __str__(self):
        return ('Qualifying Results:\n'
                f'Race: {Schedule.query.filter_by(id=self.raceId).first().name}\n'
                f'Driver: {Driver.query.filter_by(id=self.driverId.first().name)}\n'
                f'Team: {Team.query.filter_by(id=self.teamId.first().name)}\n'
                f'Position: {self.position}\n'
                f'Fastest Lap: {self.fastestLap}\n'
                f'Range Hits: {self.rangeHits}')

    def __repr__(self):
        return f'<gameapp.QualifyingResults object for {Schedule.query.filter_by(id=self.raceId).first().name}'


class RaceResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    raceId = db.Column(db.Integer, db.ForeignKey('schedule.id'))
    driverId = db.Column(db.Integer, db.ForeignKey('driver.id'))
    teamId = db.Column(db.Integer, db.ForeignKey('team.id'))
    position = db.Column(db.Integer, index=True)
    lapsLed = db.Column(db.Integer, index=True)
    fastestLap = db.Column(db.Float, index=True)
    rangeHits = db.Column(db.Integer)

    def __init__(self, standings, driverId, teamId = None):
        self.driverId = driverId
        self.position = standings['finishingPosition']
        self.rangeHits = standings['timesRaceRangeHit']

        if standings['raceId'] != 0:
            self.raceId = standings['raceId']

        if teamId is not None:
            self.teamId = teamId

    def __str__(self):
        return ('Race Results:\n'
                f'Race: {Schedule.query.filter_by(id=self.raceId).first().name}\n'
                f'Driver: {Driver.query.filter_by(id=self.driverId.first().name)}\n'
                f'Team: {Team.query.filter_by(id=self.teamId.first().name)}\n'
                f'Position: {self.position}\n'
                f'Laps Led: {self.lapsLed}\n'
                f'Fastest Lap: {self.fastestLap}\n'
                f'Range Hits: {self.rangeHits}')

    def __repr__(self):
        return f'<gameapp.RaceResults object for {Schedule.query.filter_by(id=self.raceId).first().name}'

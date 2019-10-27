from datetime import datetime

from models.driver import Driver
from models.team import Team
from webapp import db


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    length = db.Column(db.Float)
    type = db.Column(db.String(32))
    location = db.Column(db.String(64))
    schedule = db.relationship('Schedule')

    def __init__(self, track):
        self.name = track['name']
        self.length = track['length']
        self.type = track['type']
        self.location = track['location']

    def __str__(self):
        return (f'Track Name: {self.name}\n'
                f'Length: {self.length}\n'
                f'Type: {self.type}\n'
                f'Location: {self.location}\n')

    def __repr__(self):
        return f'<gameapp.Track object for {self.name}>'


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    date = db.Column(db.Date)
    type = db.Column(db.String(16))
    track_id = db.Column(db.Integer, db.ForeignKey('track.id'))
    laps = db.Column(db.Integer)
    stages = db.Column(db.Array(db.Integer))
    race_processed = db.Column(db.Boolean)
    qualifying_results = db.relationship('QualifyingResults')
    race_results = db.relationship('RaceResults')

    def __init__(self, schedule):
        self.name = schedule['name']
        self.date = datetime.strptime(schedule['date'], '%m/%d/%Y').date()
        self.type = schedule['type']
        self.track_id = Track.query.filter_by(name=schedule['track']).first().id
        self.laps = schedule['laps']
        self.stages = schedule['stages']
        self.race_processed = schedule['race_processed']

    def __str__(self):
        return (f'Race Name: {self.name}\n'
                f'Date: {self.date}\n'
                f'Type: {self.type}\n'
                f'Track: {Track.query.filter_by(id=self.id).first().name}'
                f'Laps: {self.laps}'
                f'Stages: {self.stages}'
                f'Race Processed? {self.race_processed}')

    def __repr__(self):
        return f'<gameapp.Schedule object for {self.name}>'


class QualifyingResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('schedule.id'))
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    position = db.Column(db.Integer, index=True)
    fastest_lap = db.Column(db.Float, index=True)
    range_hits = db.Column(db.Integer)

    def __init__(self, standings, driver_id, team_id = None):
        self.driver_id = driver_id
        self.position = standings['qualifying_position']
        self.range_hits = standings['times_qualifying_range_hit']

        if standings['race_id'] != 0:
            self.race_id = standings['race_id']

        if team_id is not None:
            self.team_id = team_id

    def __str__(self):
        return ('Qualifying Results:\n'
                f'Race: {Schedule.query.filter_by(id=self.race_id).first().name}\n'
                f'Driver: {Driver.query.filter_by(id=self.driver_id.first().name)}\n'
                f'Team: {Team.query.filter_by(id=self.team_id.first().name)}\n'
                f'Position: {self.position}\n'
                f'Fastest Lap: {self.fastest_lap}\n'
                f'Range Hits: {self.range_hits}')

    def __repr__(self):
        return f'<gameapp.QualifyingResults object for {Schedule.query.filter_by(id=self.race_id).first().name}'


class RaceResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('schedule.id'))
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    position = db.Column(db.Integer, index=True)
    laps_led = db.Column(db.Integer, index=True)
    fastest_lap = db.Column(db.Float, index=True)
    range_hits = db.Column(db.Integer)

    def __init__(self, standings, driver_id, team_id = None):
        self.driver_id = driver_id
        self.position = standings['finishing_position']
        self.range_hits = standings['times_race_range_hit']

        if standings['race_id'] != 0:
            self.race_id = standings['race_id']

        if team_id is not None:
            self.team_id = team_id

    def __str__(self):
        return ('Race Results:\n'
                f'Race: {Schedule.query.filter_by(id=self.race_id).first().name}\n'
                f'Driver: {Driver.query.filter_by(id=self.driver_id.first().name)}\n'
                f'Team: {Team.query.filter_by(id=self.team_id.first().name)}\n'
                f'Position: {self.position}\n'
                f'Laps Led: {self.laps_led}\n'
                f'Fastest Lap: {self.fastest_lap}\n'
                f'Range Hits: {self.range_hits}')

    def __repr__(self):
        return f'<gameapp.RaceResults object for {Schedule.query.filter_by(id=self.race_id).first().name}'

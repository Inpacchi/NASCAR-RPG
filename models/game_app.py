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
        if 'location' in track.keys():
            self.location = track['location']

    def __str__(self):
        return (f'Track Name: {self.name}\n'
                f'Length: {self.length}\n'
                f'Type: {self.type}\n'
                f'Location: {self.location}\n')

    def __repr__(self):
        return f'<game_app.Track>[{self.name}]'


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_number = db.Column(db.Integer)
    name = db.Column(db.String(64), index=True, nullable=False)
    date = db.Column(db.Date)
    type = db.Column(db.String(16))
    track_id = db.Column(db.Integer, db.ForeignKey('track.id'))
    laps = db.Column(db.Integer)
    stages = db.Column(db.ARRAY(db.Integer))
    average_position_change_per_lap = db.Column(db.Integer)
    average_laps_under_caution = db.Column(db.Integer)
    race_processed = db.Column(db.Boolean)
    qualifying_results = db.relationship('QualifyingResults')
    race_results = db.relationship('RaceResults')

    def __init__(self, schedule):
        self.name = schedule['name']
        self.type = schedule['type']
        self.laps = schedule['laps']
        self.event_number = schedule['event_number']
        self.date = datetime.strptime(schedule['date'], '%m/%d/%Y').date()
        self.track_id = Track.query.filter_by(name=schedule['track']).first().id
        if schedule['stages'] != '':
            self.stages = (int(stage) for stage in schedule['stages'].split(','))
        if schedule['race_processed'] in ('true', 'True', 'yes', 'y', 'Y'):
            self.race_processed = True
        elif schedule['race_processed'] in ('false', 'False', ' no', 'n', 'N'):
            schedule['race_processed'] = False
        else:
            race_processed = schedule['race_processed']
            raise TypeError(f'"{race_processed}" is not a valid type.')

    def __str__(self):
        return (f'Race Name: {self.name}\n'
                f'Date: {self.date}\n'
                f'Type: {self.type}\n'
                f'Track: {Track.query.filter_by(id=self.id).first().name}'
                f'Laps: {self.laps}'
                f'Stages: {self.stages}'
                f'Race Processed? {self.race_processed}')

    def __repr__(self):
        return f'<game_app.Schedule>[{self.name}]'


class QualifyingResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('schedule.id'))
    track_id = db.Column(db.Integer, db.ForeignKey('track.id'))
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    process_date_time = db.Column(db.DateTime)
    position = db.Column(db.Integer)
    fastest_time = db.Column(db.Float)
    top_speed = db.Column(db.Float)

    def __init__(self, driver_id, team_id, track_id, process_date_time, standings):
        self.driver_id = driver_id
        self.team_id = team_id
        self.track_id = track_id
        self.process_date_time = process_date_time
        self.position = standings['qualifying_position']
        self.fastest_time = standings['fastest_time']
        self.top_speed = standings['top_speed']
        if standings['race_id'] != 0:
            self.race_id = standings['race_id']

    def __str__(self):
        return ('Qualifying Results:\n'
                f'Race: {Schedule.query.filter_by(id=self.race_id).first().name}\n'
                f'Track: {Track.query.filter_by(id=self.track_id.first().name)}\n'
                f'Driver: {Driver.query.filter_by(id=self.driver_id.first().name)}\n'
                f'Team: {Team.query.filter_by(id=self.team_id.first().name)}\n'
                f'Position: {self.position}\n'
                f'Fastest Lap: {self.fastest_time}\n'
                f'Top Speed: {self.top_speed}')

    def __repr__(self):
        return f'<game_app.QualifyingResults>[{Schedule.query.filter_by(id=self.race_id).first().name}]'


class RaceResults(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    race_id = db.Column(db.Integer, db.ForeignKey('schedule.id'))
    track_id = db.Column(db.Integer, db.ForeignKey('track.id'))
    driver_id = db.Column(db.Integer, db.ForeignKey('driver.id'))
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    process_date_time = db.Column(db.DateTime)
    start_position = db.Column(db.Integer)
    mid_race_position = db.Column(db.Integer)
    finish_position = db.Column(db.Integer)
    lowest_position = db.Column(db.Integer)
    highest_position = db.Column(db.Integer)
    average_position = db.Column(db.Integer)
    top_15_lap_count = db.Column(db.Integer)
    top_15_lap_percentage = db.Column(db.Integer)
    lap_lead_count = db.Column(db.Integer)
    lap_lead_percentage = db.Column(db.Integer)
    total_lap_count = db.Column(db.Integer)
    driver_rating = db.Column(db.Integer)

    def __init__(self, driver_id, team_id,  track_id, process_date_time, standings):
        self.driver_id = driver_id
        self.team_id = team_id
        self.track_id = track_id
        self.process_date_time = process_date_time
        self.start_position = standings['start_position']
        self.mid_race_position = standings['mid_race_position']
        self.finish_position = standings['finish_position']
        self.lowest_position = standings['lowest_position']
        self.highest_position = standings['highest_position']
        self.top_15_lap_count = standings['top_15_lap_count']
        self.lap_lead_count = standings['lap_lead_count']
        self.total_lap_count = standings['total_lap_count']
        if standings['race_id'] != 0:
            self.race_id = standings['race_id']

    def __str__(self):
        return ('Race Results:\n'
                f'Race: {Schedule.query.filter_by(id=self.race_id).first().name}\n'
                f'Track: {Track.query.filter_by(id=self.track_id.first().name)}\n'
                f'Driver: {Driver.query.filter_by(id=self.driver_id.first().name)}\n'
                f'Team: {Team.query.filter_by(id=self.team_id.first().name)}\n'
                f'Start Position: {self.start_position}\n'
                f'Mid-Race Position: {self.mid_race_position}\n'
                f'Finish Position: {self.finish_position}\n'
                f'Lowest Position: {self.lowest_position}\n'
                f'Highest Position: {self.highest_position}\n'
                f'Average Position: {self.average_position}\n'
                f'Top 15 Lap Count : {self.top_15_lap_count}\n'
                f'Top 15 Lap Percentage: {self.top_15_lap_percentage}\n'
                f'Lap Lead Count: {self.lap_lead_count}\n'
                f'Lap Lead Percentage: {self.lap_lead_percentage}\n'
                f'Total Lap Count: {self.total_lap_count}\n'
                f'Driver Rating: {self.driver_rating}')

    def __repr__(self):
        return f'<game_app.RaceResults>[{Schedule.query.filter_by(id=self.race_id).first().name}]'

from webapp import db


class Track(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    length = db.Column(db.Float)
    type = db.Column(db.String(32))
    schedule = db.relationship('Schedule', secondary='TrackScheduleAssociation')


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, nullable=False)
    date = db.Column(db.Date)
    type = db.Column(db.String(16))
    track = db.relationship('Track', secondary='TrackScheduleAssociation')
    laps = db.Column(db.Integer)
    stages = db.Column(db.String(32))
    # stages = db.Column(db.Array(db.Integer))  # PostgreSQL
    raceProcessed = db.Column(db.String(3))


class TrackScheduleAssociation(db.Model):
    trackId = db.Column(db.Integer, db.ForeignKey('track.id'), primary_key=True)
    scheduleId = db.Column(db.Integer, db.ForeignKey('schedule.id'), primary_key=True)


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(32), index=True)
    length = db.Column(db.Integer)
    salary = db.Column(db.Float)
    driverId = db.Column(db.Integer, db.ForeignKey('driver.id'))
    driver = db.relationship('Driver', uselist=False, back_populates='contract')
from webapp import db


class Contract(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.String(32), index=True)
    length = db.Column(db.Integer)
    salary = db.Column(db.Float)
    driverId = db.Column(db.Integer, db.ForeignKey('driver.id'))
    driver = db.relationship('Driver', uselist=False, back_populates='contract')
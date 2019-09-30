from time import time

import jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

from webapp import app, db, login


@login.user_loader
def loadUser(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return f'<User {self.username}>'

    def setPassword(self, password):
        self.password_hash = generate_password_hash(password)

    def checkPassword(self, password):
        return check_password_hash(self.password_hash, password)

    def getResetPasswordToken(self, expiresIn=600):
        return jwt.encode({'resetPassword': self.id, 'exp': time() + expiresIn}, app.config['SECRET_KEY'],
                          algorithm='HS256').decode('utf-8')

    @staticmethod
    def verifyResetPasswordToken(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])['resetPassword']
        except Exception:
            return

        return User.query.get(id)

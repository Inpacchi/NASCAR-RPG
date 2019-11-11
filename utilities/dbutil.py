from datetime import datetime

from sqlalchemy.exc import SQLAlchemyError

from models.game_app import QualifyingResults, RaceResults
from models.driver import Driver
from models.team import Team

from webapp import db


def add_standings_to_session(standings, track):
    date_time = datetime.now()
    for block in standings:
        driver = Driver.query.filter_by(name=block).first()

        if len(driver.team) == 1:
            team_id = Team.query.filter_by(id=driver.team[0].team_id).first().id
        else:
            team_id = None

        db.session.add(QualifyingResults(standings[block], track.id, date_time, driver.id, team_id))
        db.session.add(RaceResults(standings[block], track.id, date_time, driver.id, team_id))


def commit():
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
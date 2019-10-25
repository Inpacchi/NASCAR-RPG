from models.gameapp import QualifyingResults, RaceResults
from models.driver import Driver

from webapp import db


def populateStandings(standings):
    for block in standings:
        driver = Driver.query.filter_by(name=block).first()

        db.session.add(QualifyingResults(standings[block], driver.id))
        db.session.add(RaceResults(standings[block], driver.id))

        db.session.commit()

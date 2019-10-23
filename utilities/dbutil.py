from models.gameapp import QualifyingResults, RaceResults
from models.driver import Driver

from webapp import db

def populateStandings(standingsDict):
    for blockName in standingsDict:
        driver = Driver.query.filter_by(name=blockName).first()

        db.session.add(QualifyingResults(driver.id, standingsDict[blockName]))
        db.session.add(RaceResults(driver.id, standingsDict[blockName]))

        db.session.commit()
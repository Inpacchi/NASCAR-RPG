import importlib

from models.team import Team, TeamCars, TeamRentals, TeamDrivers
from models.driver import Driver
from models.gameapp import Schedule, Track, QualifyingResults, RaceResults
from game import potential, raceweekend, test_race_weekend
from utilities import futil, dbutil
from webapp import db

print('Interactive Setup Completed!')
import importlib, json

from models.team import Team, TeamCars, TeamRentals, TeamDrivers
from models.driver import Driver
from models.game_app import Schedule, Track, QualifyingResults, RaceResults
from game import potential, raceweekend, test_race_weekend
from utilities import futil, dbutil, gutil
from webapp import db

print('Interactive Setup Completed!')
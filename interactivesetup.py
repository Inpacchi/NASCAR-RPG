import importlib

from models import *
from game import  *
from utilities import *

driversDict = futil.readDictFromJSON('driver')
teamsDict = futil.readDictFromJSON('team')
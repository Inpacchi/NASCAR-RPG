import importlib

from models import *
from game import  *
from utilities import *

driversList = futil.readDictFromJSON('driver')
teamsList = futil.readDictFromJSON('team')
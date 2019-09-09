import importlib

from models import *
from game import  *
from utilities import *

# futil.readDictFromJSON('driver')
# futil.readDictFromJSON('team')

# HM = team.Team.instances.get('Hendrick Motorsports')
#
# charterInfo = {
#     5: {
#         'number': 5,
#         'placement': [],
#         'worth': 0
#     },
#     24: {
#         'number': 24,
#         'placement': [],
#         'worth': 0
#     },
#     48: {
#         'number': 48,
#         'placement': [],
#         'worth': 0
#     },
#     88: {
#         'number': 88,
#         'placement': [],
#         'worth': 0
#     }
# }
#
# test = team.CharterTeam(HM, 4, charterInfo)
#
# modelList = {
#     test.name: test
# }
#
# futil.writeDictToJSON('charterteam', modelList)
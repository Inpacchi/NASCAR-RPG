import json
from utilities import futil
from models.driver import Driver

progression = {}
regression = {}

driver_potential = {}


def process_stage(standings, driversDict):
    _load_potential_rates()
    _load_driver_potential(driversDict)
    _calculate_driver_potential(driversDict, standings)


def _load_potential_rates():
    with open('data/json/potential/progression.json', 'r') as progressionJSON:
        progression.update(json.load(progressionJSON))

    with open('data/json/potential/regression.json', 'r') as regressionJSON:
        regression.update(json.load(regressionJSON))


def _load_driver_potential():
    for driver in Driver.instances:
        temp_dict = {
            driver: {
                "age": Driver.instances[driver].age,
                "potential": Driver.instances[driver].potential
            }
        }

        driver_potential.update(temp_dict)


# TODO: Update proper progression/regression training
def _calculate_driver_potential(standings):
    for driver_name in driver_potential:
        driver = Driver.instances[driver_name]

        string = driver_potential[driver_name]['potential'].split(';')
        age_range = string[1]

        standing_placement = determine_standing_placement(standings[driver_name]['finishing_position'])
        rate = 0

        if driver.age < age_range[0]:
            rate = progression[string[0]][standing_placement]
        elif driver.age in age_range:
            rate = progression['0p'][standing_placement]
        elif driver.age > age_range or driver.age > age_range[1]:
            rate = regression[string[2]][standing_placement]

        overall_rating = float(Driver.instances[driver_name].overall_rating)
        overall_rating += rate
        Driver.instances[driver_name].overall_rating = str(overall_rating)

    futil.write_dict_to_json('currentdrivers', Driver.instances)


def determine_standing_placement(finishing_position):
    if finishing_position == 1:
        return 'first'
    elif 2 <= finishing_position <= 3:
        return 'top3'
    elif 4 <= finishing_position <= 5:
        return 'top5'
    elif 6 <= finishing_position <= 10:
        return 'top10'
    elif 11 <= finishing_position <= 15:
        return 'top15'
    elif 16 <= finishing_position <= 20:
        return 'top20'
    elif 21 <= finishing_position <= 25:
        return 'top25'
    elif 26 <= finishing_position <= 30:
        return 'top30'
    elif 31 <= finishing_position <= 35:
        return 'top35'
    elif 36 <= finishing_position <= 40:
        return 'top40'
    elif 41 <= finishing_position:
        return 'DNF'
    elif finishing_position == 'DNQ':
        return 'DNQ'

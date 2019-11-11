import random
from math import floor

from game.race_stats_calculator import calculate_average_position_change_by_range
from models.driver import Driver
from models.team import Team
from utilities import futil

DRIVER_FACTOR = 1.25
TEAM_FACTOR = 1.4

standings = {}
rate_ranges = {}
ending_range = None

position_bonuses = {
    1: .25,
    2: .18,
    3: .18,
    4: .15,
    5: .15,
    6: .12,
    7: .12,
    8: .12,
    9: .10,
    10: .10,
    11: .07,
    12: .07,
    13: .07,
    14: .06,
    15: .06,
    16: .05,
    17: .05,
    18: .05,
    19: .05,
    20: .04,
    21: .04,
    22: .04,
    23: .04,
    24: .03,
    25: .03,
    26: .03,
    27: .03,
    28: .03,
    29: .02,
    30: .02,
    31: .02,
    32: .02,
    33: .02,
    34: .02,
    35: .02,
    36: .01,
    37: .01,
    38: .01,
    39: .01,
    40: .01
}


def process_stage():
    drivers_db = Driver.query.all()
    drivers = []

    for driver in drivers_db:
        if len(driver.team) == 1:
            drivers.append(driver)

    _populate_ranges(drivers)
    _populate_standings(drivers)
    race(500, drivers)


def _populate_ranges(drivers):
    placement_range = 0
    for driver in drivers:
        team = Team.query.filter_by(id=driver.team[0].team_id).first()

        dict_to_add = {
            driver.name: {
                "starting_range": placement_range,
                "ending_range": 0
            }
        }

        placement_range = placement_range + _calculate_range(driver, team)
        dict_to_add[driver.name]['ending_range'] = placement_range
        rate_ranges.update(dict_to_add)
        placement_range = placement_range + 1

    global ending_range
    ending_range = placement_range


def _repopulate_ranges(drivers):
    placement_range = 0
    for driver in drivers:
        team = Team.query.filter_by(id=driver.team[0].team_id).first()

        rate_ranges[driver.name]['starting_range'] = floor(placement_range)

        placement_range = placement_range + _calculate_range(driver, team, standings[driver.name]['laps_led'])

        position_bonus = position_bonuses[standings[driver.name]['position']]

        bonus_range = floor((placement_range * position_bonus) + placement_range)

        if rate_ranges[driver.name]['ending_range'] <= bonus_range:
            rate_ranges[driver.name]['ending_range'] = bonus_range
        else:
            rate_ranges[driver.name]['ending_range'] = floor((rate_ranges[driver.name]['ending_range'] * position_bonus) + rate_ranges[driver.name]['ending_range'])

        placement_range = rate_ranges[driver.name]['ending_range'] + 1
    global ending_range
    ending_range = placement_range


def _calculate_range(driver, team, bonus: int = 0):
    driver_result = pow(float(driver.restricted_track_rating), DRIVER_FACTOR)
    team_result = pow((team.used_equipment_rating + team.personnel_rating) / 2, TEAM_FACTOR)
    bonus_result = bonus * 50
    return round(((driver_result * team_result) + bonus_result) / 100)


def _populate_standings(drivers):
    for driver in drivers:
        standings.update({
            driver.name: {
                "position": None,
                "laps_led": 0,
                "dnf_odds": 0
            }
        })


def race(laps, drivers):
    lap_count = 1

    # Daytona 500 average
    # average = calculate_average_position_change_by_range('2009-2018', 1)
    average = 6
    last_position = len(standings)
    floor_position = last_position - average

    while lap_count <= laps:
        print(f'********** Processing lap {lap_count} **********')
        if lap_count == 1:
            _calculate_lap_1_positions()
        else:
            position_changes = []
            _repopulate_ranges(drivers)
            
            for driver in rate_ranges:
                _calculate_lap_position(last_position, floor_position, average, driver, random.randint(0, ending_range), position_changes)

            for driver in standings:
                if standings[driver]['position'] == 1:
                    standings[driver]['laps_led'] = standings[driver]['laps_led'] + 1
            # futil.write_dict_to_json('standings', standings, 'test_simulation/standings', f'standings_lap_{lap_count}')
            # futil.write_dict_to_json('standings', rate_ranges, 'test_simulation/rate_ranges', f'rate_ranges_lap_{lap_count}')
        lap_count = lap_count + 1

    futil.write_dict_to_json('standings', rate_ranges, 'test_simulation/rate_ranges', 'finish_rate_ranges')
    futil.write_dict_to_json('standings', standings, 'test_simulation/standings', 'finish_standings')


def _calculate_lap_1_positions():
    running_position = 1
    non_range_hits = 0
    random_number = random.randint(0, ending_range)

    for driver in rate_ranges:
        # Any driver that has their rate range hit will get first pickings at the high end of the positions
        # Use the non_range_hits to keep track of how many drivers' don't get their ranges hit
        if rate_ranges[driver]['starting_range'] <= random_number <= rate_ranges[driver]['ending_range']:
            if running_position == 1:
                standings[driver]['laps_led'] = standings[driver]['laps_led'] + 1
                standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .0001
            else:
                standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .0003

            standings[driver]['position'] = running_position
            running_position = running_position + 1
        else:
            standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .0007
            non_range_hits = non_range_hits + 1

    # For any driver that doesn't have their range hit, assign them a random position based on what's left
    iterator = 0
    positions = []
    while iterator < non_range_hits:
        positions.append(running_position)
        running_position = running_position + 1
        iterator = iterator + 1

    for driver in rate_ranges:
        if standings[driver]['position'] is None:
            standings[driver]['position'] = random.choice(positions)
            positions.remove(standings[driver]['position'])
    futil.write_dict_to_json('standings', rate_ranges, 'test_simulation/rate_ranges', 'start_rate_ranges')
    futil.write_dict_to_json('standings', standings, 'test_simulation/standings', 'start_standings')


def _calculate_lap_position(last_position, floor_position, average, driver, random_number, position_changes):
    current_position = standings[driver]['position']
    previous_driver = driver

    if rate_ranges[driver]['starting_range'] <= random_number <= rate_ranges[driver]['ending_range']:
        if current_position <= average:
            random_position = random.randint(1, current_position)
        else:
            random_position = random.randint(current_position - average, current_position)

        if random_position == 1:
            if 1 not in position_changes:
                standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .0001
                position_changes.append(1)
            else:
                standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .0003
                while random_position == 1:
                    if current_position <= average:
                        random_position = random.randint(2, current_position)
                    else:
                        random_position = random.randint(current_position - average, current_position)
        else:
            standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .0007

        previous_position = standings[driver]['position']
        standings[driver]['position'] = random_position

        while random_position != previous_position:
            for next_driver in rate_ranges:
                if next_driver != previous_driver and standings[next_driver]['position'] == random_position:
                    random_position = random_position + 1
                    standings[next_driver]['position'] = random_position
                    previous_driver = next_driver
                    break
    else:
        previous_position = standings[driver]['position']
        lowest_position = current_position + average

        if current_position >= floor_position:
            random_position = random.randint(previous_position, last_position)
        else:
            random_position = random.randint(current_position, lowest_position)

        standings[driver]['position'] = random_position
        standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .0005

        while random_position != previous_position:
            for next_driver in rate_ranges:
                if next_driver != previous_driver and standings[next_driver]['position'] == random_position:
                    random_position = random_position - 1
                    standings[next_driver]['position'] = random_position
                    previous_driver = next_driver
                    break
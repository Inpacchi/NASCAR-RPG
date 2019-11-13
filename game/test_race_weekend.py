import random
from math import floor

from game.race_stats_calculator import calculate_average_position_change_by_range
from models.driver import Driver
from models.team import Team
from utilities import futil

DRIVER_FACTOR = 1.25
TEAM_FACTOR = 1.4
CAUTION_THRESHOLD = 5

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
    _race(200, drivers)


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

        placement_range = placement_range + _calculate_range(driver, team, standings[driver.name]['lap_lead_count'])

        position_bonus = position_bonuses[standings[driver.name]['current_position']]

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
                'start_position': 0,
                'mid_race_position': 0,
                'finish_position': 0,
                'lowest_position': 0,
                'highest_position': 0,
                'average_position': 0,
                'current_position': 0,
                'lap_lead_count': 0,
                'lap_lead_percentage': 0,
                'top_15_lap_count': 0,
                'top_15_lap_percentage': 0,
                'total_lap_count': 1,
                'driver_rating': 0,
                'dnf_odds': 0
            }
        })


def _race(laps, drivers):
    # Daytona 500 Averages
    # average_position_change = calculate_average_position_change_by_range('2009-2018', 1)
    average_position_change = 6
    # average_laps_under_caution =  calculate_average_laps_under_caution_by_range('2009-2018', 1)
    average_laps_under_caution =  4

    current_lap = 1
    last_position = len(standings)
    floor_position = last_position - average_position_change
    mid_race_lap = laps / 2

    while current_lap <= laps:
        print(f'********** Processing lap {current_lap} **********')
        if current_lap == 1:
            _calculate_lap_1_positions()
        else:
            position_changes = []
            _repopulate_ranges(drivers)

            for driver in rate_ranges:
                _calculate_lap_position(last_position, floor_position, average_position_change, driver, random.randint(0, ending_range), position_changes)
            _calculate_post_lap_stats()
            # futil.write_dict_to_json('standings', standings, 'test_simulation/standings', f'standings_lap_{lap_count}')
            # futil.write_dict_to_json('standings', rate_ranges, 'test_simulation/rate_ranges', f'rate_ranges_lap_{lap_count}')

        if current_lap == mid_race_lap:
            for driver in standings:
                standings[driver]['mid_race_position'] = standings[driver]['current_position']
        current_lap = current_lap + 1

    _calculate_post_race_stats()
    # futil.write_dict_to_json('standings', rate_ranges, 'test_simulation/rate_ranges', 'finish_rate_ranges')
    # futil.write_dict_to_json('standings', standings, 'test_simulation/standings', 'finish_standings')


def _calculate_post_lap_stats():
    for driver in standings:
        standings[driver]['average_position'] = standings[driver]['average_position'] + standings[driver]['current_position']
        standings[driver]['total_lap_count'] = standings[driver]['total_lap_count'] + 1

        if standings[driver]['current_position'] <= 15:
            standings[driver]['top_15_lap_count'] = standings[driver]['top_15_lap_count'] + 1

        if standings[driver]['current_position'] == 1:
            standings[driver]['lap_lead_count'] = standings[driver]['lap_lead_count'] + 1
            standings[driver]['highest_position'] = 1
        else:
            if standings[driver]['current_position'] > standings[driver]['lowest_position']:
                standings[driver]['lowest_position'] = standings[driver]['current_position']
            elif standings[driver]['current_position'] < standings[driver]['highest_position']:
                standings[driver]['highest_position'] = standings[driver]['current_position']


def _calculate_post_race_stats():
    for driver in standings:
        standings[driver]['finish_position'] = standings[driver]['current_position']
        standings[driver]['lap_lead_percentage'] = (standings[driver]['lap_lead_count'] / standings[driver]['total_lap_count']) * 100
        standings[driver]['top_15_lap_percentage'] = (standings[driver]['top_15_lap_count'] / standings[driver]['total_lap_count']) * 100
        standings[driver]['average_position'] = round(standings[driver]['average_position'] / standings[driver]['total_lap_count'])
        # TODO: Driver Rating


def _calculate_lap_1_positions():
    running_position = 1
    non_range_hits = 0

    for driver in rate_ranges:
        random_number = random.randint(0, ending_range)
        # Any driver that has their rate range hit will get first pickings at the high end of the positions
        # Use the non_range_hits to keep track of how many drivers' don't get their ranges hit
        if rate_ranges[driver]['starting_range'] <= random_number <= rate_ranges[driver]['ending_range']:
            if running_position == 1:
                standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .0001
            else:
                standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .003

            standings[driver]['current_position'] = running_position
            running_position = running_position + 1
        else:
            standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .01
            non_range_hits = non_range_hits + 1

    # For any driver that doesn't have their range hit, assign them a random position based on what's left
    iterator = 0
    positions = []
    while iterator < non_range_hits:
        positions.append(running_position)
        running_position = running_position + 1
        iterator = iterator + 1

    for driver in rate_ranges:
        if standings[driver]['current_position'] == 0:
            standings[driver]['current_position'] = random.choice(positions)
            positions.remove(standings[driver]['current_position'])

        standings[driver]['start_position'] = standings[driver]['current_position']
        standings[driver]['lowest_position'] = standings[driver]['current_position']
        standings[driver]['highest_position'] = standings[driver]['current_position']

    # futil.write_dict_to_json('standings', rate_ranges, 'test_simulation/rate_ranges', 'start_rate_ranges')
    # futil.write_dict_to_json('standings', standings, 'test_simulation/standings', 'start_standings')


def _calculate_lap_position(last_position, floor_position, average_position_change, driver, random_number, position_changes):
    current_position = standings[driver]['current_position']
    previous_driver = driver

    if rate_ranges[driver]['starting_range'] <= random_number <= rate_ranges[driver]['ending_range']:
        if current_position <= average_position_change:
            random_position = random.randint(1, current_position)
        else:
            random_position = random.randint(current_position - average_position_change, current_position)

        if random_position == 1:
            if 1 not in position_changes:
                standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .0001
                position_changes.append(1)
            else:
                standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .0005
                while random_position == 1:
                    if current_position <= average_position_change:
                        random_position = random.randint(2, current_position)
                    else:
                        random_position = random.randint(current_position - average_position_change, current_position)
        else:
            standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .003

        previous_position = standings[driver]['current_position']
        standings[driver]['current_position'] = random_position

        while random_position != previous_position:
            for next_driver in rate_ranges:
                if next_driver != previous_driver and standings[next_driver]['current_position'] == random_position:
                    random_position = random_position + 1
                    standings[next_driver]['current_position'] = random_position
                    previous_driver = next_driver
                    break
    else:
        previous_position = standings[driver]['current_position']
        lowest_position = current_position + average_position_change

        if current_position >= floor_position:
            random_position = random.randint(previous_position, last_position)
        else:
            random_position = random.randint(current_position, lowest_position)

        standings[driver]['current_position'] = random_position
        standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .01

        while random_position != previous_position:
            for next_driver in rate_ranges:
                if next_driver != previous_driver and standings[next_driver]['current_position'] == random_position:
                    random_position = random_position - 1
                    standings[next_driver]['current_position'] = random_position
                    previous_driver = next_driver
                    break


def _caution(average_laps_under_caution, lap_count):
    pass
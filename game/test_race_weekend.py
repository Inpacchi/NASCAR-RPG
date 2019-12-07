import math
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


def _repopulate_ranges(drivers, current_lap = None):
    placement_range = 0
    for driver in drivers:
        if standings[driver.name]['status'] == 'running':
            team = Team.query.filter_by(id=driver.team[0].team_id).first()

            rate_ranges[driver.name]['starting_range'] = floor(placement_range)

            if current_lap is not None and standings[driver.name]['total_lap_count'] < current_lap:
                lap_difference = current_lap - standings[driver.name]['total_lap_count']
                penalty = lap_difference * -100
                placement_range = placement_range + _calculate_range(driver, team, penalty)
            else:
                if standings[driver.name]['lap_lead_count'] != 0:
                    placement_range = placement_range + \
                                      _calculate_range(driver, team, standings[driver.name]['lap_lead_count'])
                elif standings[driver.name]['top_15_lap_count'] != 0:
                    placement_range = placement_range + \
                                      _calculate_range(driver, team, standings[driver.name]['top_15_lap_count'])
                else:
                    placement_range = placement_range + _calculate_range(driver, team)

            position_bonus = position_bonuses[standings[driver.name]['current_position']]

            bonus_range = floor((placement_range * position_bonus) + placement_range)

            if rate_ranges[driver.name]['ending_range'] <= bonus_range:
                rate_ranges[driver.name]['ending_range'] = bonus_range
            else:
                rate_ranges[driver.name]['ending_range'] = floor(
                    (rate_ranges[driver.name]['ending_range'] * position_bonus)
                    + rate_ranges[driver.name]['ending_range'])

            placement_range = rate_ranges[driver.name]['ending_range'] + 1
        else:
            try:
                del rate_ranges[driver.name]
            except KeyError:
                pass
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
                'mid_race_position': None,
                'finish_position': 0,
                'lowest_position': 0,
                'highest_position': 0,
                'average_position': 0,
                'current_position': 0,
                'stage_1_position': 0,
                'stage_2_position': 0,
                'position_when_wrecked': None,
                'lap_lead_count': 0,
                'lap_lead_percentage': 0,
                'top_15_lap_count': 0,
                'top_15_lap_percentage': 0,
                'total_lap_count': 0,
                'driver_rating': 0,
                'cautions_caused': 0,
                'status': 'running',
                'dnf_odds': 0
            }
        })
        standings[driver.name]['dnf_odds'] = random.uniform(0, .09) * math.pow((driver.restricted_track_rating / 100),
                                                                               2)


def _race(laps, drivers):
    # Daytona 500 Averages
    # average_position_change = calculate_average_position_change_by_range('2009-2018', 1)
    average_position_change = 6
    # average_laps_under_caution =  calculate_average_laps_under_caution_by_range('2009-2018', 1)
    average_laps_under_caution = 4

    current_lap = 1
    mid_race_lap = laps / 2

    while current_lap <= laps:
        last_position = _determine_last_position()
        floor_position = last_position - average_position_change
        print(f'********** Processing lap {current_lap} **********')
        if current_lap == 1:
            _calculate_lap_1_positions()
            _calculate_post_lap_stats()
        else:
            position_changes = []
            drivers_not_on_lead_lap = []
            _repopulate_ranges(drivers, current_lap)

            for driver in rate_ranges:
                if standings[driver]['status'] == 'running':
                    if standings[driver]['total_lap_count'] == current_lap - 1:
                        _calculate_lead_lap_position(last_position, floor_position, average_position_change, driver,
                                                     position_changes)
                    else:
                        x = standings[driver]['total_lap_count']
                        print(f'{driver} is not on the lead lap - they are on lap {x}')
                        drivers_not_on_lead_lap.append(driver)

            if drivers_not_on_lead_lap:
                if len(drivers_not_on_lead_lap) > 1:
                    _process_non_lead_lap_drivers(drivers_not_on_lead_lap)
                else:
                    standings[drivers_not_on_lead_lap[0]]['dnf_odds'] = \
                        standings[drivers_not_on_lead_lap[0]]['dnf_odds'] + random.uniform(.001, .002)

            _calculate_post_lap_stats()

            for driver in standings:
                if standings[driver]['status'] == 'running' and standings[driver]['dnf_odds'] > .1:
                    current_lap = _determine_if_caution_flag_waved(driver, drivers, current_lap)
            # futil.write_dict_to_json('standings', standings, 'test_simulation/standings', f'standings_lap_{current_lap}')
            # futil.write_dict_to_json('standings', rate_ranges, 'test_simulation/rate_ranges', f'rate_ranges_lap_{lap_count}')

        if current_lap == mid_race_lap:
            for driver in standings:
                if standings[driver]['status'] == 'running':
                    standings[driver]['mid_race_position'] = standings[driver]['current_position']

        if current_lap == 60:
            for driver in standings:
                if standings[driver]['status'] == 'running':
                    standings[driver]['stage_1_position'] = standings[driver]['current_position']
                    _repopulate_ranges(drivers)

        if current_lap == 120:
            for driver in standings:
                if standings[driver]['status'] == 'running':
                    standings[driver]['stage_2_position'] = standings[driver]['current_position']
                    _repopulate_ranges(drivers)
        current_lap = current_lap + 1

    _post_race_processing()
    futil.write_dict_to_json('standings', standings, 'test_simulation/standings', 'post_post_race_processing')


def _calculate_post_lap_stats():
    for driver in standings:
        if standings[driver]['status'] == 'running':
            standings[driver]['average_position'] = standings[driver]['average_position'] + standings[driver][
                'current_position']
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


def _post_race_processing():
    for driver in standings:
        if standings[driver]['status'] == 'running':
            standings[driver]['finish_position'] = standings[driver]['current_position']
        standings[driver]['current_position'] = None
        standings[driver]['dnf_odds'] = None
        standings[driver]['lap_lead_percentage'] = \
            round(standings[driver]['lap_lead_count'] / standings[driver]['total_lap_count'], 4) * 100
        standings[driver]['top_15_lap_percentage'] = \
            round(standings[driver]['top_15_lap_count'] / standings[driver]['total_lap_count'], 4) * 100
        standings[driver]['average_position'] = \
            round(standings[driver]['average_position'] / standings[driver]['total_lap_count'])
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
                standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + random.uniform(0, .001)
            else:
                standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + random.uniform(0, .002)

            standings[driver]['current_position'] = running_position
            running_position = running_position + 1
        else:
            standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + random.uniform(.002, .003)
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


def _calculate_lead_lap_position(last_position, floor_position, average_position_change, driver, position_changes):
    random_number = random.randint(0, ending_range)
    current_position = standings[driver]['current_position']

    if rate_ranges[driver]['starting_range'] <= random_number <= rate_ranges[driver]['ending_range']:
        if current_position <= average_position_change:
            random_position = random.randint(1, current_position)
        else:
            random_position = random.randint(current_position - average_position_change, current_position)

        if random_position == 1:
            if 1 not in position_changes:
                standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + random.uniform(0, .001)
                position_changes.append(1)
            else:
                standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + random.uniform(0, .0015)
                while random_position == 1:
                    if current_position <= average_position_change:
                        random_position = random.randint(2, current_position)
                    else:
                        random_position = random.randint(current_position - average_position_change, current_position)
        else:
            standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + random.uniform(0, .002)

        previous_position = standings[driver]['current_position']
        standings[driver]['current_position'] = random_position

        _shift_drivers(driver, previous_position, random_position, 'up')
    else:
        previous_position = standings[driver]['current_position']
        standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + random.uniform(.002, .003)

        if current_position >= floor_position:
            random_position = random.randint(previous_position, last_position)
        else:
            random_position = random.randint(current_position, current_position + average_position_change)

        standings[driver]['current_position'] = random_position
        _shift_drivers(driver, previous_position, random_position, 'down')


def _process_non_lead_lap_drivers(drivers_not_on_lead_lap):
    drivers_positions = []

    for driver in drivers_not_on_lead_lap:
        drivers_positions.append(standings[driver]['total_lap_count'])

    drivers_to_process = {}

    for driver, laps in zip(drivers_not_on_lead_lap, drivers_positions):
        if laps not in drivers_to_process.keys():
            drivers_to_process[laps] = []
        drivers_to_process[laps].append(driver)

    for laps in drivers_to_process:
        if len(drivers_to_process[laps]) == 1:
            standings[drivers_to_process[laps][0]]['dnf_odds'] = \
                standings[drivers_to_process[laps][0]]['dnf_odds'] + random.uniform(.001, .002)
            return
        elif len(drivers_to_process[laps]) == 2:
            _determine_swap(drivers_to_process[laps])
            return

        ceiling_and_floor_positions = _calculate_ceiling_and_floor_positions(drivers_to_process[laps])
        for driver in drivers_to_process[laps]:
            _calculate_non_lead_lap_position(driver, ceiling_and_floor_positions)


def _calculate_non_lead_lap_position(driver, ceiling_and_floor_positions):
    ceiling_position = ceiling_and_floor_positions[0]
    floor_position = ceiling_and_floor_positions[1]
    current_position = standings[driver]['current_position']
    random_number = random.randint(0, ending_range)
    print(f'Ceiling: {ceiling_position}\nFloor: {floor_position}')
    if rate_ranges[driver]['starting_range'] <= random_number <= rate_ranges[driver]['ending_range']:
        random_position = random.randint(ceiling_position, standings[driver]['current_position'])
        standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + random.uniform(.001, .002)
        switch = 'up'
    else:
        random_position = random.randint(standings[driver]['current_position'], floor_position)
        standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + random.uniform(.002, .003)
        switch = 'down'

    if ceiling_position == current_position or random_position == current_position:
        return

    previous_position = standings[driver]['current_position']
    standings[driver]['current_position'] = random_position

    _shift_drivers(driver, previous_position, random_position, switch)


def _determine_swap(drivers):
    for driver in drivers:
        random_number = random.randint(0, ending_range)

        if rate_ranges[driver]['starting_range'] <= random_number <= rate_ranges[driver]['ending_range']:
            standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + random.uniform(.0015, .0025)
            temp_position = standings[driver]['current_position']
            standings[driver]['current_position'] = standings[drivers[1]]['current_position']
            standings[drivers[1]]['current_position'] = temp_position
        else:
            standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + random.uniform(.002, .003)


def _calculate_ceiling_and_floor_positions(drivers):
    if len(drivers) == 1:
        return standings[drivers[0]]['current_position']

    ceiling_position = 1
    floor_position = 34

    for driver in drivers:
        if standings[driver]['current_position'] > ceiling_position:
            ceiling_position = standings[driver]['current_position']

        if standings[driver]['current_position'] < floor_position:
            floor_position = standings[driver]['current_position']

    return [ceiling_position, floor_position]


def _determine_if_caution_flag_waved(driver_name, drivers, current_lap):
    if random.uniform(0, 1) < .05:
        standings[driver_name]['cautions_caused'] = standings[driver_name]['cautions_caused'] + 1
        print('\n - - - - - - - - Caution Flag - - - - - - - - ')

        if random.uniform(0, 1) < .5:
            x = standings[driver_name]['current_position']
            print(f'{driver_name} caused a wreck in position #{x} and has crashed')
            _driver_did_not_finish(driver_name)
        else:
            print(f'{driver_name} caused a wreck')
        _lucky_dog(driver_name, current_lap)
        _caution_flag_out(driver_name)

        end_caution_lap = current_lap + random.randint(1, 4)
        while current_lap < end_caution_lap:
            current_lap += 1
            print(f'\n * - * - * - * - CAUTION LAP {current_lap} - * - * - * - * ')
            _calculate_post_lap_stats()

        for driver in drivers:
            if standings[driver.name]['status'] == 'running':
                standings[driver.name]['dnf_odds'] = \
                    random.uniform(0, .09) * math.pow((driver.restricted_track_rating / 100), 2)
    else:
        for driver in drivers:
            if standings[driver.name]['status'] == 'running' and driver.name == driver_name:
                standings[driver.name]['dnf_odds'] = \
                    random.uniform(0, .09) * math.pow((driver.restricted_track_rating / 100), 2)
                break
    return current_lap


def _caution_flag_out(caution_driver):
    drivers_involved_chances = random.uniform(0, 1)
    if drivers_involved_chances < .05:
        drivers_involved_in_crash = random.randint(13, 22)
    elif drivers_involved_chances < .1:
        drivers_involved_in_crash = random.randint(9, 12)
    elif drivers_involved_chances < .25:
        drivers_involved_in_crash = random.randint(5, 8)
    else:
        drivers_involved_in_crash = random.randint(1, 4)

    caution_driver_position = standings[caution_driver]['current_position']
    if caution_driver_position > 4:
        caution_impact_range = [caution_driver_position - 4, caution_driver_position + drivers_involved_in_crash]
    else:
        caution_impact_range = [1, caution_driver_position + drivers_involved_in_crash]

    for driver in standings:
        if drivers_involved_in_crash > 0 and standings[driver]['status'] == 'running' and driver != caution_driver \
                and caution_impact_range[0] <= standings[driver]['current_position'] <= caution_impact_range[1]:
            wreck_chances = random.uniform(0, 1)
            if wreck_chances < .5:
                x = standings[driver]['current_position']
                print(f'{driver} in position #{x} was involved in the wreck and has crashed')
                drivers_involved_in_crash -= 1
                _driver_did_not_finish(driver)
            elif wreck_chances < .9:
                x = standings[driver]['current_position']
                print(f'{driver} in position #{x} was involved in the wreck')
                drivers_involved_in_crash -= 1
                standings[driver]['dnf_odds'] = .01
                _drop_laps(driver)


def _lucky_dog(driver_name, current_lap):
    last_position = 1
    last_driver = None
    for driver in standings:
        if driver != driver_name and standings[driver]['status'] == 'running' \
                and standings[driver]['total_lap_count'] < current_lap \
                and standings[driver]['current_position'] > last_position:
            last_position = standings[driver]['current_position']
            last_driver = driver
    if last_driver is None:
        return
    standings[last_driver]['total_lap_count'] = standings[last_driver]['total_lap_count'] + 1


def _driver_did_not_finish(driver_dnf):
    standings[driver_dnf]['finish_position'] = len(standings)
    standings[driver_dnf]['lowest_position'] = standings[driver_dnf]['finish_position']
    standings[driver_dnf]['position_when_wrecked'] = standings[driver_dnf]['current_position']
    standings[driver_dnf]['current_position'] = standings[driver_dnf]['finish_position']
    standings[driver_dnf]['dnf_odds'] = None
    standings[driver_dnf]['status'] = 'crash'
    _shift_drivers(
        driver_dnf, standings[driver_dnf]['position_when_wrecked'], standings[driver_dnf]['finish_position'], 'down')


def _shift_drivers(previous_driver, old_position, new_position, direction):
    while new_position != old_position:
        for next_driver in standings:
            if previous_driver != next_driver and standings[next_driver]['current_position'] == new_position:
                if direction == 'up':
                    new_position += 1
                elif direction == 'down':
                    new_position -= 1
                else:
                    raise Exception('No direction was specified')
                standings[next_driver]['current_position'] = new_position
                previous_driver = next_driver
                if standings[next_driver]['status'] == 'crash':
                    standings[next_driver]['finish_position'] = new_position
                break


def _determine_last_position():
    last_position = len(standings)
    for driver in standings:
        if standings[driver]['status'] == 'crash':
            last_position -= 1
    return last_position


def _drop_laps(driver):
    random_number = random.uniform(0, 1)

    if random_number < .7:
        laps_to_lose = 1
    elif random_number < .6:
        laps_to_lose = 2
    elif random_number < .5:
        laps_to_lose = 3
    elif random_number < .4:
        laps_to_lose = 4
    elif random_number < .3:
        laps_to_lose = 5
    elif random_number < .2:
        laps_to_lose = 6
    elif random_number < .1:
        laps_to_lose = 7
    else:
        laps_to_lose = 0

    standings[driver]['total_lap_count'] = standings[driver]['total_lap_count'] - laps_to_lose
    x = standings[driver]['total_lap_count']
    print(f'{driver} has dropped {laps_to_lose} laps and is now on lap {x}')

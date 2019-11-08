import random

from models.driver import Driver
from models.team import Team
from utilities import futil

DRIVER_FACTOR = 1.25
TEAM_FACTOR = 1.4

standings = {}
rate_ranges = {}
ending_range = None


def process_stage():
    drivers_db = Driver.query.all()
    drivers = []
    for driver in drivers_db:
        if len(driver.team) == 1:
            drivers.append(driver)
    _populate_ranges(drivers)
    _populate_standings(drivers)
    race(75)


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

        placement_range += _calculate_range(driver, team)
        dict_to_add[driver.name]['ending_range'] = placement_range
        rate_ranges.update(dict_to_add)
        placement_range += 1

    global ending_range
    ending_range = placement_range


def _calculate_range(driver, team, startingBonus: int = 0):
    driver_result = pow(float(driver.restricted_track_rating), DRIVER_FACTOR)
    team_result = pow((team.used_equipment_rating + team.personnel_rating) / 2, TEAM_FACTOR)
    bonus_result = startingBonus * 50
    return round(((driver_result * team_result) + bonus_result) / 100)


def _populate_standings(drivers):
    for driver in drivers:
        dict_to_add = {
            driver.name: {
                "position": None,
                "laps_led": 0,
                "dnf_odds": 0
            }
        }

        standings.update(dict_to_add)


def race(laps):
    running_position = 1
    non_range_hits = 0

    lap_count = 1
    while lap_count <= laps:
        random_number = random.randint(0, ending_range)

        if lap_count == 1:
            for driver in rate_ranges:
                if rate_ranges[driver]['starting_range'] <= random_number <= rate_ranges[driver]['ending_range']:
                    standings[driver]['position'] = running_position
                    standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .0001
                    running_position = running_position + 1
                    if running_position == 1:
                        standings[driver]['laps_led'] = standings[driver]['laps_led'] + 1
                else:
                    standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .0005
                    non_range_hits = non_range_hits + 1
            iterator = 0
            positions = []
            while iterator < non_range_hits:
                positions.append(running_position)
                running_position = running_position + 1
                iterator = iterator + 1
            for driver in rate_ranges:
                if standings[driver]['position'] is None:
                    position = random.choice(positions)
                    standings[driver]['position'] = position
                    positions.remove(position)
            running_position = 1
            futil.write_dict_to_json('standings', standings, 'standings_lap_1')
        else:
            for driver in rate_ranges:
                if rate_ranges[driver]['starting_range'] <= random_number <= rate_ranges[driver]['ending_range']:
                    standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .0001
                    if running_position == 1:
                        standings[driver]['laps_led'] = standings[driver]['laps_led'] + 1
                    previous_position = standings[driver]['position']
                    standings[driver]['position'] = running_position
                    if running_position < previous_position:
                        previous_driver = driver
                        while running_position != previous_position:
                            for driver_2 in rate_ranges:
                                if driver_2 != previous_driver and standings[driver_2]['position'] == running_position:
                                    running_position = running_position + 1
                                    standings[driver_2]['position'] = running_position
                                    previous_driver = driver_2
                                    break
                    elif running_position > previous_position:
                        previous_driver = driver
                        while running_position != previous_position:
                            for driver_2 in rate_ranges:
                                if driver_2 != previous_driver and standings[driver_2]['position'] == running_position:
                                    running_position -= 1
                                    standings[driver_2]['position'] = running_position
                                    previous_driver = driver_2
                                    break
                else:
                    standings[driver]['dnf_odds'] = standings[driver]['dnf_odds'] + .0005
            running_position = 1
            futil.write_dict_to_json('standings', standings, f'standings_lap_{lap_count}')
        lap_count = lap_count + 1
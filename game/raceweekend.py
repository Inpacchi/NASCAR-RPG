from random import randint

from game import potential
from models.game_app import Schedule, Track
from models.driver import Driver
from models.team import Team
from utilities import dbutil
from webapp import db

DRIVER_FACTOR = 1.25
TEAM_FACTOR = 1.4

rate_ranges = {}
standings = {}
ending_range = 0


def process_stage(race_id: int = None, race_name: str = None, track_name: str = None) -> None:
    """
    Main entry method for raceweekend.py

    Package available method that handles all function calls and logic processing for the race package.

    :return: None
    :rtype: None
    """

    race = None

    if race_id is not None:
        race = Schedule.query.filter_by(id=race_id).first()
        track = Track.query.filter_by(id=race.track_id).first()
    elif race_name is not None:
        race = Schedule.query.filter(Schedule.name.like(f'%{race_name}%')).first()
        track = Track.query.filter(id=race.track_id).first()
    elif track_name is not None:
        track = Track.query.filter(Track.name.like(f'%{track_name}%')).first()
    else:
        raise Exception('Either race_id, race_name or track_name must be specified!')

    drivers = Driver.query.all()

    _populate_ranges(drivers, track)
    _populate_standings(drivers)
    _qualifying(race, track)
    _race()
    dbutil.add_standings_to_session(standings, track)
    if race_id is not None or race_name is not None:
        race.race_processed = True
    dbutil.commit()
    # potential.process_stage(standings, drivers)


def _populate_ranges(drivers, track) -> None:
    """
    Populates the rate_rangesDict with rate ranges to be used for race stage processing.

    :return: None
    :rtype: None
    """

    placement_range = 0
    for driver in drivers:
        dict_to_add = {
            driver.name: {
                "starting_range": placement_range,
                "ending_range": 0
            }
        }

        if len(driver.team) == 0:
            team = None
        elif len(driver.team) == 1:
            team = Team.query.filter_by(id=driver.team[0].team_id).first()
        else:
            # TODO: Add series column to schedule table to determine team if driver is associated with more than 1
            team = None

        placement_range += _calculate_range(track, driver, team)
        dict_to_add[driver.name]['ending_range'] = placement_range
        rate_ranges.update(dict_to_add)
        placement_range += 1

    global ending_range
    ending_range = placement_range


def _calculate_range(track, driver: Driver, team: Team, startingBonus: int = 0) -> float:
    """
    Returns a range for each driver dependent upon their overall rating as well as their team rating and any bonuses.

    :param driver: Driver model object
    :type driver: Driver
    :param team: Team model object
    :type team: Team
    :param startingBonus: Any bonus to be added to the formula
    :type startingBonus: integer
    :return: Range to determine standings
    :rtype: float
    """

    if track.type == 'short':
        driver_result = pow(float(driver.short_rating), DRIVER_FACTOR)
    elif track.type == 'short-intermediate':
        driver_result = pow(float(driver.short_intermediate_rating), DRIVER_FACTOR)
    elif track.type == 'intermediate':
        driver_result = pow(float(driver.intermediate_rating), DRIVER_FACTOR)
    elif track.type == 'superspeedway':
        driver_result = pow(float(driver.super_speedway_rating), DRIVER_FACTOR)
    elif track.type == 'restricted':
        driver_result = pow(float(driver.restricted_track_rating), DRIVER_FACTOR)
    elif track.type == 'road':
        driver_result = pow(float(driver.road_course_rating), DRIVER_FACTOR)
    else:
        raise Exception('Track type not defined')

    if team is not None:
        team_result = pow((team.used_equipment_rating + team.personnel_rating) / 2, TEAM_FACTOR)
    else:
        team_result = pow(50, TEAM_FACTOR)

    bonus_result = startingBonus * 50

    return round(((driver_result * team_result) + bonus_result) / 100)


def _populate_standings(drivers) -> None:
    """
    Populates the standings with the standard standings that will be generated during race stage processing.

    :return: None
    :rtype: None
    """

    for driver in drivers:
        dict_to_add = {
            driver.name: {
                "race_id": None,
                "track_id": None,
                "qualifying_position": None,
                "finishing_position": None,
                "laps_led": None,
                "times_qualifying_range_hit": None,
                "times_race_range_hit": None,
                "fastest_qualifying_lap": None
            }
        }

        standings.update(dict_to_add)


def _qualifying(race=None, track=None) -> None:
    """
    Processes the qualifying stage of the race and writes the results to the standings.

    :return: None
    :rtype: None
    """

    qualifying_position = 1

    while qualifying_position != len(standings) + 1:
        random_number = randint(0, ending_range)

        for rate_range in rate_ranges:
            if race is not None and standings[rate_range]['race_id'] is None:
                standings[rate_range]['race_id'] = race.id
            elif track is not None and standings[rate_range]['track_id'] is None:
                standings[rate_range]['track_id'] = track.id

            if rate_ranges[rate_range]['starting_range'] <= random_number <= rate_ranges[rate_range]['ending_range']:
                if standings[rate_range]['qualifying_position'] is None:
                    standings[rate_range]['qualifying_position'] = qualifying_position
                    standings[rate_range]['times_qualifying_range_hit'] = 1
                    qualifying_position += 1
                else:
                    standings[rate_range]['times_qualifying_range_hit'] += 1


def _race() -> None:
    """
    Processes the actual race portion and writes the results to the standings.

    :return: None
    :rtype: None
    """

    finishing_position = 1

    while finishing_position != len(standings) + 1:
        random_number = randint(0, ending_range)

        for rate_range in rate_ranges:
            if rate_ranges[rate_range]['starting_range'] <= random_number <= rate_ranges[rate_range]['ending_range']:
                if standings[rate_range]['finishing_position'] is None:
                    standings[rate_range]['finishing_position'] = finishing_position
                    standings[rate_range]['times_race_range_hit'] = 1
                    finishing_position += 1
                else:
                    standings[rate_range]['times_race_range_hit'] += 1

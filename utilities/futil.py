from typing import Union, TextIO
import os.path
import json
import csv

from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from models.driver import Driver
from models.gameapp import Schedule, Track
from models.team import Team, TeamRentals
from webapp import db

MODEL_TYPE_DICT = {
    'driver_subset': {
        'driver',
        'currentdrivers',
        'testdriver'
    },
    'team_subset': {
        'team',
        'charterteam',
        'testteam'
    },
    'test_subset': {
        'testdriver',
        'testteam'
    },
    'misc_subset': {
        'standings',
        'tracks',
        'schedule',
    },
    'schedules': {
        '2020schedule'
    }
}


def _json_file(model_type: str, file_path: str = None, file_name: str = None) -> TextIO:
    """
    Returns a JSON file based on given parameters.

    If file_path is specified, direct json_path to the the given file_path and file_name (file_name MUST be specified.)

    If file_name is specified, direct json_path to the intended directory with the given file_name.

    Otherwise, take in a model type and attempt to open the relevant JSON file. If the file is not
    found, then it is is created.

    Once the file has been opened or created, it becomes the return value.

    :param model_type: Type of model being loaded
    :type model_type: string
    :param file_path: If specified, path to file to be used for I/O
    :type file_path: string
    :param file_name: If specified, name of file to be used for I/O
    :type file_name: string
    :return: Raw JSON connection string
    :rtype: TextIO
    """

    if file_path is not None and file_name is not None:
        json_path = f'data/{file_path}/{file_name}'
    elif file_name is not None:
        if model_type.lower() in MODEL_TYPE_DICT.get('driver_subset'):
            json_path = f'data/json/drivers/{file_name}.json'
        elif model_type.lower() in MODEL_TYPE_DICT.get('team_subset'):
            json_path = f'data/json/teams/{file_name}.json'
        elif model_type.lower() in MODEL_TYPE_DICT.get('test_subset'):
            json_path = f'../data/json/tests/{file_name}.json'
        else:
            raise Exception(f'\'{model_type}\' is not a valid model type!')
    else:
        if model_type.lower() == 'driver':
            json_path = 'data/json/drivers/drivers.json'
        elif model_type.lower() == 'currentdrivers':
            json_path = 'data/json/drivers/currentdrivers.json'
        elif model_type.lower() == 'team':
            json_path = 'data/json/teams/teams.json'
        elif model_type.lower() == 'charterteam':
            json_path = 'data/json/teams/charterteams.json'
        elif model_type.lower() == 'standings':
            json_path = 'data/json/standings.json'
        elif model_type.lower() == 'tracks':
            json_path = 'data/json/tracks.json'
        elif model_type.lower() == '2020schedule':
            json_path = 'data/json/seasons/2020/schedule.json'
        elif model_type.lower() == 'testdriver':
            json_path = '../data/tests/json/drivers/drivers.json'
        elif model_type.lower() == 'testteam':
            json_path = '../data/tests/json/teams/teams.json'
        else:
            raise Exception(f'\'{model_type}\' is not a valid model type!')

    try:
        json_file = open(json_path, 'r+', encoding='utf-8-sig')
    except IOError:
        json_file = open(json_path, 'w+', encoding='utf-8-sig')

    return json_file


def _csv_file(model_type: str, file_name: str = None, conversion: str = None) -> TextIO:
    """
    Returns a CSV file based on given parameters.

    If conversion is specified as 'y', the intended usage is to store data as a CSV for database operations.
    csv_path is directed towards a conversion directory such as to separate these files from regular data.

    If file_name is specified, direct csv_path to the intended directory with the given file_name.

    Otherwise, take in a model type and attempt to open the relevant CSV file. If the file is not
    found, then it is created.

    Once the file has been opened or created, it becomes the return value.

    :param model_type: Type of model being loaded
    :type model_type: string
    :param file_name: If specified, name of file to be used for I/O
    :type file_name: string
    :param conversion: If specified, use conversion output path
    :type conversion: string
    :return: Raw CSV connection string
    :rtype: TextIO
    """

    if conversion is not None and conversion.lower() == 'y':
        csv_path = f'data/sqlite/conversion/{file_name}.csv'
    elif file_name is not None:
        if model_type.lower() in MODEL_TYPE_DICT.get('driver_subset'):
            csv_path = f'data/csv/drivers/{file_name}.csv'
        elif model_type.lower() in MODEL_TYPE_DICT.get('team_subset'):
            csv_path = f'data/csv/teams/{file_name}.csv'
        elif model_type.lower() in MODEL_TYPE_DICT.get('test_subset'):
            csv_path = f'../data/csv/tests/{file_name}.csv'
        elif model_type.lower() in MODEL_TYPE_DICT.get('misc_subset').union(MODEL_TYPE_DICT.get('schedules')):
            csv_path = f'data/csv/{file_name}.csv'
        else:
            raise Exception('You entered a file_name, but did not enter a valid model type!')
    else:
        if model_type.lower() == 'driver':
            csv_path = 'data/csv/drivers/drivers.csv'
        elif model_type.lower() == 'team':
            csv_path = 'data/csv/teams/teams.csv'
        elif model_type.lower() == 'testdriver':
            csv_path = '../data/tests/csv/drivers/drivers.csv'
        elif model_type.lower() == 'testteam':
            csv_path = '../data/tests/csv/teams/teams.csv'
        elif model_type.lower() in MODEL_TYPE_DICT.get('misc_subset').union(MODEL_TYPE_DICT.get('schedules')):
            csv_path = f'data/csv/{model_type}.csv'
        else:
            raise Exception(f'\'{model_type}\' is not a valid model type!')

    try:
        csv_file = open(csv_path, 'r+', encoding='utf-8-sig')
    except IOError:
        csv_file = open(csv_path, 'w+', encoding='utf-8-sig')

    return csv_file


def _get_csv_header(model_type: str) -> list:
    """
    Returns the relevant model_type CSV Header.

    :param model_type: Type of model being loaded
    :type model_type: string
    :return: list of column names
    :rtype: list
    """

    if model_type.lower() in (MODEL_TYPE_DICT.get('driver_subset').union('testdriver')):
        header = ['name', 'age', 'teamName', 'contractStatus', 'car_number', 'short_rating', 'short_intermediate_rating',
                  'intermediate_rating', 'super_speedway_rating', 'restricted_track_rating', 'road_course_rating',
                  'overall_rating', 'potential']
    elif model_type.lower() in (MODEL_TYPE_DICT.get('team_subset').union('testteam')):
        header = ['name', 'owner', 'car_manufacturer', 'equipment_rating', 'teamRating', 'raceRating', 'drivers']
    elif model_type.lower() == 'standings':
        header = ["qualifying_position", "finishing_position", "laps_led", "times_qualifying_range_hit", "times_race_range_hit",
                  "fastest_qualifying_lap"]
    elif model_type.lower() == 'tracks':
        header = ['name', 'length', 'type']
    elif model_type.lower() in MODEL_TYPE_DICT.get('schedules'):
        header = ['name', 'date', 'type', 'track', 'laps', 'stages', 'race_processed']
    else:
        raise Exception(f'\'{model_type}\' is not a valid model type!')

    return header


def read_dict_from_json(model_type: str, file_name: str = None, file_path: str = None) -> Union[None, dict]:
    """
    Reads a dictionary and either populates Model.Instances (if present) or returns the dictionary.

    If file_path is specified, open the JSON at the given file_path and file_name (file_name MUST be specified.)

    :param model_type: Type of model being loaded
    :type model_type: string
    :param file_path: If specified, path to JSON to be read from
    :type file_path: string
    :param file_name: If specified, name of JSON to be read from
    :type file_name: string
    :return: Dictionary if type is not a model
    :rtype: dictionary
    :return: None if type is a model
    :rtype: None
    """

    json_file = _json_file(model_type, file_path, file_name, None)
    temp_dict = json.load(json_file)
    json_file.close()

    if model_type.lower() in MODEL_TYPE_DICT.get('driver_subset'):
        for model in temp_dict:
            Driver(temp_dict[model])
        return
    elif model_type.lower() in MODEL_TYPE_DICT.get('team_subset'):
        if Driver.instances == {}:
            read_dict_from_json(model_type)

        for model in temp_dict:
            driversDict = temp_dict[model]['drivers']
            temp_dict[model]['drivers'] = []

            for name in driversDict:
                temp_dict[model]['drivers'].append(Driver.instances[name])

            Team(temp_dict[model])
        return
    elif model_type.lower() in (MODEL_TYPE_DICT.get('misc_subset').union(MODEL_TYPE_DICT.get('schedules'))):
        return temp_dict


def write_dict_to_json(model_type: str, models: dict = None, file_name: str = None) -> None:
    """
    Writes the model dictionary to the relevant model type JSON file.

    Otherwise, take in a model type and model dictionary and attempt to write the models or
    dictionary to a JSON file.

    :param model_type: Type of model being written to
    :type model_type: string
    :param models: If specified, dictionary of data or models to be written to the JSON file
    :type models: dict
    :param file_name: If specified, name of file to be written to
    :type file_name: string
    :return: None
    :rtype: None
    """

    if models is None:
        if model_type.lower() in MODEL_TYPE_DICT.get('driver_subset'):
            models = Driver.query.all()
        elif model_type.lower() in MODEL_TYPE_DICT.get('team_subset'):
            models = Team.query.all()
        else:
            raise Exception("No data dictionary was passed in and one could not be loaded. Please try again.")

    json_file = _json_file(model_type, None, file_name)

    # Clear the file
    json_file.seek(0)
    json_file.truncate(0)

    if model_type.lower() in MODEL_TYPE_DICT.get('driver_subset').union(MODEL_TYPE_DICT.get('team_subset')):
        temp_dict = {}
        for name in models:
            temp_dict[name] = models[name].serialize()

            if model_type.lower() in MODEL_TYPE_DICT.get('team_subset'):
                temp_dict[name]['drivers'] = []
                for driver in models[name].drivers:
                    temp_dict[name]['drivers'].append(driver.name)

        json.dump(temp_dict, json_file, indent=4)
    elif model_type.lower() in MODEL_TYPE_DICT.get('misc_subset').union(MODEL_TYPE_DICT.get('schedules')):
        json.dump(models, json_file, indent=4)

    json_file.close()
    print(f'\nJSON file for model type "{model_type}" created at {json_file.name}')


def convert_csv_to_json(model_type: str, file_name: str = None) -> None:
    """
    Import lines from a CSV file as models and convert to dictionary format.

    :param model_type: Type of model being loaded
    :type model_type: string
    :param file_name: If specified, the specific path to write the CSV file to
    :type file_name: string
    :return: None
    :rtype: None
    """

    csv_file = _csv_file(model_type, file_name)
    reader = csv.DictReader(csv_file)

    if model_type in MODEL_TYPE_DICT.get('driver_subset'):
        for row in reader:
            Driver(row)
        write_dict_to_json(model_type, Driver.instances, file_name)
    elif model_type in MODEL_TYPE_DICT.get('team_subset'):
        for row in reader:
            Team(row)
        write_dict_to_json(model_type, Team.instances, file_name)

    csv_file.close()
    print(f'CSV file for model type "{model_type}" converted from {csv_file.name}')


def convert_dict_to_csv(model_type: str, models: dict = None, file_name: str = None, conversion: str = None) -> None:
    """
    Convert regular dictionaries and model dictionaries to a CSV format.

    :param model_type: Type of model being written to
    :type model_type: string
    :param models: If specified, a dictionary of values
    :type models: dict
    :param file_name: If specified, the specific path to write the CSV file to
    :type file_name: string
    :param conversion: If specified, use conversion output path
    :type conversion: string
    :return: None
    :rtype: None
    """

    if models is None and model_type.lower() in MODEL_TYPE_DICT.get('misc_subset').union(
            MODEL_TYPE_DICT.get('schedules')):
        models = read_dict_from_json(model_type)
    elif not Driver.instances and models is None:
        read_dict_from_json(model_type)

    csv_file = _csv_file(model_type, file_name, conversion)

    writer = csv.DictWriter(csv_file, fieldnames=_get_csv_header(model_type))
    writer.writeheader()

    if model_type in MODEL_TYPE_DICT.get('driver_subset'):
        for driver in Driver.instances.values():
            writer.writerow(driver.serialize())
    elif model_type in MODEL_TYPE_DICT.get('team_subset'):
        for team in Team.instances.values():
            writer.writerow(team.serialize())
    else:
        writer.writerows(models.values())

    csv_file.close()
    print(f'\nCSV file created at {csv_file.name}')


def add_csv_to_db(model_type: str, file_name: str = None) -> None:
    """
    Add rows from a CSV to the database.

    If the commit should fail, the intended changes are written to a file so a commit can be tried again.

    TODO: Add if parameters for other data types.

    :param model_type: Type of model being loaded
    :type model_type: string
    :param file_name: If specified, name of file to be used for I/O
    :type file_name: string
    :return: None
    :rtype: None
    """

    if model_type.lower() in MODEL_TYPE_DICT.get('misc_subset').union(MODEL_TYPE_DICT.get('schedules')) \
            and not os.path.exists(f'data/csv/{model_type}.csv'):
        if model_type.lower() in MODEL_TYPE_DICT.get('schedules') \
                and os.path.exists(f'data/json/seasons/{model_type[:4]}/schedule.json'):
            convert_dict_to_csv(model_type)
        elif os.path.exists(f'data/json/{model_type}.json'):
            convert_dict_to_csv(model_type)

    csv_file = _csv_file(model_type, file_name)
    reader = csv.DictReader(csv_file)

    if model_type.lower() in MODEL_TYPE_DICT.get('driver_subset'):
        for row in reader:
            name = row['name']
            if Driver.query.filter(Driver.name.like(f'%{name}%')).scalar() is None:
                driver = Driver(row)
                db.session.flush()
            else:
                driver = Driver.query.filter(Driver.name.like(f'%{name}%')).first()
            driver.add_team(row)
    elif model_type.lower() in MODEL_TYPE_DICT.get('team_subset'):
        rentals = []
        for row in reader:
            name = row['name']
            if Team.query.filter(Team.name.like(f'%{name}%')).scalar() is None:
                team = Team(row)
                db.session.flush()
            else:
                team = Team.query.filter(Team.name.like(f'%{name}%')).first()
            if row['equipment_rented_from'] not in (None, ''):
                rentals.append((row['equipment_rented_from'], row['name']))
            team.populate_cars(row)
        for rental in rentals:
            equipment_lender_id = Team.query.filter(Team.name.like(f'%{rental[0]}%')).first().id
            equipment_lendee = Team.query.filter(Team.name.like(f'%{rental[1]}%')).first()
            if TeamRentals.query.filter_by(from_id=equipment_lender_id, to_id=equipment_lendee.id).scalar() is None:
                equipment_lendee.add_rental(equipment_lender_id)
    elif model_type.lower() in MODEL_TYPE_DICT.get('schedules'):
        for row in reader:
            db.session.add(Schedule(row))
    elif model_type.lower() == 'tracks':
        for row in reader:
            db.session.add(Track(row))

    _try_commit()


def _try_commit():
    try:
        db.session.commit()
    except SQLAlchemyError:
        db.session.rollback()
        raise SQLAlchemyError

from utilities import futil


def print_current_standings():
    standings = futil.read_dict_from_json('standings', 'pre_post_race_processing', 'test_simulation/standings')
    current_position = 1
    current_positions = []

    print('-------- CURRENT STANDINGS --------')
    while current_position != len(standings) + 1:
        for current_driver in standings:
            if standings[current_driver]['current_position'] == current_position:
                print(f'{current_driver} is in position #{current_position}')
                current_position += 1
                break

    for driver in standings:
        current_positions.append(standings[driver]['current_position'])

    print(sorted(current_positions))

def print_finish_standings():
    standings = futil.read_dict_from_json('standings', 'post_post_race_processing', 'test_simulation/standings')
    finish_position = 1
    finish_positions = []

    print('-------- FINISH STANDINGS --------')
    while finish_position != len(standings) + 1:
        for current_driver in standings:
            if standings[current_driver]['finish_position'] == finish_position:
                print(f'{current_driver} is in position #{finish_position}')
                finish_position += 1
                break

    for driver in standings:
        finish_positions.append(standings[driver]['finish_position'])

    print(sorted(finish_positions))
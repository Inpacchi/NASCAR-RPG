# This file is named race_stats_calculator as functionality is present that
# would allow for the manipulation of other stats.

import requests
from bs4 import BeautifulSoup


def calculate_average_position_change_by_event(event_year, event_id):
    return round(_average_position_change_by_event(event_year, event_id), 0)


def _average_position_change_by_event(event_year, event_id):
    if event_id < 10:
        event_id = f'0{event_id}'

    # Loop Data Stats
    race_stats_url_1 = f'https://www.racing-reference.info/loopdata/{event_year}-{event_id}/W'
    race_stats_page_1 = requests.get(race_stats_url_1)

    if race_stats_page_1.status_code != 200:
        raise Exception('Grab was not successful.')

    race_stats_soup_1 = BeautifulSoup(race_stats_page_1.text, 'html.parser')
    stats_table_1 = race_stats_soup_1.find_all(class_='tb')[2]
    stats_table_header_1 = stats_table_1.find_all('th')
    stats_table_header_1_length = len(stats_table_header_1)
    stat_rows_1 = stats_table_1.find_all('tr')
    stats = {}

    for header in stats_table_header_1:
        stats[header.string] = []

    for row in stat_rows_1:
        columns = row.find_all('td')
        if len(columns) != stats_table_header_1_length:
            continue
        for header, column in zip(stats_table_header_1, columns):
            stats[header.string].append(column.string)

    # Race Results
    racenav = race_stats_soup_1.find_all(class_='racenav')
    race_results_page_url = racenav[0].find_all('a')[0].get('href')
    race_stats_url_2 = f'https://www.racing-reference.info{race_results_page_url}'
    race_stats_page_2 = requests.get(race_stats_url_2)

    if race_stats_page_2.status_code != 200:
        raise Exception('Grab was not successful.')

    race_stats_soup_2 = BeautifulSoup(race_stats_page_2.text, 'html.parser')
    stats_table_2 = race_stats_soup_2.find_all(class_='tb')[2]
    stats_table_header_2 = stats_table_2.find_all('th')
    stats_table_header_2_length = len(stats_table_header_2)
    stat_rows_2 = stats_table_2.find_all('tr')
    statuses = []

    for row in stat_rows_2:
        columns = row.find_all('td')
        if len(columns) != stats_table_header_2_length:
            continue
        if int(event_year) > 2015:
            statuses.append(columns[7].string)
        else:
            statuses.append(columns[8].string)

    # Average Calculation
    count = 0
    average = 0
    for start, mid, finish, status in zip(stats['Start'], stats['Mid Race'], stats['Finish'], statuses):
        if str(status) == 'running':
            average_1 = abs(int(start) - int(mid))
            average_2 = abs(int(mid) - int(finish))
            average_3 = abs(average_1 - average_2) / 2
            count += 1
            average += average_3
    return average / count


def calculate_average_position_change_by_range(event_year_range, event_id):
    if type(event_year_range) is not str:
        raise Exception('"event_year_range" must be a string with the years separated by a dash (-)')

    if len(event_year_range) != 9:
        raise Exception('"event_year_range" must have two full years, such as "2015-2019"')

    event_year_range = event_year_range.split('-')
    start_year = int(event_year_range[0])
    end_year = int(event_year_range[1]) + 1

    count = 0
    average = 0
    while start_year != end_year:
        x = _average_position_change_by_event(start_year, event_id)
        average += x
        count += 1
        start_year += 1
    return round(average / count, 0)

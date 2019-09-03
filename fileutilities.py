from models import *
import json
import csv
import os
import progressbar


# TODO: Add interactive file input functionality

def writeDriversListToJSON(driversList):
    driversListJSON = []

    bar = createProgressBar()

    # Try to open the file and if it is not found, then create it
    try:
        driversJSON = open('data/json/drivers.json', 'r+')

        print("drivers.json found. Reading drivers from file...")

        # Read and load the current drivers JSON
        tempDriversDict = json.load(driversJSON)

        bar.start()
        i = 0

        # Store each driver in the driversList as a driver object
        for tempDriver in tempDriversDict:
            driversList.append(driver.Driver(tempDriver))
            bar.update(i + 1)

        bar.finish()
        print()
    except IOError:
        driversJSON = open('data/json/drivers.json', 'w+')
        print("drivers.json not found. File has been created.")

    print("Appending drivers...")
    bar.start()
    i = 0

    # Serialize each driver object as JSON and append it to the JSON list
    for driverObject in driversList:
        driversListJSON.append(json.loads(driverObject.toJSON()))
        bar.update(i+1)

    bar.finish()
    print()

    # Reset JSON current position to 0 (start of file)
    driversJSON.seek(0)

    # Clear the contents of the JSON
    driversJSON.truncate(0)

    # Write the JSON list to the JSON file with pretty print enabled
    json.dump(driversListJSON, driversJSON, indent=4)

    driversJSON.close()

    print("\ndrivers.json has been updated!")


def writeTeamsListToJSON(teamsList):
    teamsListJSON = []

    bar = createProgressBar()

    try:
        teamsJSON = open('data/json/teams.json', 'r+')

        print("teams.json found. Reading teams from file...")

        tempTeamsList = json.load(teamsJSON)

        bar.start()
        i = 0

        for tempTeam in tempTeamsList:
            teamsList.append(team.Team(tempTeam))
            bar.update(i+1)

        bar.finish()
        print()
    except IOError:
        teamsJSON = open('data/json/teams.json', 'w+')
        print("teams.json not found. File has been created.")

    print("Appending teams...")
    bar.start()
    i = 0

    for teamObject in teamsList:
        teamsListJSON.append(json.loads(teamObject.toJSON()))
        bar.update(i+1)

    bar.finish()
    print()

    teamsJSON.seek(0)

    teamsJSON.truncate(0)

    json.dump(teamsListJSON, teamsJSON, indent=4)

    teamsJSON.close()

    print("\nteams.json has been updated!")


def convertDriverCSVtoJSON():
    # Define the standard header column names that should be present in the CSV file
    properHeader = ['Name', 'Age', 'Team Name', 'Contract Status', 'Car Number', 'Short Rating',
                    'Short Intermediate Rating',
                    'Intermediate Rating', 'Superspeedway Rating', 'Restrictor Plate Rating', 'Road Rating',
                    'Overall Rating', 'Potential Retain']

    # Temporary variable to store the actual headers from the CSV file to compare to the proper header
    csvHeader = []

    # Must define encoding='utf-8-sig' to function seamlessly with Excel sheets and exports.
    with open('data/csv/drivers.csv', mode='r', encoding='utf-8-sig') as driversCSV:
        reader = csv.reader(driversCSV)

        # Advance and store the previous line (what will now be the headers)
        header = next(reader)

        for column in header:
            csvHeader.append(column)

    # TODO: Refine error checking and display messages when the headers don't match up.
    headerDiffList = headerDiff(properHeader, csvHeader)

    # Get the differences of the two lists; if they are not ordered correctly or have different column names,
    # don't do anything.
    if headerDiffList:
        print("Seems like the header is messed up. Check the CSV and try again.\n")
        # itemCount = 0
        # for item in headerDiffList:
        # if itemCount == 0 or itemCount % 2 == 0:
        # print("Expected:", headerDiffList[itemCount])
        # print("Got:", headerDiffList[itemCount + 1])
        # itemCount += 1
    else:
        print("The header in both files match! Importing drivers now...")

        with open('data/csv/drivers.csv', mode='r', encoding='utf-8-sig') as driversCSV:
            reader = csv.reader(driversCSV)

            driversList = []

            # Advance the reader past the headers
            next(reader)

            # Initialize progress bar and parameters for displaying
            bar = createProgressBar()
            bar.start()
            i = 0

            for row in reader:
                driversList.append(driver.Driver(row))
                bar.update(i+1)

            bar.finish()
            print()

        writeDriversListToJSON(driversList)

        # TODO: Move file to archive and rename it according to what's already in the folder
        # os.rename('data/csv/drivers.csv', 'data/csv/archive/drivers.csv')


def headerDiff(properHeader, csvHeader):
    return [i for i in properHeader + csvHeader if i not in properHeader or i not in csvHeader]


def createProgressBar():
    return progressbar.ProgressBar(max_value=20, widgets=[progressbar.Bar('=', '[', ']'), ' ', progressbar.Percentage()])
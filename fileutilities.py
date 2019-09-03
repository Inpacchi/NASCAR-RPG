from models import driver
import json
import csv
import os

# TODO: Add interactive file input functionality

def writeDriversListToJSON(driversList):
    driversListJSON = []
    
    # Try to open the file and if it is not found, then create it
    try:
        driversJSON = open('data/json/drivers.json', 'r+')
        
        # Read and load the current drivers JSON
        tempDriversDict = json.load(driversJSON)
        
        # Store each driver in the driversList as a driver object
        for tempDriver in tempDriversDict:
            driversList.append(driver.Driver(tempDriver))
    except IOError:
        driversJSON = open('data/json/drivers.json', 'w+')
    
    # Serialize each driver object as JSON and append it to the JSON list
    for driver in driversList:
        driversListJSON.append(json.loads(driver.toJSON()))
    
    # Reset JSON current position to 0 (start of file)
    driversJSON.seek(0)
    
    # Clear the contents of the JSON
    driversJSON.truncate(0)
    
    # Write the JSON list to the JSON file with pretty print enabled
    json.dump(driversListJSON, driversJSON, indent = 4)
    
    driversJSON.close()
     
# TODO: Copy logic from above method
def writeTeamsListToJSON(teamsList):
    teamsListJSON = []

    for driver in teamsList:
        teamsListJSON.append(json.loads(driver.toJSON()))

    with open('data/json/teamsJSON.json', 'w') as teamsJSON:
        json.dump(teamsListJSON, teamsJSON, indent = 4)
        
def convertFromCSV():
    # Define the standard header column names that should be present in the CSV file
    properHeader = ['Name', 'Age', 'Team Name', 'Contract Status', 'Car Number', 'Short Rating', 'Short Intermediate Rating', 
    'Intermediate Rating', 'Superspeedway Rating', 'Restrictor Plate Rating', 'Road Rating', 'Overall Rating', 'Potential Retain']
    
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
    
    # Get the differences of the two lists; if they are not ordered correctly or have different column names, don't do anything.
    if headerDiffList != []:
        print("Seems like the header is messed up. Check the CSV and try again.\n")
        # itemCount = 0
        # for item in headerDiffList:
            # if itemCount == 0 or itemCount % 2 == 0:
                # print("Expected:", headerDiffList[itemCount])
                # print("Got:", headerDiffList[itemCount + 1])
                # itemCount += 1
    else:
        print("Header files match! Importing files now...")
        
        with open('data/csv/drivers.csv', mode='r', encoding='utf-8-sig') as driversCSV:
            reader = csv.reader(driversCSV)
            
            driversList = []
            
            # Advance the reader past the headers
            next(reader)
            
            for row in reader:
                driversList.append(driver.Driver(row))
            
        writeDriversListToJSON(driversList)
        
        # TODO: Move file to archive and rename it according to what's already in the folder
        # os.rename('data/csv/drivers.csv', 'data/csv/archive/drivers.csv')
        
def headerDiff(properHeader, csvHeader): 
    return [i for i in properHeader + csvHeader if i not in properHeader or i not in csvHeader] 
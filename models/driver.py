import random
import json


class Driver:
    name = ""
    age = 0
    contractStatus = ""

    teamName = ""
    carNumber = 0

    shortRating = 0
    shortIntermediateRating = 0
    intermediateRating = 0
    superSpeedwayRating = 0
    restrictorPlateRating = 0
    roadRating = 0
    overallRating = 0
    potential = ""

    momentum = 0

    # TODO: Implement these two features
    # contractLength = 0
    # salary = 0
    # carManufacturer = ""

    # TODO: Fix driver class variable types
    # TODO: Constructor for new drivers
    # Use an overload to initialize based on the driver type input
    def __init__(self, driver):
        if type(driver) == dict:
            self.name = driver['name']
            self.age = driver['age']
            self.teamName = driver['teamName']
            self.contractStatus = driver['contractStatus']
            self.carNumber = driver['carNumber']
            self.shortRating = driver['shortRating']
            self.shortIntermediateRating = driver['shortIntermediateRating']
            self.intermediateRating = driver['intermediateRating']
            self.superSpeedwayRating = driver['superSpeedwayRating']
            self.restrictorPlateRating = driver['restrictorPlateRating']
            self.roadRating = driver['roadRating']
            self.overallRating = driver['overallRating']
            self.potential = driver['potential']
        else:
            self.name = driver[0]
            self.age = driver[1]
            self.teamName = driver[2]
            self.contractStatus = driver[3]
            self.carNumber = driver[4]
            self.shortRating = driver[5]
            self.shortIntermediateRating = driver[6]
            self.intermediateRating = driver[7]
            self.superSpeedwayRating = driver[8]
            self.restrictorPlateRating = driver[9]
            self.roadRating = driver[10]
            self.overallRating = driver[11]
            self.potential = driver[12]

    def __str__(self):
        return (f"Driver Name: {self.name}\n"
                f"Age: {self.age}\n"
                f"Team Name: {self.teamName}\n"
                f"Contract Status: {self.contractStatus}\n"
                f"Car Number: {self.carNumber}\n"
                f"Short Track Rating: {self.shortRating}\n"
                f"Short-Intermediate Track Rating: {self.shortIntermediateRating}\n"
                f"Intermediate Track Rating: {self.intermediateRating}\n"
                f"Superspeedway Track Rating: {self.superSpeedwayRating}\n"
                f"Road Course Rating: {self.roadRating}\n"
                f"Overall Rating: {self.overallRating}\n"
                f"Potential: {self.potential}\n")

    def toDict(self):
        return self.__dict__

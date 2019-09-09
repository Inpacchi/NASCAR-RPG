import random
import json

# TODO: Fix driver class variable types
# TODO: Constructor for new drivers


class Driver:
    instances = {}

    def __init__(self, driver):
        self.name = driver['name']
        self.age = driver['age']
        self.teamName = driver['teamName']
        self.contractStatus = driver['contractStatus']
        self.carNumber = driver['carNumber']
        self.shortRating = driver['shortRating']
        self.shortIntermediateRating = driver['shortIntermediateRating']
        self.intermediateRating = driver['intermediateRating']
        self.superSpeedwayRating = driver['superSpeedwayRating']
        self.restrictedTrackRating = driver['restrictedTrackRating']
        self.roadCourseRating = driver['roadCourseRating']
        self.overallRating = driver['overallRating']
        self.potential = driver['potential']

        Driver.instances[self.name] = self

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
                f"Road Course Rating: {self.roadCourseRating}\n"
                f"Overall Rating: {self.overallRating}\n"
                f"Potential: {self.potential}\n")

    def toDict(self):
        return self.__dict__

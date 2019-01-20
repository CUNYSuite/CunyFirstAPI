
###***********************************###
'''
CUNYFirstAPI
File: actions_locations.py
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###
import enum 
from .grades import Student_Grades
from .student_center import Student_Center
from .actions_locations import ActionObject, Location
from .transcript import Transcript_Page

class ActionObject:
    def location(self):
        raise NotImplementedError

class Location:
    def __init__(self, session):
        self._session = session

    def move(self):
        raise NotImplementedError

    def request(self):
        raise NotImplementedError

class Locations(enum.Enum):
    student_center = 0
    student_grades = 1
    transcript     = 2

    @staticmethod
    def get_location_object(location):
        if location == Locations.student_center:
            return Student_Center()
        elif location == Locations.student_grades:
            return Student_Grades()
        elif location == Locations.transcript:
            return Transcript_Page()
        else:
            return None

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
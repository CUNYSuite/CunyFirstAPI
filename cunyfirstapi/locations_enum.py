
###***********************************###
'''
CUNYFirstAPI
File: locations_enum.py
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###
import enum 
from .grades import Student_Grades
from .student_center import Student_Center
from .transcript import Transcript_Page

class Locations():
    student_center = 0
    student_grades = 1
    transcript     = 2

    def __init__(self, session, college_code):
        self._college_code = college_code
        self._session = session

    def get_location_object(self, location):
        if location == Locations.student_center:
            return Student_Center(self._session, self._college_code)
        elif location == Locations.student_grades:
            return Student_Grades(self._session, self._college_code)
        elif location == Locations.transcript:
            return Transcript_Page(self._session, self._college_code)
        else:
            return None

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
from cunyfirstapi.grades import Student_Grades
from cunyfirstapi.student_center import Student_Center
from cunyfirstapi.transcript import Transcript_Page
from cunyfirstapi.class_search import Class_Search
from cunyfirstapi.enroll import Enrollment

class Locations():
    student_center = 0
    student_grades = 1
    transcript     = 2
    class_search   = 3
    enrollment     = 4

    def __init__(self, session, college_code):
        self._college_code = college_code
        self._session = session

    def get_location_object(self, location):
        try:

            return {
                Locations.student_center:       Student_Center(self._session, self._college_code),
                Locations.student_grades:       Student_Grades(self._session, self._college_code),
                Locations.transcript:           Transcript_Page(self._session, self._college_code),
                Locations.class_search:         Class_Search(self._session, self._college_code),
                Locations.enrollment:           Enrollment(self._session, self._college_code)
            }[location]

        except KeyError:
            return None
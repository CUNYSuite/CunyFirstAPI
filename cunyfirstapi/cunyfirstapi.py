###***********************************###
'''
CUNYFirstAPI
File: cunyfirstaapi.py
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###
import requests
import re
from os import sys, path
from lxml import html
from bs4 import BeautifulSoup
from lxml import etree
from os.path import join, dirname
from . import login as cuny_login
from . import constants
from .student_center import Student_Center, Student_Center_Action
from .grades import Student_Grades, Student_Grades_Action
from .actions_locations import ActionObject, Location
from .transcript import Transcript_Page, Transcript_Page_Action
from .locations_enum import Locations

class CUNYFirstAPI():

    def __init__(self, username=None, password=None, college_code="QNS01"):
        self._username = username
        self._password = password
        self._session = requests.Session()
        self._college_code = college_code
        self._location_parser = Locations(self._session, self._college_code)

    def restart_session(self):
        self._session = requests.Session()

    def set_password(self, password):
        self._password = password

    def set_username(self, username):
        self._username = username

    def set_college_code(self, college_code):
        self._college_code = college_code

    def get_current_session(self):
        return self._session

    def is_logged_in(self, session=None):
        return cuny_login.is_logged_in(session if session else self._session)
            
    def login(self, username=None, password=None, college_code=None):   
    
        if username:
            self._username = username
        if password:
            self._password = password
        if college_code:
             self._college_code = college_code

        self._session = cuny_login.login(
            self._username, 
            self._password, 
        )
        self._location_parser = Locations(
            self._session, 
            self._college_code
        )

    def move_to(self, loc):
        location = self._location_parser.get_location_object(loc)
        return location.move().action()


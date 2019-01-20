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
from .actions_locations import ActionObject, Location, Locations
from .transcript import Transcript_Page, Transcript_Page_Action

class CUNYFirstAPI():

    def __init__(self, username=None, password=None):
        self._username = username
        self._password = password
        self._session = requests.Session()

    def restart_session(self):
        self._session = requests.Session()

    def set_password(self, password):
        self._password = password

    def set_username(self, username):
        self._username = username

    def get_current_session(self):
        return self._session

    def is_logged_in(self):
        cuny_login.is_logged_in(session)

    def login(self, username=None, password=None):        
        if username:
            self._username = username
        if password:
            self._password = password

        cuny_login.login(
            self._username, 
            self._password, 
            self._session
        )

    def move_to(loc):
        location = Locations.get_location_object(loc)
        return location.move().request()




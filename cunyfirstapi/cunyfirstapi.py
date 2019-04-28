###***********************************###
'''
CUNYFirstAPI
File: cunyfirstapi.py
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
import json
from os.path import join, dirname
from cunyfirstapi import login as cuny_login
from cunyfirstapi.locations_enum import Locations

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

    def logout(self):
        cuny_login.logout(self._session)

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)
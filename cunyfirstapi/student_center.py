###***********************************###
'''
CUNYFirstAPI
File: student_center.py
Author: Ehud Adler
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###
from os import sys, path
from lxml import html
from bs4 import BeautifulSoup
from lxml import etree
from os.path import join, dirname
import requests
import re
from . import constants
from .helper import get_semester

class Student_Center(Location):

    def move(self):
        if data is None:
            request_method = self._session.get
        else:
            request_method = self._session.post

        if headers is None:
            headers = self._session.headers

        response = request_method(
            url=constants.CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL, 
            data=data, 
            headers=headers
        )
        return self.request()

    def request(self)
        return Student_Center_Action()
        

class Student_Center_Action(ActionObject):
    def location(self):
        return Student_Center()

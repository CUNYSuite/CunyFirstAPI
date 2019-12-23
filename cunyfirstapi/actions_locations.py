
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
class ActionObject:
    def location(self):
        raise NotImplementedError

class Location:
    def __init__(self, session, college_code):
        self._session = session
        self._college_code = college_code

    def set_sid(self, icsid):
        self._icsid = icsid

    def move(self):
        raise NotImplementedError

    def action(self):
        raise NotImplementedError

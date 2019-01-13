from os import sys, path
from lxml import html
from os.path import join, dirname
import requests
import re
from . import constants


__author__ = "Ehud Adler"
__copyright__ = "Copyright 2018, CUNY Suite"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Ehud Adler & Akiva Sherman"
__email__ = "self@ehudadler.com"
__status__ = "Production"

'''
The Cuny Navigator makes moving around the cunyFirst website
alot easier.
'''
class CUNYFirstAPI():

    

    def __init__(self, new_session = None):
        if new_session is None:
            new_session = requests.Session()

        self._session = new_session

    def logout(self):
        try:
            self._session.get(constants.CUNY_FIRST_LOGOUT_URL)
            self._session.get(constants.CUNY_FIRST_LOGOUT_2_URL)
            self._session.get(constants.CUNY_FIRST_LOGOUT_3_URL)
            return True
        except BaseException:
            return False 

    def login(self, username, password):
            self._session.get(constants.CUNY_FIRST_HOME_URL)

            # AUTH LOGIN
            username = re.sub(r'@login\.cuny\.edu','',username)         # just in case, remove @login stuff

            data = {
                'usernameH': f'{username}@login.cuny.edu',
                'username': username,
                'password': password,
                'submit': ''
            }

            self._session.post(
                url = constants.CUNY_FIRST_AUTH_SUBMIT_URL, 
                data = data
            )

            # STUDENT CENTER
            response = self._session.get(constants.CUNY_FIRST_STUDENT_CENTER_URL)

            tree = html.fromstring(response.text)

            try:
                encquery = tree.xpath('//*[@name="enc_post_data"]/@value')[0]
            except IndexError:
                return None

            data = {'enc_post_data': encquery}

            response = self._session.post(
                url = constants.CUNY_FIRST_LOGIN_URL, 
                data = data
            )
            tree = html.fromstring(response.text)

            try:
                encreply = tree.xpath('//*[@name="enc_post_data"]/@value')[0]
            except IndexError:
                return None

            data = {'enc_post_data': encreply}
            self._session.post(
                url = constants.CUNY_FIRST_LOGIN_2_URL, 
                data=data
            )
            response = self._session.get(constants.CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL)

            return response

    def to_login(self):
        return self._session.get(constants.CUNY_FIRST_HOME_URL)

    def to_student_center(self):
        response = self.session.get(constants.CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL)
        
        return response

    def to_transcript_download(self):
        pass

    def to_current_term_grades(self, term):
        self._session.get(constants.CUNY_FIRST_GRADES_URL)
        payload = {'ICACTION': 'DERIVED_SSS_SCT_SSS_TERM_LINK'}
        try:
            response = self._session.post(
                url = constants.CUNY_FIRST_GRADES_URL, 
                data = payload
            )
        except TimeoutError:
            return None

        tree = html.fromstring(response.text)

        payload_key = ''.join(
            tree.xpath(
                f'//span[text()="{term}"]/parent::div/parent::td/preceding-sibling::td/div/input/@id'))

        payload_value = ''.join(
            tree.xpath(
                f'//span[text()="{term}"]/parent::div/parent::td/preceding-sibling::td/div/input/@value'))

        payload = {
            payload_key : payload_value,
            'ICACTION' : 'DERIVED_SSS_SCT_SSR_PB_GO'
        }

        try:
            response = self._session.post(
                url = constants.CUNY_FIRST_GRADES_URL, 
                data=payload
            )
            return response
        except TimeoutError:
            return None

    def to_choose_semester_grade_page(self):
        self._session.get(constants.CUNY_FIRST_GRADES_URL)
        payload = {'ICACTION': 'DERIVED_SSS_SCT_SSS_TERM_LINK'}
        try:
            response = self._session.post(
                url = constants.CUNY_FIRST_GRADES_URL, 
                data = payload
            )
            return response
        except TimeoutError:
            return None

    def to_search_classes(self):
        pass

    def to_weekly_schedule(self):
        pass

    def to_exam_schedule(self):
        pass

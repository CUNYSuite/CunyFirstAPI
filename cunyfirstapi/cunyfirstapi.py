###***********************************###
'''
Grade Notifier
File: cunyfirstaapi.py
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###

from os import sys, path
from lxml import html
from os.path import join, dirname
import requests
import re
from . import constants



'''
The Cuny Navigator makes moving around the cunyFirst website
alot easier.
'''
class PersistentSession:

    def __init__(self, username=None, password=None):
        self._session = requests.Session()
        self._username = username
        self._password = password
        self._history = []

    # provide everything a session has
    def __getattr__(self, attr_name):  
        if not self.is_logged_in():
            self.login(self._username, self._password)
        history.append(__getattribute__(attr_name))
        return self._session.__getattribute__(attr_name)
   

    # Revive
    #
    # The __getattr__ method keeps a list of all get, post request
    # In this method we sign you back in and retrace your steps
    # Allowing for true revival. The session will have exactly
    # the same history and will be in the same location
    def revive(self):
        login(self._username, self._password)        
        for moment in history:
            self._session.moment

    def get_history(self):
        return self._history

    def is_logged_in(self):   
        r = self._session.get(
            constants.CUNY_FIRST_HOME_URL_TEST,
            allow_redirects=False)
        return not r.status_code == 302

    def login(self, username, password):
        self._username = username
        self._password = password
        new_session = requests.Session()
        new_session.get(constants.CUNY_FIRST_HOME_URL)

        # AUTH LOGIN
        # just in case, remove @login stuff
        username = re.sub(r'@login\.cuny\.edu','',username)  

        data = {
            'usernameH': f'{username}@login.cuny.edu',
            'username': username,
            'password': password,
            'submit': ''
        }

        new_session.post(
            url = constants.CUNY_FIRST_AUTH_SUBMIT_URL, 
            data = data
        )

        # STUDENT CENTER
        response = new_session.get(constants.CUNY_FIRST_STUDENT_CENTER_URL)
        tree = html.fromstring(response.text)

        try:
            encquery = tree.xpath('//*[@name="enc_post_data"]/@value')[0]
        except IndexError:
            return None

        data = {'enc_post_data': encquery}
        response = new_session.post(
            url = constants.CUNY_FIRST_LOGIN_URL, 
            data = data
        )
        tree = html.fromstring(response.text)

        try:
            encreply = tree.xpath('//*[@name="enc_post_data"]/@value')[0]
        except IndexError:
            return None

        data = {'enc_post_data': encreply}
        new_session.post(
            url = constants.CUNY_FIRST_LOGIN_2_URL, 
            data=data
        )
        response = new_session.get(constants.CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL)
        self._session = new_session
        return response

class CUNYFirstAPI():

    def __init__(self, username=None, password=None):
        self._username = username
        self._password = password
        self._session = PersistentSession(self._username, self._password)

    def restart_session(self):
        if self._session is None:
            new_session = requests.Session()
            self._session = PersistentSession(self._username, self._password)
        else:
            self._session =  new_session.login(
                new_session._username, 
                new_session._password
            )

    def logout(self):
        try:
            self._session.get(constants.CUNY_FIRST_LOGOUT_URL)
            self._session.get(constants.CUNY_FIRST_LOGOUT_2_URL)
            self._session.get(constants.CUNY_FIRST_LOGOUT_3_URL)
            return True
        except BaseException:
            return False 

    def set_password(self, password):
        self._password = password

    def set_username(self, username):
        self._username = username

    def get_current_session(self):
        return self._session

    def is_logged_in(self):
        return self._session.is_logged_in()

    def login(self):
        # Pass through to session class
        self._session.login(self._username, self._password)

    def to_login(self):
        return self._session.get(constants.CUNY_FIRST_HOME_URL)

    def to_student_center(self, data=None, headers=None):
        if data is None:
            request_method = self._session.get
        else:
            request_method = self._session.post

        if headers is None:
            headers = self._session.headers

        response = request_method(url=constants.CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL, data=data, headers=headers)
        
        return response

    def to_transcript_download(self, college_code):
        
        # go to transcript request page without properly navigating, throw an error and get the values of the hidden form
        url = constants.CUNY_FIRST_TRANSCRIPT_REQUEST_URL
        response = self._session.get(url)
        #print(r.text)
        tree = html.fromstring(response.text)                  # parse the html DOM
        data = {}                                       # store the key-value pairs for the form here
        for el in tree.xpath('//input'):
            # iterate through the hidden form
            name = ''.join(el.xpath('./@name'))
            value = ''.join(el.xpath('./@value'))
            #print(name,value)
            data[name] = value
        
        # manually make some changes to the form
        data['ICAJAX'] = '1'
        data['ICNAVTYPEDROPDOWN'] = '1'
        data['ICYPos'] = '144'
        data['ICStateNum'] = '1'
        data['ICAction'] = 'DERIVED_SSS_SCR_SSS_LINK_ANCHOR4'
        data['ICBcDomData'] = ''
        data['DERIVED_SSS_SCL_SSS_MORE_ACADEMICS'] = '9999'
        data['DERIVED_SSS_SCL_SSS_MORE_FINANCES'] = '9999'
        data['CU_SF_SS_INS_WK_BUSINESS_UNIT'] = college_code
        data['DERIVED_SSS_SCL_SSS_MORE_PROFILE'] = '9999'

        # set url to student center menu
        self.to_student_center(data=data)
       
        # navigate to the academics page
        self._session.get(constants.CUNY_FIRST_MY_ACADEMICS_URL)
        
        # modify form for next stage
        data['ICStateNum'] = '3'
        data['ICAction'] = 'DERIVED_SSSACA2_SS_UNOFF_TRSC_LINK'
        data['ICYPos'] = '95'
        data['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$'] = '9999'
        data['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$'] = '9999'

        # go to transcript request page by posting data saying we want to go
        response = self._session.post(url, data=data)

        #data['url'] = url

        url = constants.CUNY_FIRST_TRANSCRIPT_REQUEST_URL

        response = self._session.get(url)            # actually go to transcript request page

        return response

    def download_transcript(self, college_code, data=None):
        if data is None:
            data = {'ICElementNum': '0'}
        # modify the form data to say we declared a college to pick from

        url = constants.CUNY_FIRST_TRANSCRIPT_REQUEST_URL
        r = self._session.get(url)
        #print(re.search(r'ICSID.*',r.text))
        tree = html.fromstring(r.text)
        data['ICAJAX'] = '1'
        data['ICSID'] = tree.xpath('//*[@id="ICSID"]/@value')[0]

        data['ICStateNum'] = '5'
        data['ICAction'] = 'SA_REQUEST_HDR_INSTITUTION'
        data['SA_REQUEST_HDR_INSTITUTION'] = college_code
        data['ICYPos'] ='115'

        # tell it we picked that college
        r = self._session.post(url, data=data)

        # tell it we selected "Student Unofficial Transcript"
        data['ICStateNum'] = '6'
        r = self._session.post(url, data=data)

        # submit our final request to view report
        data['ICStateNum'] = '7'
        data['ICAction'] = 'GO'
        data['DERIVED_SSTSRPT_TSCRPT_TYPE3'] = 'STDNT'

        r = self._session.post(url, data=data)

        # the response contains the url of the transcript. extract with regex
        pdfurl = re.search(r'window.open\(\'(https://hrsa\.cunyfirst\.cuny\.edu/psc/.*\.pdf)',r.text).group(1)

        # get the resource at the extracted url, which is the pdf of the transcript
        r = self._session.get(pdfurl)
        return r
        

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


from os import sys, path
from bs4 import BeautifulSoup
from lxml import etree
from twilio.rest import Client
from lxml import html
from os.path import join, dirname

__author__ = "Ehud Adler"
__copyright__ = "Copyright 2018, CUNY Suite"
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Ehud Adler & Akiva Sherman"
__email__ = "self@ehudadler.com"
__status__ = "Production"

CUNY_FIRST_HOME_URL = "https://home.cunyfirst.cuny.edu"
CUNY_FIRST_AUTH_SUBMIT_URL = "https://ssologin.cuny.edu/oam/server/auth_cred_submit"
CUNY_FIRST_STUDENT_CENTER_URL = "https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE" \
    + "/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?FolderPath" \
    + "=PORTAL_ROOT_OBJECT.HC_SSS_STUDENT_CENTER&IsFolder" \
    + "=false&IgnoreParamTempl=FolderPath%2cIsFolder&PortalActualURL" \
    + "=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc%2fcnyhcprd%2f" \
    + "EMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL" \
    + "&PortalContentURL=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc" \
    + "%2fcnyhcprd%2fEMPLOYEE%2fHRMS%2fc%2f" \
    + "SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalContentProvider" \
    + "=HRMS&PortalCRefLabel=Student%20Center&PortalRegistryName" \
    + "=EMPLOYEE&PortalServletURI=https%3a%2f%2fhome.cunyfirst.cuny.edu" \
    + "%2fpsp%2fcnyepprd%2f&PortalURI" \
    + "=https%3a%2f%2fhome.cunyfirst.cuny.edu%2fpsc%2fcnyepprd%2f" \
    + "&PortalHostNode=EMPL&NoCrumbs=yes&PortalKeyStruct=yes"
CUNY_FIRST_LOGIN_URL = "https://ssologin.cuny.edu/obrareq.cgi"
CUNY_FIRST_LOGIN_2_URL = "https://hrsa.cunyfirst.cuny.edu/obrar.cgi"
CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL = "https://hrsa.cunyfirst.cuny.edu/psc" \
    + "/cnyhcprd/EMPLOYEE/HRMS/c" \
    + "/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?FolderPath" \
    + "=PORTAL_ROOT_OBJECT.HC_SSS_STUDENT_CENTER&IsFolder" \
    + "=false&IgnoreParamTempl=FolderPath%2cIsFolder&PortalActualURL" \
    + "=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc%2fcnyhcprd" \
    + "%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&" \
    + "PortalContentURL=https%3a%2f%2fhrsa.cunyfirst.cuny.edu" \
    + "%2fpsc%2fcnyhcprd%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES." \
    + "SSS_STUDENT_CENTER.GBL&PortalContentProvider=HRMS&PortalCRefLabel" \
    + "=Student%20Center&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2f" \
    + "home.cunyfirst.cuny.edu%2fpsp%2fcnyepprd%2f&PortalURI" \
    + "=https%3a%2f%2fhome.cunyfirst.cuny.edu%2fpsc%2fcnyepprd%2f&PortalHostNode" \
    + "=EMPL&NoCrumbs=yes&PortalKeyStruct=yes"
CUNY_FIRST_GRADES_URL = "https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/" \
    + "SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL?Page=SSR_SSENRL_GRADE&Action" \
    + "=A&TargetFrameName=None"
CUNY_FIRST_HOME_URL_TEST = 'https://home.cunyfirst.cuny.edu/psp/cnyepprd/EMPLOYEE/EMPL/h/?tab=DEFAULT'
CUNY_FIRST_LOGOUT_URL = 'https://home.cunyfirst.cuny.edu/psp/cnyepprd/EMPLOYEE/EMPL/?cmd=logout'
CUNY_FIRST_LOGOUT_2_URL = 'https://home.cunyfirst.cuny.edu/sso/logout?end_url=https://home.cunyfirst.cuny.edu'
CUNY_FIRST_LOGOUT_3_URL = 'https://ssologin.cuny.edu/oamsso-bin/logout.pl?end_url=https%3A' \
    + '%2F%2Fhome.cunyfirst.cuny.edu'

'''
The Cuny Navigator makes moving around the cunyFirst website
alot easier.
'''
class CUNYFirstAPI():

    session = None

    def __init__(self, new_session):
        self.session = new_session

    def logout(self):
        try:
            session.get(constants.CUNY_FIRST_LOGOUT_URL)
            session.get(constants.CUNY_FIRST_LOGOUT_2_URL)
            session.get(constants.CUNY_FIRST_LOGOUT_3_URL)
            return True
        except BaseException:
            return None

    def login(self, username, password):
            session.get(CUNY_FIRST_HOME_URL)

            # AUTH LOGIN
            data = {
                'usernameH': '{0}@login.cuny.edu'.format(username),
                'username': username,
                'password': password,
                'submit': ''
            }

            session.current.post(
                CUNY_FIRST_AUTH_SUBMIT_URL, 
                data=data
            )

            # STUDENT CENTER
            response = session.get(CUNY_FIRST_STUDENT_CENTER_URL)

            tree = html.fromstring(response.text)
            try:
                encquery = tree.xpath('//*[@name="enc_post_data"]/@value')[0]
            except IndexError:
                return None

            data = {'enc_post_data': encquery}
            response = session.post(
                CUNY_FIRST_LOGIN_URL, 
                data=data
            )
            tree = html.fromstring(response.text)

            try:
                encreply = tree.xpath('//*[@name="enc_post_data"]/@value')[0]
            except IndexError:
                return None

            data = {'enc_post_data': encreply}
            session.current.post(
                CUNY_FIRST_LOGIN_2_URL, 
                data=data
            )
            response = session.get(CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL)

            return response

    def to_login(self):
        return self.session.get(CUNY_FIRST_HOME_URL)

    def to_student_center(self):

        response = self.session.get(CUNY_FIRST_STUDENT_CENTER_URL)
        tree = html.fromstring(response.text)

        try:
            encquery = tree.xpath('//*[@name="enc_post_data"]/@value')[0]
        except IndexError:
            return None

        data = {'enc_post_data': encquery}
        response = self.session.post(CUNY_FIRST_LOGIN_URL, data=data)

        tree = html.fromstring(response.text)
        try:
            encreply = tree.xpath('//*[@name="enc_post_data"]/@value')[0]
        except IndexError:
            return None
        data = {'enc_post_data': encreply}
        self.session.post(CUNY_FIRST_LOGIN_2_URL, data=data)

        response = self.session.get(CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL)
        
        return response

    def to_transcript_download(self):
        pass

    def to_current_term_grades(self, term):
        self.session.get(CUNY_FIRST_GRADES_URL)
        payload = {'ICACTION': 'DERIVED_SSS_SCT_SSS_TERM_LINK'}
        try:
            response = self.session.post(
                CUNY_FIRST_GRADES_URL, 
                data=payload
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
            payload_key: payload_value,
            'ICACTION': 'DERIVED_SSS_SCT_SSR_PB_GO'
        }

        try:
            response = session.current.post(CUNY_FIRST_GRADES_URL, data=payload)
            return response
        except TimeoutError:
            return None

    def to_choose_semester_grade_page(self):
        self.session.get(CUNY_FIRST_GRADES_URL)
        payload = {'ICACTION': 'DERIVED_SSS_SCT_SSS_TERM_LINK'}
        try:
            response = self.session.post(
                CUNY_FIRST_GRADES_URL, 
                data=payload
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

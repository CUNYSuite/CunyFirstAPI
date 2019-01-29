###***********************************###
'''
CUNYFirstAPI
File: transcript.py
Author: Ehud Adler
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###
from lxml import html, etree
from os.path import join
import re
from cunyfirstapi import constants
from cunyfirstapi.helper import get_semester
from cunyfirstapi.actions_locations import ActionObject, Location

class Transcript_Page(Location):
    def move(self):
        data = {}                              
        url = constants.CUNY_FIRST_TRANSCRIPT_REQUEST_URL
        response = self._session.get(url)
        tree = html.fromstring(response.text)
        for el in tree.xpath('//input'):
            # iterate through the hidden form
            name = ''.join(el.xpath('./@name'))
            value = ''.join(el.xpath('./@value'))
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
        data['CU_SF_SS_INS_WK_BUSINESS_UNIT'] = self._college_code
        data['DERIVED_SSS_SCL_SSS_MORE_PROFILE'] = '9999'

        # set url to student center menu
        #self.to_student_center(data=data)
        self._session.get(url=constants.CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL, data=data)
       
        # navigate to the academics page
        self._session.get(url=constants.CUNY_FIRST_MY_ACADEMICS_URL)
        
        # modify form for next stage
        data['ICStateNum'] = '3'
        data['ICAction'] = 'DERIVED_SSSACA2_SS_UNOFF_TRSC_LINK'
        data['ICYPos'] = '95'
        data['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$7$'] = '9999'
        data['DERIVED_SSTSNAV_SSTS_MAIN_GOTO$8$'] = '9999'

        # go to transcript request page by posting data saying we want to go
        response = self._session.post(url, data=data)
        url = constants.CUNY_FIRST_TRANSCRIPT_REQUEST_URL
        response = self._session.get(url) 
        return self

    def action(self):
        return Transcript_Page_Action(self)
        

class Transcript_Page_Action(ActionObject):

    def __init__(self, location):
        self._location = location

    def location(self):
        return self._location

    def download(self, alt_college_code=None):
        if data is None:
            data = {'ICElementNum': '0'}

        college_code = self.location()._college_code

        if alt_college_code:
            college_code = alt_college_code

        url = constants.CUNY_FIRST_TRANSCRIPT_REQUEST_URL
        r = self.location()._session.get(url)
        tree = html.fromstring(r.text)

        data['ICAJAX'] = '1'
        data['ICSID'] = tree.xpath('//*[@id="ICSID"]/@value')[0]
        data['ICStateNum'] = '5'
        data['ICAction'] = 'SA_REQUEST_HDR_INSTITUTION'
        data['SA_REQUEST_HDR_INSTITUTION'] = college_code
        data['ICYPos'] ='115'

        # tell it we picked that college
        r = self.location()._session.post(url, data=data)

        # tell it we selected "Student Unofficial Transcript"
        data['ICStateNum'] = '6'
        r = self.location()._session.post(url, data=data)

        # submit our final request to view report
        data['ICStateNum'] = '7'
        data['ICAction'] = 'GO'
        data['DERIVED_SSTSRPT_TSCRPT_TYPE3'] = 'STDNT'

        r = self.location()._session.post(url, data=data)

        # the response contains the url of the transcript. extract with regex
        pdfurl = re.search(r'window.open\(\'(https://hrsa\.cunyfirst\.cuny\.edu/psc/.*\.pdf)',r.text).group(1)

        # get the resource at the extracted url, which is the pdf of the transcript
        r = self.location()._session.get(pdfurl)
        return r

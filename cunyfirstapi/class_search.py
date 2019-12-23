###***********************************###
'''
CUNYFirstAPI
File: class_search.py
Author: Eric Akiva Sherman
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###
from os import sys, path
from lxml import html, etree
from bs4 import BeautifulSoup
import re
from os.path import join
from cunyfirstapi import constants
from cunyfirstapi.helper import get_semester
from cunyfirstapi.actions_locations import ActionObject, Location

from pprint import pprint
class Class_Search(Location):
    def move(self):
        headers = {
            'Origin': 'https://hrsa.cunyfirst.cuny.edu',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Referer': constants.CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL,
            'Connection': 'keep-alive',
        }
        payload = { 'ICAJAX': '1',
                    'ICNAVTYPEDROPDOWN': '1',
                    'ICType': 'Panel',
                    'ICElementNum': '0',
                    #'ICStateNum': '6',
                    'ICAction': 'DERIVED_SSS_SCR_SSS_LINK_ANCHOR1',
                    'ICXPos': '0',
                    'ICYPos': '180',
                    'ResponsetoDiffFrame': '-1',
                    'TargetFrameName': 'None',
                    'FacetPath': 'None',
                    'ICFocus': '',
                    'ICSaveWarningFilter': '0',
                    'ICChanged': '-1',
                    'ICAutoSave': '0',
                    'ICResubmit': '0',
                    'ICSID': self._session.icsid,
                    'ICActionPrompt': 'false',
                    'ICBcDomData': '',
                    'ICFind': '',
                    'ICAddCount': '',
                    'ICAPPCLSDATA': '',
                    'DERIVED_SSS_SCL_SSS_MORE_ACADEMICS': '9999',
                    'DERIVED_SSS_SCL_SSS_MORE_FINANCES': '9999',
                    #'CU_SF_SS_INS_WK_BUSINESS_UNIT': 'QNS01',
                    'DERIVED_SSS_SCL_SSS_MORE_PROFILE': '9999',
                    'ptus_defaultlocalnode': 'PSFT_CNYHCPRD',
                    'ptus_dbname': 'CNYHCPRD',
                    'ptus_portal': 'EMPLOYEE',
                    'ptus_node': 'HRMS',
                    'ptus_workcenterid': ''}
        
        #pprint(self._session.cookies.get_dict())

        self._response = self._session.post(url=constants.CUNY_FIRST_STUDENT_CENTER_BASE_URL, 
            data=payload, 
            headers=headers)
        #print(self._response.text)
        self._response = self._session.get(url=constants.CUNY_FIRST_CLASS_SEARCH_URL, 
            headers=headers)
        #print(self._response.text)

        return self
    def action(self):
        return Class_Search_Action(self)


class Class_Search_Action(ActionObject):

    def __init__(self, location):
        self._location = location

    def location(self):
        return self._location #Class_Search()

    '''
    ICAction: Tell the server we are gonna search for a class now
    ICSID: The unique key which tells the server what session we are
    institution: one of the cuny college codes which tells the server
                  which college we are searching for classes in
    term: number code of the term we are searching for classes in.
    TODO: write a function which retrieves number codes based on name  
    subject: capital letter course code (CSCI, ENSCI, LCD, etc...)
    course_number_match: type of match for course_number
                         'E' -> exactly match (default)
                         'C' -> contains digits
                         'G' -> greater than or equal to
                         'T' -> less than or equal to
    course_number: the course code (111 in CSCI 111, or the 3 in ASTR 3. etc...)
    course_career: undergraduate or graduate (those are the options for QNS)
                         'GRAD' -> graduate
                         'UGRD' -> undergraduate
    course_attribute: courses for specific programs such as ASAP, 
                         SEEK, ESL, Macaulay, etc...
                         see website for full list (PUT THEM ALL IN THE DOCS)
    course_attribute_value: subprograms within the course_attribute program
                         see website for full list (PUT THEM ALL IN THE DOCS?)
    requirement_designation: choose which requirement designation the courses
                         should fulfill (Creative Expression, Scientific World, etc...)
    open_classes_only: True if only looking for open classes, False for all classes
    course_keyword: provide keywords to filter course search by
    course_component: search by class type being lecture, lab, dissertation, etc...
                        (SEE WEBSITE AND PUT IN DOCS)
    class_number: choose specific class ID number (will return exactly 1 result)   
    session: decide which session of a term to look for 
            examples: 6 week 1, 6 week 2, winter, 8 week 1 etc...
            see website for full list (PUT THEM ALL IN THE DOCS)
    mode_of_instruction: courses taught in a specific mode of instruction
                            fully online, hybrid, in person etc...
                            see website for full list (PUT THEM ALL IN THE DOCS) 
    meeting_start_time_match: decide if class start time between 2 times (will be done in net PR)
                                after a time, before a time etc...
    meeting_start_time: time in format of HH:MMAM or HH:MMPM
    meeting_end_time_match: decide if class end time between 2 times (will be done in net PR)
                                after a time, before a time etc...
    meeting_end_time: time in format of HH:MMAM or HH:MMPM
    days_of_week_match: decide if to include any/only of specified days (J/I)
                               or to exclude any/only of specified days (F/E)
                               (SEE WEBSITE AND PUT IN DOCS)
    days_of_week: array with names of days of the week for the type of match specified above
    minimum_units_match: match course by credits with numerical comparison
                        'GT' -> greater than
                        'GE' -> greater than or equal to (default)
                        'E' -> equal to
                        'LT' -> less than
                        'LE' -> less than or equal to
    minimum_units: lowest number of credits, matched by above comparison type
    maximum_units_match: match course by credits with numerical comparison
                        'GT' -> greater than
                        'GE' -> greater than or equal to 
                        'E' -> equal to
                        'LT' -> less than
                        'LE' -> less than or equal to (default)
    maximum_units: highest number of credits, matched by above comparison type
    campus: name of campus (varies by college, so check website)
    _location: name of location (varies by college+campus, check website)
    instructor_last_name_match: type of comparison for instructor's last name
                        'B' -> begins with
                        'C' -> contains
                        'E' -> is exactly
    instructor_last_name: part or whole of instructor's last name, match by above
    '''   
    def submit_search(self, 
        institution, 
        term, 
        course_number='', 
        subject='', 
        course_number_match='E', 
        course_career='', 
        course_attribute='', 
        course_attribute_value='', 
        requirement_designation='',
        open_classes_only=True, 
        session='', 
        mode_of_instruction='', 
        meeting_start_time_match='GE',
        meeting_start_time='', 
        meeting_end_time_match='LE',
        meeting_end_time='', 
        days_of_week_match='', 
        days_of_week=None, 
        class_number='', 
        course_keyword='',
        minimum_units_match='GE', 
        minimum_units='', 
        maximum_units_match='LE', 
        maximum_units='', 
        course_component='', 
        campus='', 
        _location='', 
        instructor_last_name_match='B', 
        instructor_last_name='', 
        parsed=True):
        
        if days_of_week is None:
            days_of_week = []

        if len(subject) > 8:
            raise ValueError(f"The value for the field \"Subject\" was over by {len(subject)-8} "+
                "characters. Reduce to 8 or fewer characters.")
        days_of_week = set(map(lambda x: x.lower(), days_of_week))

        headers = {
            'Origin': 'https://hrsa.cunyfirst.cuny.edu',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Referer': constants.CUNY_FIRST_CLASS_SEARCH_URL,
            'Connection': 'keep-alive',
        }  

        # tell server who we are and what we wanna do
        action_options = {
            'ICAction': 'CLASS_SRCH_WRK2_SSR_PB_CLASS_SRCH',
            'ICSID': self._location._session.icsid
            }
        # fill in mandatory options of college and term
        mandatory_options = {
            'CLASS_SRCH_WRK2_INSTITUTION$31$': institution,
            'CLASS_SRCH_WRK2_STRM$35$': term
            }
        # options pertaining to the generic course itself, or a specific class based on number
        course_options = {
            'SSR_CLSRCH_WRK_SUBJECT_SRCH$0' : subject,
            'SSR_CLSRCH_WRK_SSR_EXACT_MATCH1$1': course_number_match,
            'SSR_CLSRCH_WRK_CATALOG_NBR$1': course_number,
            'SSR_CLSRCH_WRK_ACAD_CAREER$2': course_career,
            'SSR_CLSRCH_WRK_CRSE_ATTR$3': course_attribute,
            'SSR_CLSRCH_WRK_CRSE_ATTR_VALUE$3': course_attribute_value,
            'SSR_CLSRCH_WRK_CU_RQMNT_DESIGNTN$4': requirement_designation,
            'SSR_CLSRCH_WRK_SSR_OPEN_ONLY$chk$5': 'Y' if open_classes_only else 'N',
            'SSR_CLSRCH_WRK_DESCR$11': course_keyword,
            'SSR_CLSRCH_WRK_SSR_COMPONENT$13': course_component,
            'SSR_CLSRCH_WRK_CLASS_NBR$10': class_number
        }
        #pprint(course_options)
        # options pertaining to when the class of a course takes place
        day_time_options = {
            'SSR_CLSRCH_WRK_SESSION_CODE$6': session,
            'SSR_CLSRCH_WRK_INSTRUCTION_MODE$7': mode_of_instruction,
            'SSR_CLSRCH_WRK_SSR_START_TIME_OPR$8': meeting_start_time_match,
            'SSR_CLSRCH_WRK_MEETING_TIME_START$8': meeting_start_time,
            'SSR_CLSRCH_WRK_SSR_END_TIME_OPR$8': meeting_end_time_match,
            'SSR_CLSRCH_WRK_MEETING_TIME_END$8': meeting_end_time,
            'SSR_CLSRCH_WRK_INCLUDE_CLASS_DAYS$9': days_of_week_match,
            'SSR_CLSRCH_WRK_MON$chk$9': '' if 'monday' not in days_of_week else 'Y',
            'SSR_CLSRCH_WRK_TUES$chk$9': '' if 'tuesday' not in days_of_week else 'Y',
            'SSR_CLSRCH_WRK_WED$chk$9': '' if 'wednesday' not in days_of_week else 'Y',
            'SSR_CLSRCH_WRK_THURS$chk$9': '' if 'thursday' not in days_of_week else 'Y',
            'SSR_CLSRCH_WRK_FRI$chk$9': '' if 'friday' not in days_of_week else 'Y',
            'SSR_CLSRCH_WRK_SAT$chk$9': '' if 'saturday' not in days_of_week else 'Y',
            'SSR_CLSRCH_WRK_SUN$chk$9': '' if 'sunday' not in days_of_week else 'Y',
        }
        # options pertaining to how many credits a course is
        credits_options = {
            'SSR_CLSRCH_WRK_SSR_UNITS_MIN_OPR$12': minimum_units_match,
            'SSR_CLSRCH_WRK_UNITS_MINIMUM$12': minimum_units,
            'SSR_CLSRCH_WRK_SSR_UNITS_MAX_OPR$12': maximum_units_match,
            'SSR_CLSRCH_WRK_UNITS_MAXIMUM$12': maximum_units,
        }
        # options pertaining to where the class is located
        location_options = {    
            'SSR_CLSRCH_WRK_CAMPUS$14': campus,
            'SSR_CLSRCH_WRK_LOCATION$15': _location,
        }
        # options pertaining to who is teaching the class
        instructor_options = {
            'SSR_CLSRCH_WRK_SSR_EXACT_MATCH2$16': instructor_last_name_match,
            'SSR_CLSRCH_WRK_LAST_NAME$16': instructor_last_name
        }
        # stitch em all together
        payload = dict(action_options, **mandatory_options, **course_options, 
            **day_time_options, **credits_options, **location_options, **instructor_options)

        response = self.location()._session.post(
            url=constants.CUNY_FIRST_CLASS_SEARCH_URL, 
            data=payload, 
            headers=headers)
        ###################################################
        if not parsed:
            return response.text

        
        result = []
        if re.search(r'<span  class=\'SSSMSGWARNINGTEXT\'.*</span>', response.text):
            #print(re.search(r'<span  class=\'SSSMSGWARNINGTEXT\'.*</span>', response.text).group(0))
            tree = html.fromstring(re.search(r'<span  class=\'SSSMSGWARNINGTEXT\'.*</span>', response.text).group(0))
            warning = ''.join(tree.xpath('//span[@class="SSSMSGWARNINGTEXT"]/text()'))
            return {
                'results': result,
                'success' : False,
                'reason' : warning
            }
        if re.search(r'<span  class=\'SSSMSGALERTTEXT\'.*</span>', response.text):
            #print(re.search(r'<span  class=\'SSSMSGWARNINGTEXT\'.*</span>', response.text).group(0))
            tree = html.fromstring(re.search(r'<span  class=\'SSSMSGALERTTEXT\'.*</span>', response.text).group(0))
            warning = ''.join(tree.xpath('//span[@class="SSSMSGALERTTEXT"]/text()'))
            return {
                'results': result,
                'success' : False,
                'reason' : warning
            }

        if re.search(r'processing_win0\(0,3000\);addMsg\("(.*)"\);playMsg\(\);', response.text):
            tree = html.fromstring(re.search(r'processing_win0\(0,3000\);addMsg\("(.*)"\);playMsg\(\);', 
                response.text).group(1))
            warning = ''.join(tree.xpath('//span[@class="popupText"]/text()'))
            return {
                'results': result,
                'success' : False,
                'reason' : warning
            }
        
        #print(response.text)
        tree = html.fromstring(re.search(r'(<table class=\'PSPAGECONTAINER\'[\s\S]*</table>)\n<DIV class=',response.text).group(1))
        course_divs = tree.xpath('//div[contains(@id,"win0divSSR_CLSRSLT_WRK_GROUPBOX2") and not(contains(@id,"GP"))]')

        for div in course_divs:
            rows = div.xpath('.//tr[contains(@id,"trSSR_CLSRCH_MTG1$") and contains(@id,"_row")]')
            div_title = ''.join(div.xpath('.//div[contains(@id,"win0divSSR_CLSRSLT_WRK_GROUPBOX2GP")]/text()'))
            div_title = re.sub('\xa0',' ',div_title)
            _subject, _course_number, _title = re.search(r'^\s(\w+)\s+([\d\w]+)\s*-\s*(.+)',div_title).group(1,2,3)
            for row in rows:
                row_info = {
                    'subject': _subject,
                    'course_number': _course_number,
                    'title': _title,
                    'description': ''.join(row.xpath('../../../../following-sibling::tr//span[contains(@id,"DERIVED_CLSRCH_DESCRLONG$")]/text()')),
                    'class_number': ''.join(row.xpath('.//a[contains(@id,"MTG_CLASS_NBR$")]/text()')).strip(),
                    'section': ''.join(row.xpath('.//a[contains(@id,"MTG_CLASSNAME$")]/text()')).strip(),
                    'days_and_times': ''.join(row.xpath('.//span[contains(@id,"MTG_DAYTIME$")]/text()')).strip(),
                    'room': ''.join(row.xpath('.//span[contains(@id,"MTG_ROOM$")]/text()')).strip(),
                    'instructor': ''.join(row.xpath('.//span[contains(@id,"MTG_INSTR$")]/text()')).strip(),
                    'meeting_dates': ''.join(row.xpath('.//span[contains(@id,"MTG_TOPIC$")]/text()')).strip(),
                    'status': re.search(r'OPEN|CLOSED|WAITLIST',''.join(row.xpath('.//img[@class="SSSIMAGECENTER"]/@src'))).group(0).strip(),
                    'bookstore_link': '',    #''.join(row.xpath('.//a[contains(@id,"MTG_INSTR$")]/text()'))
                    'mode_of_instruction': ''.join(row.xpath('.//span[contains(@id,"INSTRUCT_MODE_DESCR$")]/text()')).strip()
                }

                # you wouldn't believe it but cunyfirst actually does not always properly return
                # open classes. good job cunyfirst
                if open_classes_only and row_info['status'] != 'OPEN':
                    continue
                result.append(row_info)
        results = {
            'results': result,
            'success': True
        }
        return results

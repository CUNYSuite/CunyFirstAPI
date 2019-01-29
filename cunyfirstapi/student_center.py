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
from cunyfirstapi import constants
from cunyfirstapi.actions_locations import ActionObject, Location

import re
from lxml import html
from pprint import pprint

class Student_Center(Location):
    def move(self, data=None, headers=None):
        if data is None:
            request_method = self._session.get
        else:
            request_method = self._session.post

        if headers is None:
            headers = self._session.headers

        self._response = request_method(
            url=constants.CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL, 
            data=data, 
            headers=headers
        )

        return self

    def action(self):
        return Student_Center_Action(self)
        

class Student_Center_Action(ActionObject):

    def __init__(self, location):
        self._location = location

    def location(self):
        return self._location

    def _get_window_content(self, window_id):
        tree = html.fromstring(self.location()._response.text)
        window_table = tree.xpath(f'//table[@id="{window_id}"]')[0]
        text_as_list = list(
                filter(None,map(
                    str.strip,window_table.xpath('.//text()')
                    )
                )
            )
        return text_as_list       

    def holds(self):
        return self._get_window_content('SRVCIND_HOLD_VW$scroll$0')

    def todo(self):
        return self._get_window_content('ACE_DERIVED_SSS_SCL_DESCR2')

    def milestones(self):
        return self._get_window_content('SSR_CARMLSTN_VW$scroll$0')

    def schedule(self, filename=None):
        data = {
            "scheduleTitle": "",
        }

        tree = html.fromstring(self.location()._response.text)

        course_codes = tree.xpath('//span[contains(@id,"CLASS_NAME$span")]')
        course_details = tree.xpath('//span[contains(@id,"DERIVED_SSS_SCL_SSR_MTG_SCHED_LONG")]')
        table = [] 
        for code_node, detail_node in zip(course_codes, course_details):
            code =list(
                map(lambda x: re.sub('\r','',x), code_node.xpath('.//text()')))
            details =list(
                map(lambda x: re.sub('\r','',x), detail_node.xpath('.//text()')))
            table += [*code, *details]

        for i in range(0,len(table),4):
            course_code = table[i]
            course_type = table[i+1]
            times = table[i+2]
            room = table[i+3]

            course_type = re.search(r'^\w+',course_type).group(0)
            sunday = re.search('Su',times)
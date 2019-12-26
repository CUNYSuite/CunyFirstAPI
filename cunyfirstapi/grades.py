###***********************************###
'''
CUNYFirstAPI
File: grades.py
Author: Ehud Adler
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###
from os import sys, path
from lxml import html, etree
from bs4 import BeautifulSoup
from lxml import etree
from os.path import join
from cunyfirstapi import constants
from cunyfirstapi.helper import get_semester
from cunyfirstapi.actions_locations import ActionObject, Location

class Student_Grades(Location):
    def move(self):
        self._session.get(constants.CUNY_FIRST_GRADES_URL)
        payload = {'ICACTION': 'DERIVED_SSS_SCT_SSS_TERM_LINK'}
        term = get_semester()
        try:
            response = self._session.post(
                url = constants.CUNY_FIRST_GRADES_URL, 
                data = payload
            )
            tree = html.fromstring(response.text)
            payload_key = ''.join(tree.xpath(
                    f'//span[text()="{term}"]/parent::div/parent::td/preceding-sibling::td/div/input/@id'
            ))

            payload_value = ''.join(tree.xpath(
                    f'//span[text()="{term}"]/parent::div/parent::td/preceding-sibling::td/div/input/@value'
            ))
            payload = {
                payload_key : payload_value,
                'ICACTION' : 'DERIVED_SSS_SCT_SSR_PB_GO'
            }
            self._response = self._session.post(
                url=constants.CUNY_FIRST_GRADES_URL, 
                data=payload
            )
            return self
        except TimeoutError:
            return None

    def action(self):
        return Student_Grades_Action(self)
        

class Student_Grades_Action(ActionObject):

    def __init__(self, location):
        self._location = location

    def location(self):
        return self._location

    def grades(self):
        tree = BeautifulSoup(self._location._response.text, 'lxml')
        good_html = tree.prettify()
        soup = BeautifulSoup(good_html, 'html.parser')
        result = []
        refresh_result = None

        try:
            table = soup.findAll(
                'table', attrs={'class': "PSLEVEL1GRIDWBO"}
            )[0]  # get term table
        except BaseException:
            raise ValueError('Could not find grades table')

        if table is not None:
            row_marker = 0
            for row in table.find_all('tr'):
                column_marker = 0
                row_marker += 1
                columns = row.find_all('td')
                data = []
                for column in columns:
                    if row_marker > 1:
                        data.append(column.get_text())
                    column_marker += 1
                if len(data) is not 0:
                    new_class = {
                        'name': data[0].strip(),
                        'description': data[1].strip(),
                        'units': data[2].strip(),
                        'grading': data[3].strip(),
                        'grade': data[4].strip(),
                        'gradepts': data[5].strip()
                    }
                    result.append(new_class)

            gpa_stats = soup.findAll(
                'table', attrs={'class': "PSLEVEL1GRIDWBO"}
            )[1]  # get gpa table

            last_row = gpa_stats.find_all('tr')[-1]
            term_gpa_text = last_row.find_all('td')[1].get_text().strip()
            if not term_gpa_text:
                term_gpa_text = '-1'

            term_gpa = float(term_gpa_text)

            cumulative_gpa_text = last_row.find_all('td')[-1].get_text().strip()
            if not cumulative_gpa_text:
                cumulative_gpa_text = '-1'

            cumulative_gpa = float(cumulative_gpa_text)
            
            return { 'results': result, 'term_gpa': term_gpa, 'cumulative_gpa': cumulative_gpa }
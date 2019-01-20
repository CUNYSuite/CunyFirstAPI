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
from lxml import html
from bs4 import BeautifulSoup
from lxml import etree
from os.path import join, dirname
import requests
import re
from . import constants
from .helper import get_semester

class Student_Grades(Location):

    def move(self):
        self._session.get(constants.CUNY_FIRST_GRADES_URL)
        payload = {'ICACTION': 'DERIVED_SSS_SCT_SSS_TERM_LINK'}
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
            response = self._session.post(
                url = constants.CUNY_FIRST_GRADES_URL, 
                data=payload
            )
            return Student_Grades_Action()
        except TimeoutError:
            return None

    def request(self)
        return Student_Grade_Request()
        

class Student_Grades_Action(ActionObject):
    def location(self):
        return Student_Center()

    def grades(self, self._session):

        tree = BeautifulSoup(response.text, 'lxml')
        good_html = tree.prettify()
        soup = BeautifulSoup(good_html, 'html.parser')
        result = []
        refresh_result = None

        try:
            table = soup.findAll(
                'table', attrs={'class': "PSLEVEL1GRIDWBO"}
            )[0]  # get term table
        except BaseException:
            table = None

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
                    new_class = Class(
                        data[0].strip(), 
                        data[1].strip(),
                        data[2].strip(), 
                        data[3].strip(),
                        data[4].strip(), 
                        data[5].strip()
                    )
                    result.append(new_class)

            gpa_stats = soup.findAll(
                'table', attrs={'class': "PSLEVEL1GRIDWBO"}
            )[1]  # get gpa table

            last_row = gpa_stats.find_all('tr')[-1]
            term_gpa_text = last_row.find_all('td')[1].get_text().strip()
            if not term_gpa_text:
                term_gpa_text = '-1'

            term_gpa = float(term_gpa_text)
            cumulative_gpa = float(last_row.find_all('td')[-1].get_text())
            refresh_result = RefreshResult(result, GPA(term_gpa, cumulative_gpa))
            return grades
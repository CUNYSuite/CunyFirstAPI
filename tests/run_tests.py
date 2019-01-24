###***********************************###
'''
CUNYFirstAPI
File: tests.py
Author: Ehud Adler
Core Maintainers: Ehud Adler, Akiva Sherman, 
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###
import unittest
import sys
from os import sys, path
import os
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from cunyfirstapi.locations_enum import Locations
from cunyfirstapi import CUNYFirstAPI
from cunyfirstapi.redacted_stdout import RedactedPrint, \
    STDOutOptions, RedactedFile

username = None
password = None
redacted_print_std = None
redacted_print_err = None

class TestTest(unittest.TestCase):
    def test(self):
        self.assertEqual(True, True)

class TestLogin(unittest.TestCase):
    def test(self):
        if not is_ci():
            self.assertTrue(True)
        else:
            global username
            global password
            api = CUNYFirstAPI(username, password)
            api.login()
            self.assertTrue(api.is_logged_in())

class TestClassSearch(unittest.TestCase):
    def test(self):
        if not is_ci():
            self.assertTrue(True)
        else:
            global username
            global password

            api = CUNYFirstAPI(username, password)
            api.login()

            # test course match, days of week, start/end times
            loc = api.move_to(Locations.class_search).location()
            result1 = loc.action().submit_search(institution='QNS01', term='1192', 
                course_number='1', course_number_match='G', days_of_week=['Monday','Wednesday'],
                meeting_start_time='12:00PM', meeting_end_time='3:00PM')
            test1 = len(result1['results']) > 0

            # test day of week match
            loc = api.move_to(Locations.class_search).location()
            result2 = loc.action().submit_search(institution='QNS01', term='1192', course_number_match='G',
                course_number='1', days_of_week_match='J', days_of_week=['Tuesday'])
            test2 = len(result2['results']) == 0

            # test mode of instruction, open classes only, requirement designation
            loc = api.move_to(Locations.class_search).location()
            result3 = loc.action().submit_search(institution='QNS01', term='1192', course_number='1',
                course_number_match='G', requirement_designation='FSW',
                meeting_start_time='12:00PM', meeting_end_time='3:00PM', 
                open_classes_only=False, mode_of_instruction='H')
            test3 = len(result3['results']) > 0

            # test last name match and last name
            loc = api.move_to(Locations.class_search).location()
            result4 = loc.action().submit_search(institution='QNS01', term='1192', course_number='1',
                course_number_match='G', instructor_last_name_match='B', 
                instructor_last_name='Obren', open_classes_only=False)
            test4 = len(result4['results']) > 0

            # test invalid subject value by length
            loc = api.move_to(Locations.class_search).location()
            try:
                result5 = loc.action().submit_search(institution='QNS01', term='1192', subject='FAKESUBJECT', course_number='111')
                self.assertTrue(False)
            except ValueError:
                self.assertTrue(True)
            

            # test invalid time
            loc = api.move_to(Locations.class_search).location()
            result6 = loc.action().submit_search(institution='QNS01', term='1192', 
                course_number='111', subject='CSCI', meeting_start_time='25:00AM', parsed=True)
            test6 = len(result6['results']) == 0


            self.assertTrue(test1)
            self.assertTrue(test2)
            self.assertTrue(test3)
            self.assertTrue(test4)
            self.assertTrue(test6)


def get_username_password():
    global username
    global password
    with open(".env", "r") as f:
        username = f.readline().strip()
        password = f.readline().strip()

def monkey_path_print():
    global username
    global password
    global redacted_print_std
    global redacted_print_err
    ## Monkey Patching stdout to remove any sens. data
    redacted_list = [username, password]
    redacted_print_std = RedactedPrint(STDOutOptions.STDOUT, redacted_list)
    redacted_print_err = RedactedPrint(STDOutOptions.ERROR, redacted_list)
    redacted_print_std.enable()
    redacted_print_err.enable()

def is_local():
    return not is_venus_mars() and not is_ci()

def is_venus_mars():
    return socket.gethostname() == "venus" or socket.gethostname() == "mars"

def is_ci():
    return os.path.isfile(".ci")

def run_test():
    unittest.main()

def main():
    if is_ci():
        print("Running on CI.....")
        get_username_password()
        monkey_path_print()

    run_test()

if __name__ == '__main__':
    main()
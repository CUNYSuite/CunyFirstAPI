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
sys.path.append(path.dirname(path.dirname(path.abspath(__file__))))
from cunyfirstapi.locations_enum import Locations
from cunyfirstapi import CUNYFirstAPI

#import CUNYFirstAPI
import argparse
import sys

username = ''
password = ''


class TestTest(unittest.TestCase):
    def test(self):
        self.assertEqual(True, True)


class ClassSearchTest(unittest.TestCase):
    def test(self):
        if not is_ci():
            self.assertTrue(True)

        global username
        global password
        api = CUNYFirstAPI(username, password)
        api.login()
        search_page = api.move_to(Locations.class_search)
        results = search_page.submit_search(institution='QNS01', term='1192', \
            subject = 'CSCI', course_number='111')
        self.assertTrue(len(results['results']) > 0)



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

def get_username_password():
    global username
    global password
    with open(".env", "r") as f:
        username = f.readline()
        password = f.readline()


def is_local():
    return not is_venus_mars() and not is_ci()

def is_venus_mars():
    return socket.gethostname() == "venus" or socket.gethostname() == "mars"

def is_ci():
    return os.path.isfile(".ci")


def run_test():
    scriptpath = script_path()
    instancepath = instance_path()

    if os.path.isfile(instancepath):
        os.system('rm {0}'.format(instancepath))

    os.system('touch {0}'.format(instancepath))
    unittest.main()
    os.system('rm {0}'.format(instancepath))

def main():
    if is_ci():
        print("Running on CI.....")
        get_username_password()
        monkey_path_print()
        
    run_test()

if __name__ == '__main__':

    main()
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
    unittest.main()


def main():
    if is_ci():
        print("Running on CI.....")
        get_username_password()

    run_test()

if __name__ == '__main__':

    main()
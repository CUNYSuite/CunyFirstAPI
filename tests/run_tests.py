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

global username
global password


class TestTest(unittest.TestCase):
    def test(self):
        self.assertEqual(True, True)


class ClassSearchTest(unittest.TestCase):
    def test(self):
        api = CUNYFirstAPI(username, password)
        api.login()
        search_page = api.move_to(Locations.class_search)
        results = search_page.submit_search(institution='QNS01', term='1192', \
            subject = 'CSCI', course_number='111')
        self.assertTrue(len(results['results']) > 0)



def run_test():
    global username
    global password

    parser = argparse.ArgumentParser()
    parser.add_argument('--username')
    parser.add_argument('--password')
    parser.add_argument('unittest_args', nargs='*')

    args = parser.parse_args()

    username = args.username
    password = args.password

    sys.argv[1:] = args.unittest_args
    unittest.main()

def main():
    run_test()

if __name__ == '__main__':

    main()
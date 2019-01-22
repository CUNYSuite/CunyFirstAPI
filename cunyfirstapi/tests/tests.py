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
from ..locations_enum import Location
from ..cunyfirstapi import CUNYFirstAPI

class TestTest(unittest.TestCase):
    def test(self):
        self.assertEqual(True, True)


class ClassSearchTest(unittest.TestCase):
    def test(self, username, password):
        api = CUNYFirstAPI(username, password)
        search_page = api.move_to(Location.class_search)
        results = search_page.submit_search(institution='QNS01', term='1192', \
            subject = 'CSCI', course_number='111')
        self.assertTrue(len(results['results']) > 0)
        


def run_test():
    unittest.main()

def main():
    run_test()

if __name__ == '__main__':
    main()
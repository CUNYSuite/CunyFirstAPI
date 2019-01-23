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

#import CUNYFirstAPI
import argparse
import sys

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
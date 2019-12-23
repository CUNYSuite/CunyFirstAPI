###***********************************###
'''
CUNYFirstAPI
File: helper.py
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###

import datetime

def get_semester():
    now = datetime.datetime.now()
    today = (now.month, now.day)
    if (1, 15) <= today < (6, 15):
        return f'{now.year} Spring Term'
    elif (6, 15) <= today < (9, 15):
        return f'{now.year} Summer Term'
    else:
        if now.month == 1:
            return f'{now.year-1} Fall Term'
        else:
            return f'{now.year} Fall Term'
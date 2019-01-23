
###***********************************###
'''
CUNYFirstAPI
File: login.py
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###
import requests
import re
from lxml import html
from . import constants

def is_logged_in(session):

    # Sanity check, make sure session is not None
    if not session:
        return False

    try:
        r = session.get(
            constants.CUNY_FIRST_HOME_URL_TEST,
            allow_redirects=False)
    except TimeoutError:
        return False
    return not r.status_code == 302

def login(username, password):  
    new_session = requests.Session()
    new_session.get(constants.CUNY_FIRST_HOME_URL)
    # AUTH LOGIN
    # just in case, remove @login stuff
    username = re.sub(r'@login\.cuny\.edu','',username)  

    data = {
        'usernameH': f'{username.strip()}@login.cuny.edu',
        'username': username.strip(),
        'password': password.strip(),
        'submit': ''
    }

    print(data)

    response = new_session.post(
        url = constants.CUNY_FIRST_AUTH_SUBMIT_URL, 
        data = data
    )

    # STUDENT CENTER
    response = new_session.get(constants.CUNY_FIRST_STUDENT_CENTER_URL)
    tree = html.fromstring(response.text)

    try:
        encquery = tree.xpath('//*[@name="enc_post_data"]/@value')[0]
    except IndexError:
        return None

    data = {'enc_post_data': encquery}
    response = new_session.post(
        url = constants.CUNY_FIRST_LOGIN_URL, 
        data = data
    )
    tree = html.fromstring(response.text)

    try:
        encreply = tree.xpath('//*[@name="enc_post_data"]/@value')[0]
    except IndexError:
        return None

    data = {'enc_post_data': encreply}
    new_session.post(
        url = constants.CUNY_FIRST_LOGIN_2_URL, 
        data=data
    )
    response = new_session.get(constants.CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL)
    return new_session

    def logout(session):
        try:
            session.get(constants.CUNY_FIRST_LOGOUT_URL)
            session.get(constants.CUNY_FIRST_LOGOUT_2_URL)
            session.get(constants.CUNY_FIRST_LOGOUT_3_URL)
            return True
        except BaseException:
            return False 
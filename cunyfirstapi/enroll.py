###***********************************###
'''
CUNYFirstAPI
File: student_center.py
Author: Ehud Adler
Core Maintainers: Ehud Adler, Akiva Sherman,
Yehuda Moskovits
Copyright: Copyright 2019, Ehud Adler
License: MIT
'''
###***********************************###
from cunyfirstapi import constants
from cunyfirstapi.actions_locations import ActionObject, Location
from lxml import html
import re

class Enrollment(Location):
    def move(self):
        headers = {
            'Origin': 'https://hrsa.cunyfirst.cuny.edu',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Referer': constants.CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL,
            'Connection': 'keep-alive',
        }
        payload = { 'ICAJAX': '1',
                    'ICNAVTYPEDROPDOWN': '1',
                    'ICType': 'Panel',
                    'ICElementNum': '0',
                    #'ICStateNum': '6',
                    'ICAction': 'DERIVED_SSS_SCR_SSS_LINK_ANCHOR3',
                    'ICXPos': '0',
                    'ICYPos': '180',
                    'ResponsetoDiffFrame': '-1',
                    'TargetFrameName': 'None',
                    'FacetPath': 'None',
                    'ICFocus': '',
                    'ICSaveWarningFilter': '0',
                    'ICChanged': '-1',
                    'ICAutoSave': '0',
                    'ICResubmit': '0',
                    'ICSID': self._session.icsid,
                    'ICActionPrompt': 'false',
                    'ICBcDomData': '',
                    'ICFind': '',
                    'ICAddCount': '',
                    'ICAPPCLSDATA': '',
                    'DERIVED_SSS_SCL_SSS_MORE_ACADEMICS': '9999',
                    'DERIVED_SSS_SCL_SSS_MORE_FINANCES': '9999',
                    'DERIVED_SSS_SCL_SSS_MORE_PROFILE': '9999',
                    'ptus_defaultlocalnode': 'PSFT_CNYHCPRD',
                    'ptus_dbname': 'CNYHCPRD',
                    'ptus_portal': 'EMPLOYEE',
                    'ptus_node': 'HRMS',
                    'ptus_workcenterid': ''}

        self._response = self._session.post(url=constants.CUNY_FIRST_STUDENT_CENTER_BASE_URL, 
            data=payload, 
            headers=headers)

        self._response = self._session.get(url=constants.CUNY_FIRST_ENROLLMENT_CART_BASE_URL, 
            headers=headers)

        return self

    def action(self):
        return Enrollment_Action(self)
        

class Enrollment_Action(ActionObject):
    def __init__(self, location):
        self._location = location

    def location(self):
        return self._location 

    def add_course_to_cart(self, term, class_number, lab_number=None, academic_career='UGRD', wait_list=False, permission_number=''):
        payload = {
          'ICAJAX': '1',
          'ICNAVTYPEDROPDOWN': '0',
          'ICType': 'Panel',
          'ICElementNum': '0',
          'ICAction': 'DERIVED_SSS_SCT_SSR_PB_GO',
          'ResponsetoDiffFrame': '-1',
          'TargetFrameName': 'None',
          'FacetPath': 'None',
          'ICFocus': '',
          'ICSaveWarningFilter': '0',
          'ICChanged': '-1',
          'ICAutoSave': '0',
          'ICResubmit': '0',
          'ICSID': self.location()._session.icsid,
          'ICActionPrompt': 'false',
          'ICFind': '',
          'ICAddCount': '',
          'ICAPPCLSDATA': '',
          'SSR_DUMMY_RECV1$sels$1$$0': '1',
          'ptus_defaultlocalnode': 'PSFT_CNYHCPRD',
          'ptus_dbname': 'CNYHCPRD',
          'ptus_portal': 'EMPLOYEE',
          'ptus_node': 'HRMS',
          'ptus_workcenterid': '',
          'ptus_componenturl': ''
        }
        r = self.location()._session.post(url=constants.CUNY_FIRST_ENROLLMENT_CART_BASE_URL, data=payload)

        params = {
            'ACAD_CAREER': academic_career,
            'INSTITUTION': self.location()._college_code,
            'STRM': term
        }
        r = self.location()._session.get(constants.CUNY_FIRST_ENROLLMENT_CART_BASE_URL, params=params)

        payload = {
          'ICAJAX': '1',
          'ICNAVTYPEDROPDOWN': '0',
          'ICType': 'Panel',
          'ICElementNum': '0',
          'ICAction': 'DERIVED_REGFRM1_SSR_PB_ADDTOLIST2$9$',
          'ResponsetoDiffFrame': '-1',
          'TargetFrameName': 'None',
          'FacetPath': 'None',
          'ICFocus': '',
          'ICSaveWarningFilter': '0',
          'ICChanged': '-1',
          'ICAutoSave': '0',
          'ICResubmit': '0',
          'ICSID': self.location()._session.icsid,
          'ICActionPrompt': 'false',
          'ICBcDomData': 'undefined',
          'ICFind': '',
          'ICAddCount': '',
          'ICAPPCLSDATA': '',
          'DERIVED_REGFRM1_CLASS_NBR': str(class_number),
          'DERIVED_REGFRM1_SSR_CLS_SRCH_TYPE$249$': '06',
          'ptus_defaultlocalnode': 'PSFT_CNYHCPRD',
          'ptus_dbname': 'CNYHCPRD',
          'ptus_portal': 'EMPLOYEE',
          'ptus_node': 'HRMS',
          'ptus_workcenterid': '',
          'ptus_componenturl': ''
        }

        r = self.location()._session.post(constants.CUNY_FIRST_ENROLLMENT_CART_BASE_URL, data=payload)

        if lab_number is not None:
            table_html = re.search(r'<table dir=\'ltr\'(.|\n)*?</table>', r.text).group(0)
            tree = html.fromstring(table_html)
            position = -1
            for index, row in enumerate(tree.xpath('.//tr')):
                if ''.join(row.xpath('./td[2]//text()')).strip() == str(lab_number):
                    position = index - 1
                    break
            if position < 0:
                raise ValueError('Lab may be on next page. Send message to developer to fix')

            payload = {
              'ICAJAX': '1',
              'ICNAVTYPEDROPDOWN': '0',
              'ICType': 'Panel',
              'ICElementNum': '0',
              'ICAction': 'DERIVED_CLS_DTL_NEXT_PB',
              'ResponsetoDiffFrame': '-1',
              'TargetFrameName': 'None',
              'FacetPath': 'None',
              'ICFocus': '',
              'ICSaveWarningFilter': '0',
              'ICChanged': '-1',
              'ICAutoSave': '0',
              'ICResubmit': '0',
              'ICSID': self.location()._session.icsid,
              'ICActionPrompt': 'false',
              'ICBcDomData': 'undefined',
              'ICFind': '',
              'ICAddCount': '',
              'ICAPPCLSDATA': '',
             f'SSR_CLS_TBL_R1$sels${position}$$0': str(position),
              'ptus_defaultlocalnode': 'PSFT_CNYHCPRD',
              'ptus_dbname': 'CNYHCPRD',
              'ptus_portal': 'EMPLOYEE',
              'ptus_node': 'HRMS',
              'ptus_workcenterid': '',
              'ptus_componenturl': ''
            }

            r = self.location()._session.post(constants.CUNY_FIRST_ENROLLMENT_CART_BASE_URL, data=payload)

        payload = {
          'ICAJAX': '1',
          'ICNAVTYPEDROPDOWN': '0',
          'ICType': 'Panel',
          'ICElementNum': '0',
          'ICAction': 'DERIVED_CLS_DTL_NEXT_PB$280$',
          'ResponsetoDiffFrame': '-1',
          'TargetFrameName': 'None',
          'FacetPath': 'None',
          'ICFocus': '',
          'ICSaveWarningFilter': '0',
          'ICChanged': '-1',
          'ICAutoSave': '0',
          'ICResubmit': '0',
          'ICSID': self.location()._session.icsid,
          'ICActionPrompt': 'false',
          'ICBcDomData': 'undefined',
          'ICFind': '',
          'ICAddCount': '',
          'ICAPPCLSDATA': '',
          'DERIVED_CLS_DTL_WAIT_LIST_OKAY$125$$chk': 'Y' if wait_list else 'N',
          'DERIVED_CLS_DTL_CLASS_PRMSN_NBR$118$': str(permission_number),
          'ptus_defaultlocalnode': 'PSFT_CNYHCPRD',
          'ptus_dbname': 'CNYHCPRD',
          'ptus_portal': 'EMPLOYEE',
          'ptus_node': 'HRMS',
          'ptus_workcenterid': '',
          'ptus_componenturl': ''
        }

        r = self.location()._session.post(constants.CUNY_FIRST_ENROLLMENT_CART_BASE_URL, data=payload)

        return r
        
    def enroll_all_courses(self, term=None, academic_career='UGRD'):
        if term is not None:
            params = {
                'ACAD_CAREER': academic_career,
                'INSTITUTION': self.location()._college_code,
                'STRM': term
            }
            r = self.location()._session.get(constants.CUNY_FIRST_ENROLLMENT_CART_BASE_URL, params=params)
        payload = {
          'ICAJAX': '1',
          'ICNAVTYPEDROPDOWN': '1',
          'ICType': 'Panel',
          'ICElementNum': '1',
          'ICAction': 'DERIVED_REGFRM1_LINK_ADD_ENRL$82$',
          'ResponsetoDiffFrame': '-1',
          'TargetFrameName': 'None',
          'FacetPath': 'None',
          'ICFocus': '',
          'ICSaveWarningFilter': '0',
          'ICChanged': '-1',
          'ICAutoSave': '0',
          'ICResubmit': '0',
          'ICSID': self.location()._session.icsid,
          'ICActionPrompt': 'false',
          'ICBcDomData': '',
          'ICFind': '',
          'ICAddCount': '',
          'ICAPPCLSDATA': '',
          'DERIVED_REGFRM1_CLASS_NBR': '',
          'DERIVED_REGFRM1_SSR_CLS_SRCH_TYPE$249$': '06',
          'ptus_defaultlocalnode': 'PSFT_CNYHCPRD',
          'ptus_dbname': 'CNYHCPRD',
          'ptus_portal': 'EMPLOYEE',
          'ptus_node': 'HRMS',
          'ptus_workcenterid': '',
          'ptus_componenturl': 'https://hrsa.cunyfirst.cuny.edu/psp/cnyhcprd/EMPLOYEE/HRMS/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL'
        }

        r = self.location()._session.post(constants.CUNY_FIRST_ENROLLMENT_CART_BASE_URL, data=payload)
        # print(r.text)
        enroll_request_url = re.search(r'document\.location=\'(.*)\'', r.text).group(1)
        # print(enroll_request_url)
        r = self.location()._session.get(enroll_request_url)

        payload = {
          'ICAJAX': '1',
          'ICNAVTYPEDROPDOWN': '1',
          'ICType': 'Panel',
          'ICElementNum': '1',
          'ICAction': 'DERIVED_REGFRM1_SSR_PB_SUBMIT',
          'ResponsetoDiffFrame': '-1',
          'TargetFrameName': 'None',
          'FacetPath': 'None',
          'ICFocus': '',
          'ICSaveWarningFilter': '0',
          'ICChanged': '-1',
          'ICAutoSave': '0',
          'ICResubmit': '0',
          'ICSID': self.location()._session.icsid,
          'ICActionPrompt': 'false',
          'ICBcDomData': '',
          'ICFind': '',
          'ICAddCount': '',
          'ICAPPCLSDATA': '',
          'ptus_defaultlocalnode': 'PSFT_CNYHCPRD',
          'ptus_dbname': 'CNYHCPRD',
          'ptus_portal': 'EMPLOYEE',
          'ptus_node': 'HRMS',
          'ptus_workcenterid': '',
          'ptus_componenturl': ''
        }

        r = self.location()._session.post(constants.CUNY_FIRST_ENROLLMENT_ADD_URL, data=payload)

        table_html = re.search(r'<table border=\'1\' cellspacing=\'0\' class=\'PSLEVEL1GRIDWBO\'(.|\n)*?</table>', r.text).group(0)
        tree = html.fromstring(table_html)
        results = []
        for row in tree.xpath('./tr[position()>1]'):

            _class = ''.join(row.xpath('./td[1]//text()'))
            message = ''.join(row.xpath('./td[2]//text()'))

            success = True

            if ''.join(row.xpath('./td[3]//img/@alt')) == 'Error':
                success = False

            result = {
                'class': re.sub(r'(\xa0|\s)+', ' ', _class.strip()),
                'message': message.strip(),
                'success': success
            }

            results.append(result)

        return results

    def drop_from_schedule(self, term, course, academic_career='UGRD'):
        try:
            iter(course)
        except TypeError:
            course = {course}

        params = {
              'ACAD_CAREER': academic_career,
              'INSTITUTION': self.location()._college_code,
              'STRM': term
        }
        r = self.location()._session.get(constants.CUNY_FIRST_ENROLLMENT_DROP_URL, params=params)
        payload = {
          'ICAJAX': '1',
          'ICNAVTYPEDROPDOWN': '0',
          'ICType': 'Panel',
          'ICElementNum': '0',
          'ICAction': 'DERIVED_SSS_SCT_SSR_PB_GO',
          'ResponsetoDiffFrame': '-1',
          'TargetFrameName': 'None',
          'FacetPath': 'None',
          'ICFocus': '',
          'ICSaveWarningFilter': '0',
          'ICChanged': '-1',
          'ICAutoSave': '0',
          'ICResubmit': '0',
          'ICSID': self.location()._session.icsid,
          'ICActionPrompt': 'false',
          'ICFind': '',
          'ICAddCount': '',
          'ICAPPCLSDATA': '',
          'SSR_DUMMY_RECV1$sels$1$$0': '1',
          'ptus_defaultlocalnode': 'PSFT_CNYHCPRD',
          'ptus_dbname': 'CNYHCPRD',
          'ptus_portal': 'EMPLOYEE',
          'ptus_node': 'HRMS',
          'ptus_workcenterid': '',
          'ptus_componenturl': ''
        }
        r = self.location()._session.post(url=constants.CUNY_FIRST_ENROLLMENT_DROP_URL, data=payload)

        r = self.location()._session.get(constants.CUNY_FIRST_ENROLLMENT_DROP_URL, params=params)

        payload = {
          'ICAJAX': '1',
          'ICNAVTYPEDROPDOWN': '0',
          'ICType': 'Panel',
          'ICElementNum': '0',
          'ICAction': 'DERIVED_REGFRM1_LINK_DROP_ENRL',
          'ResponsetoDiffFrame': '-1',
          'TargetFrameName': 'None',
          'FacetPath': 'None',
          'ICFocus': '',
          'ICSaveWarningFilter': '0',
          'ICChanged': '-1',
          'ICAutoSave': '0',
          'ICResubmit': '0',
          'ICSID': self.location()._session.icsid,
          'ICActionPrompt': 'false',
          'ICFind': '',
          'ICAddCount': '',
          'ICAPPCLSDATA': '',
          'SSR_DUMMY_RECV1$sels$1$$0': '1',
          'ptus_defaultlocalnode': 'PSFT_CNYHCPRD',
          'ptus_dbname': 'CNYHCPRD',
          'ptus_portal': 'EMPLOYEE',
          'ptus_node': 'HRMS',
          'ptus_workcenterid': '',
          'ptus_componenturl': ''
        }

        table_html = re.search(r'<table border=\'1\' cellspacing=\'0\' class=\'PSLEVEL1GRIDWBO\'(.|\n)*?</table>', r.text).group(0)
        tree = html.fromstring(table_html)
        for index, row in enumerate(tree.xpath('./tr[position()>1]')):
            class_text = ''.join(row.xpath('./td[2]//text()'))
            course_number = re.search(r'\((\d+)\)', class_text).group(1)
            if course_number in course: 
                payload[f'DERIVED_REGFRM1_SSR_SELECT$chk${index}'] = 'Y'
                payload[f'DERIVED_REGFRM1_SSR_SELECT${index}'] = 'Y'

        r = self.location()._session.post(constants.CUNY_FIRST_ENROLLMENT_DROP_URL, data=payload)
        payload = {
            'ICAJAX': '1',
            'ICNAVTYPEDROPDOWN': '1',
            'ICType': 'Panel',
            'ICElementNum': '1',
            'ICAction': 'DERIVED_REGFRM1_SSR_PB_SUBMIT',
            'ResponsetoDiffFrame': '-1',
            'TargetFrameName': 'None',
            'FacetPath': 'None',
            'ICFocus': '',
            'ICSaveWarningFilter': '0',
            'ICChanged': '-1',
            'ICAutoSave': '0',
            'ICResubmit': '0',
            'ICSID': self.location()._session.icsid,
            'ICActionPrompt': 'false',
            'ICBcDomData': '',
            'ICFind': '',
            'ICAddCount': '',
            'ICAPPCLSDATA': '',
            'ptus_defaultlocalnode': 'PSFT_CNYHCPRD',
            'ptus_dbname': 'CNYHCPRD',
            'ptus_portal': 'EMPLOYEE',
            'ptus_node': 'HRMS',
            'ptus_workcenterid': '',
            'ptus_componenturl': ''
        }

        r = self.location()._session.post(constants.CUNY_FIRST_ENROLLMENT_DROP_URL, data=payload)

        table_html = re.search(r'<table border=\'1\' cellspacing=\'0\' class=\'PSLEVEL1GRIDWBO\'(.|\n)*?</table>', r.text).group(0)
        tree = html.fromstring(table_html)
        results = []
        for row in tree.xpath('./tr[position()>1]'):

            _class = ''.join(row.xpath('./td[1]//text()'))
            message = ''.join(row.xpath('./td[2]//text()'))

            success = True

            if ''.join(row.xpath('./td[3]//img/@alt')) == 'Error':
                success = False

            result = {
                'class': re.sub(r'(\xa0|\s)+', ' ', _class.strip()),
                'message': message.strip(),
                'success': success
            }

            results.append(result)

        return results

    def swap_courses(self, term, swap_out, swap_in, swap_in_lab_number='', academic_career='UGRD', wait_list=False, permission_number=''):
        params = {
            'ACAD_CAREER': academic_career,
            'INSTITUTION': self.location()._college_code,
            'STRM': term
        }
        r = self.location()._session.get(constants.CUNY_FIRST_ENROLLMENT_SWAP_URL, params=params)

        payload = {
            'ICAJAX': '1',
            'ICNAVTYPEDROPDOWN': '1',
            'ICType': 'Panel',
            'ICElementNum': '0',
            'ICAction': 'DERIVED_REGFRM1_SSR_PB_ADDTOLIST2$106$',
            'ResponsetoDiffFrame': '-1',
            'TargetFrameName': 'None',
            'FacetPath': 'None',
            'ICFocus': '',
            'ICSaveWarningFilter': '0',
            'ICChanged': '-1',
            'ICAutoSave': '0',
            'ICResubmit': '0',
            'ICSID': self.location()._session.icsid,
            'ICActionPrompt': 'false',
            'ICBcDomData': '',
            'ICFind': '',
            'ICAddCount': '',
            'ICAPPCLSDATA': '',
            'DERIVED_REGFRM1_DESCR50$225$': str(swap_out),
            'DERIVED_REGFRM1_SSR_CLS_SRCH_TYPE$144$': '06',
            'DERIVED_REGFRM1_CLASS_NBR': str(swap_in),
            'ptus_defaultlocalnode': 'PSFT_CNYHCPRD',
            'ptus_dbname': 'CNYHCPRD',
            'ptus_portal': 'EMPLOYEE',
            'ptus_node': 'HRMS',
            'ptus_workcenterid': '',
            'ptus_componenturl': ''
        }
        r = self.location()._session.post(constants.CUNY_FIRST_ENROLLMENT_SWAP_URL, data=payload)

        if swap_in_lab_number is not None:
            table_html = re.search(r'<table dir=\'ltr\'(.|\n)*?</table>', r.text).group(0)
            tree = html.fromstring(table_html)
            position = -1
            for index, row in enumerate(tree.xpath('.//tr')):
                if ''.join(row.xpath('./td[2]//text()')).strip() == str(swap_in_lab_number):
                    position = index - 1
                    break
            if position < 0:
                raise ValueError('Lab may be on next page. Send message to developer to fix')

            payload = {
              'ICAJAX': '1',
              'ICNAVTYPEDROPDOWN': '0',
              'ICType': 'Panel',
              'ICElementNum': '0',
              'ICAction': 'DERIVED_CLS_DTL_NEXT_PB',
              'ResponsetoDiffFrame': '-1',
              'TargetFrameName': 'None',
              'FacetPath': 'None',
              'ICFocus': '',
              'ICSaveWarningFilter': '0',
              'ICChanged': '-1',
              'ICAutoSave': '0',
              'ICResubmit': '0',
              'ICSID': self.location()._session.icsid,
              'ICActionPrompt': 'false',
              'ICBcDomData': 'undefined',
              'ICFind': '',
              'ICAddCount': '',
              'ICAPPCLSDATA': '',
             f'SSR_CLS_TBL_R1$sels${position}$$0': str(position),
              'ptus_defaultlocalnode': 'PSFT_CNYHCPRD',
              'ptus_dbname': 'CNYHCPRD',
              'ptus_portal': 'EMPLOYEE',
              'ptus_node': 'HRMS',
              'ptus_workcenterid': '',
              'ptus_componenturl': ''
            }

            r = self.location()._session.post(constants.CUNY_FIRST_ENROLLMENT_SWAP_URL, data=payload)

        payload = {
            'ICAJAX': '1',
            'ICNAVTYPEDROPDOWN': '1',
            'ICType': 'Panel',
            'ICElementNum': '0',
            'ICAction': 'DERIVED_CLS_DTL_NEXT_PB',
            'ResponsetoDiffFrame': '-1',
            'TargetFrameName': 'None',
            'FacetPath': 'None',
            'ICFocus': '',
            'ICSaveWarningFilter': '0',
            'ICChanged': '-1',
            'ICAutoSave': '0',
            'ICResubmit': '0',
            'ICSID': self.location()._session.icsid,
            'ICActionPrompt': 'false',
            'ICBcDomData': '',
            'ICFind': '',
            'ICAddCount': '',
            'ICAPPCLSDATA': '',
            'DERIVED_CLS_DTL_WAIT_LIST_OKAY$125$$chk': 'Y' if wait_list else 'N',
            'DERIVED_CLS_DTL_CLASS_PRMSN_NBR$118$': permission_number,
            'ptus_defaultlocalnode': 'PSFT_CNYHCPRD',
            'ptus_dbname': 'CNYHCPRD',
            'ptus_portal': 'EMPLOYEE',
            'ptus_node': 'HRMS',
            'ptus_workcenterid': '',
            'ptus_componenturl': ''
        }

        r = self.location()._session.post(constants.CUNY_FIRST_ENROLLMENT_SWAP_URL, data=payload)

        table_html = re.search(r'<table border=\'1\' cellspacing=\'0\' class=\'PSLEVEL1GRIDWBO\'  id=\'CLASS_TBL_VW7\$scroll\$0\'(.|\n)*?</table>', r.text).group(0)
        tree = html.fromstring(table_html)
        results = {}

        results['swap_out'] = []
        for row in tree.xpath('./tr[position()>1]'):
            row_info = {
              'class' : ''.join(row.xpath('./td[1]//text()')).strip(),
              'description' : ''.join(row.xpath('./td[2]//text()')).strip(),
              'days_and_times' : ''.join(row.xpath('./td[3]//text()')).strip(),
              'room' : ''.join(row.xpath('./td[4]//text()')).strip(),
              'instructor' : ''.join(row.xpath('./td[5]//text()')).strip(),
              'units' : ''.join(row.xpath('./td[6]//text()')).strip(),
              'status' : ''.join(row.xpath('./td[7]//img/@alt')).strip().upper()
            }
            results['swap_out'].append(row_info)

        table_html = re.search(r'<table border=\'1\' cellspacing=\'0\' class=\'PSLEVEL1GRIDWBO\'  id=\'SSR_SS_ERD_VW\$scroll\$0\'(.|\n)*?</table>', r.text).group(0)
        tree = html.fromstring(table_html)
        results['swap_in'] = []
        for row in tree.xpath('./tr[position()>1]'):
            row_info = {
              'class': ''.join(row.xpath('./td[1]//text()')).strip(),
              'description': ''.join(row.xpath('./td[2]//text()')).strip(),
              'days_and_times': ''.join(row.xpath('./td[3]//text()')).strip(),
              'room': ''.join(row.xpath('./td[4]//text()')).strip(),
              'instructor': ''.join(row.xpath('./td[5]//text()')).strip(),
              'units': ''.join(row.xpath('./td[6]//text()')).strip(),
              'status': ''.join(row.xpath('./td[7]//img/@alt')).strip().upper()
            }
            results['swap_in'].append(row_info)

        payload = {
            'ICAJAX': '1',
            'ICNAVTYPEDROPDOWN': '1',
            'ICType': 'Panel',
            'ICElementNum': '1',
            'ICAction': 'DERIVED_REGFRM1_SSR_PB_SUBMIT',
            'ResponsetoDiffFrame': '-1',
            'TargetFrameName': 'None',
            'FacetPath': 'None',
            'ICFocus': '',
            'ICSaveWarningFilter': '0',
            'ICChanged': '-1',
            'ICAutoSave': '0',
            'ICResubmit': '0',
            'ICSID': self.location()._session.icsid,
            'ICActionPrompt': 'false',
            'ICBcDomData': '',
            'ICFind': '',
            'ICAddCount': '',
            'ICAPPCLSDATA': '',
            'ptus_defaultlocalnode': 'PSFT_CNYHCPRD',
            'ptus_dbname': 'CNYHCPRD',
            'ptus_portal': 'EMPLOYEE',
            'ptus_node': 'HRMS',
            'ptus_workcenterid': '',
            'ptus_componenturl': ''
        }

        r = self.location()._session.post(constants.CUNY_FIRST_ENROLLMENT_DROP_URL, data=payload)

        table_html = re.search(r'<table border=\'1\' cellspacing=\'0\' class=\'PSLEVEL1GRIDWBO\'(.|\n)*?</table>', r.text).group(0)
        tree = html.fromstring(table_html)
        results = []
        for row in tree.xpath('./tr[position()>1]'):

            _class = ' '.join(row.xpath('./td[1]//text()'))
            message = ''.join(row.xpath('./td[2]//text()'))

            success = True

            if ''.join(row.xpath('./td[3]//img/@alt')) == 'Error':
                success = False

            result = {
                'class': re.sub(r'(\xa0|\s)+', ' ', _class.strip()),
                'message': message.strip(),
                'success': success
            }

            results.append(result)

        return results

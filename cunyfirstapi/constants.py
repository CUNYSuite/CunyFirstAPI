
# College names and codes pulled from the CunyFirst website
college_codes = {
    'BAR01': 'Baruch College',
    'BMC01': 'Borough of Manhattan CC',
    'BCC01': 'Bronx CC',
    'BKL01': 'Brooklyn College',
    'CTY01': 'City College',
    'CSI01': 'College of Staten Island',
    'GRD01': 'Graduate Center',
    'NCC01': 'Guttman CC',
    'HOS01': 'Hostos CC',
    'HTR01': 'Hunter College',
    'JJC01': 'John Jay College',
    'KCC01': 'Kingsborough CC',
    'LAG01': 'LaGuardia CC',
    'LEH01': 'Lehman College',
    'MHC01': 'Macaulay Honors College',
    'MEC01': 'Medgar Evers College',
    'NYT01': 'NYC College of Technology',
    'QNS01': 'Queens College',
    'QCC01': 'Queensborough CC',
    'SOJ01': 'School of Journalism',
    'SLU01': 'School of Labor&Urban Studies',
    'LAW01': 'School of Law',
    'MED01': 'School of Medicine',
    'SPS01': 'School of Professional Studies',
    'SPH01': 'School of Public Health',
    'UAPC1': 'University Processing Center',
    'YRK01': 'York College'
}

CUNY_FIRST_HOME_URL = "https://home.cunyfirst.cuny.edu"
CUNY_FIRST_AUTH_SUBMIT_URL = "https://ssologin.cuny.edu/oam/server/auth_cred_submit"
CUNY_FIRST_STUDENT_CENTER_URL = "https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE" \
    + "/HRMS/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?FolderPath" \
    + "=PORTAL_ROOT_OBJECT.HC_SSS_STUDENT_CENTER&IsFolder" \
    + "=false&IgnoreParamTempl=FolderPath%2cIsFolder&PortalActualURL" \
    + "=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc%2fcnyhcprd%2f" \
    + "EMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL" \
    + "&PortalContentURL=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc" \
    + "%2fcnyhcprd%2fEMPLOYEE%2fHRMS%2fc%2f" \
    + "SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&PortalContentProvider" \
    + "=HRMS&PortalCRefLabel=Student%20Center&PortalRegistryName" \
    + "=EMPLOYEE&PortalServletURI=https%3a%2f%2fhome.cunyfirst.cuny.edu" \
    + "%2fpsp%2fcnyepprd%2f&PortalURI" \
    + "=https%3a%2f%2fhome.cunyfirst.cuny.edu%2fpsc%2fcnyepprd%2f" \
    + "&PortalHostNode=EMPL&NoCrumbs=yes&PortalKeyStruct=yes"
CUNY_FIRST_LOGIN_URL = "https://ssologin.cuny.edu/obrareq.cgi"
CUNY_FIRST_LOGIN_2_URL = "https://hrsa.cunyfirst.cuny.edu/obrar.cgi"
CUNY_FIRST_SIGNED_IN_STUDENT_CENTER_URL = "https://hrsa.cunyfirst.cuny.edu/psc" \
    + "/cnyhcprd/EMPLOYEE/HRMS/c" \
    + "/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL?FolderPath" \
    + "=PORTAL_ROOT_OBJECT.HC_SSS_STUDENT_CENTER&IsFolder" \
    + "=false&IgnoreParamTempl=FolderPath%2cIsFolder&PortalActualURL" \
    + "=https%3a%2f%2fhrsa.cunyfirst.cuny.edu%2fpsc%2fcnyhcprd" \
    + "%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL&" \
    + "PortalContentURL=https%3a%2f%2fhrsa.cunyfirst.cuny.edu" \
    + "%2fpsc%2fcnyhcprd%2fEMPLOYEE%2fHRMS%2fc%2fSA_LEARNER_SERVICES." \
    + "SSS_STUDENT_CENTER.GBL&PortalContentProvider=HRMS&PortalCRefLabel" \
    + "=Student%20Center&PortalRegistryName=EMPLOYEE&PortalServletURI=https%3a%2f%2f" \
    + "home.cunyfirst.cuny.edu%2fpsp%2fcnyepprd%2f&PortalURI" \
    + "=https%3a%2f%2fhome.cunyfirst.cuny.edu%2fpsc%2fcnyepprd%2f&PortalHostNode" \
    + "=EMPL&NoCrumbs=yes&PortalKeyStruct=yes"
CUNY_FIRST_GRADES_URL = "https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS/c/" \
    + "SA_LEARNER_SERVICES.SSR_SSENRL_GRADE.GBL?Page=SSR_SSENRL_GRADE&Action" \
    + "=A&TargetFrameName=None"
CUNY_FIRST_HOME_URL_TEST = 'https://home.cunyfirst.cuny.edu/psp/cnyepprd/EMPLOYEE/EMPL/h/?tab=DEFAULT'
CUNY_FIRST_LOGOUT_URL = 'https://home.cunyfirst.cuny.edu/psp/cnyepprd/EMPLOYEE/EMPL/?cmd=logout'
CUNY_FIRST_LOGOUT_2_URL = 'https://home.cunyfirst.cuny.edu/sso/logout?end_url=https://home.cunyfirst.cuny.edu'
CUNY_FIRST_LOGOUT_3_URL = 'https://ssologin.cuny.edu/oamsso-bin/logout.pl?end_url=https%3A' \
    + '%2F%2Fhome.cunyfirst.cuny.edu'
CUNY_FIRST_TRANSCRIPT_REQUEST_URL = 'https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE' \
    + '/HRMS/c/SA_LEARNER_SERVICES.SSS_TSRQST_UNOFF.GBL?Page=SSS_TSRQST_UNOFF&Action=A' \
    + '&EMPLID=&TargetFrameName=None'
CUNY_FIRST_MY_ACADEMICS_URL = 'https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS' \
    + '/c/SA_LEARNER_SERVICES.SSS_MY_ACAD.GBL?Page=SSS_MY_ACAD&Action=U&ExactKeys=Y&TargetFrameName=None'
CUNY_FIRST_STUDENT_CENTER_BASE_URL = 'https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS' \
    + '/c/SA_LEARNER_SERVICES.SSS_STUDENT_CENTER.GBL'

CUNY_FIRST_CLASS_SEARCH_URL = 'https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS' \
    + '/c/SA_LEARNER_SERVICES.CLASS_SEARCH.GBL?Page=SSR_CLSRCH_ENTRY&Action=U&ExactKeys=Y&TargetFrameName=None'
CUNY_FIRST_ENROLLMENT_ADD_URL = 'https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS'\
    + '/c/SA_LEARNER_SERVICES.SSR_SSENRL_ADD.GBL'
CUNY_FIRST_ENROLLMENT_CART_BASE_URL = 'https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS'\
    + '/c/SA_LEARNER_SERVICES.SSR_SSENRL_CART.GBL?Page=SSR_SSENRL_CART'
CUNY_FIRST_ENROLLMENT_DROP_URL = 'https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS' \
    + '/c/SA_LEARNER_SERVICES.SSR_SSENRL_DROP.GBL'
CUNY_FIRST_ENROLLMENT_SWAP_URL = 'https://hrsa.cunyfirst.cuny.edu/psc/cnyhcprd/EMPLOYEE/HRMS' \
    + '/c/SA_LEARNER_SERVICES.SSR_SSENRL_SWAP.GBL'
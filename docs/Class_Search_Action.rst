Class Search Action
-------------------

This page deals with the available functions for searching for classes

submit_search(parameters...)
        Method of the Class_Search_Action object to submit a search query with the CUNYFirst class search form.  
        Returns dictionary containing a boolean ``True`` or ``False``, and a list of dictionaries. Final return value is in the form of:

        .. code-block:: python
            
            {
                'success': ... ,         # True or False
                'results': [{                      # first course result
                    'subject': ...,     # all values are strings
                    'course_number': ...,
                    'title': ...,
                    'description': ...,
                    'class_number': ...,
                    'section': ...,
                    'days_and_times': ...,
                    'room': ...,
                    'instructor': ...,
                    'meeting_dates': ...,
                    'status': ...,      # 'OPEN', 'CLOSED', or 'WAITLIST'
                    'bookstore_link': ...,
                    'mode_of_instruction': ...
                },{
                    ...     # second course result
                }]
            }


        The available parameters are:

        institution
            This is the college code (QNS01 is Queens College. Full list available `here`) Required

        term
            This is the term code (``'1196'`` for Summer 2019, ``'1199'`` for Fall 2019) This will eventually be turned into words and wrapped. (Required)
        
        campus
            name of campus (varies by college, so check website) Default: empty string
            
            _location
                name of location (varies by college+campus, check website) Default: empty string

        class_number
            choose specific class ID number (will return exactly 1 result). Default: empty string

        course_attribute
            courses for specific programs such as ASAP, SEEK, ESL, Macaulay, etc... Will put list in eventually... Default: empty string
        
        course_attribute_value 
            subprograms within the course_attribute program. See website for list. Default: empty string

        course_career
            undergraduate or graduate (those are the options for QNS)

            - ``'GRAD'`` -> graduate  

            - ``'UGRD'`` -> undergraduate (default)

        course_component
            search by class type being lecture, lab, dissertation, etc... Default: empty string

        course_keyword
            provide keywords to filter course search by

        course_number
            the course code (111 in CSCI 111, or the 3 in ASTR 3. etc...) Default: empty string

            course_number_match 
                type of match for ``course_number``

                - ``'E'`` -> exactly match (default)
                - ``'C'`` -> contains digits
                - ``'G'`` -> greater than or equal to
                - ``'T'`` -> less than or equal to

        days_of_week
            iterable with names of days of the week for the type of match specified below. Default: ``None``

            days_of_week_match 
                How you want to match certain days. Default: empty string

            - ``'J'`` -> decide if to include any of specified days 
            - ``'I'`` -> decide if to include only specified days
            - ``'F'`` -> decide if to exclude any of specified days
            - ``'E'`` -> decide if to exclude only specified days 


        instructor_last_name
            part or whole of instructor's last name for the type of match specified below. Default: empty string

            instructor_last_name_match 
                type of comparison for instructor's last name

                - ``'B'`` -> begins with (default)
                - ``'C'`` -> contains
                - ``'E'`` -> is exactly

        maximum_units
            highest number of credits, matched by below comparison type. Default: empty string

            maximum_units_match 
                match course by credits with numerical comparison
               
                - ``'GT'`` -> greater than
                - ``'GE'`` -> greater than or equal to 
                - ``'E'`` -> equal to
                - ``'LT'`` -> less than
                - ``'LE'`` -> less than or equal to (default)

        minimum_units
            lowest number of credits, matched by below comparison type. Default: empty string

            minimum_units_match
                match course by credits with numerical comparison
                   
                - ``'GT'`` -> greater than 
                - ``'GE'`` -> greater than or equal to (default)
                - ``'E'`` -> equal to
                - ``'LT'`` -> less than
                - ``'LE'`` -> less than or equal to
        
        meeting_start_time
            time in format of ``'HH:MMAM'`` or ``'HH:MMPM'``. Default: empty string
            
            meeting_start_time_match
                decide if class start time between 2 times (NOT YET AVAILABLE), after a time, before a time etc...

                - ``'GT'`` -> greater than 
                - ``'GE'`` -> greater than or equal to (default)
                - ``'E'`` -> equal to
                - ``'LT'`` -> less than
                - ``'LE'`` -> less than or equal to

        
        meeting_end_time
            time in format of ``'HH:MMAM'`` or ``'HH:MMPM'``. Default: empty string
            
            meeting_end_time_match
                decide if class end time between 2 times (NOT YET AVAILABLE), after a time, before a time etc...

                - ``'GT'`` -> greater than
                - ``'GE'`` -> greater than or equal to 
                - ``'E'`` -> equal to
                - ``'LT'`` -> less than
                - ``'LE'`` -> less than or equal to (default)

        mode_of_instruction 
            courses taught in a specific mode of instruction. Default: empty string

                - ``'FO'`` -> Fully Online
                - ``'H'`` -> Hybrid (default)
                - ``'P'`` -> In Person
                - ``'O'`` -> Online
                - ``'PO'`` -> Partially Online
                - ``'W'`` -> Web-Enhanced

        open_classes_only
            Boolean value of ``True`` (default) for only classes that are open, or ``False`` for all classes

        requirement_designation
            choose which requirement designation the courses should fulfill. Default: empty string

                - ``'FCE'`` -> Flexible Core - Creative Expression
                - ``'FIS'`` -> Flexible Core - Individual and Society
                - ``'FSW'`` -> Flexible Core - Scientific World
                - ``'FUS'`` -> Flexible Core - US Experience in its Diversity
                - ``'FWG'`` -> Flexible Core - World Cultures & Global Issues
                - ``'REC'`` -> Required Core - English Composition
                - ``'RLP'`` -> Required Core - Life and Physical Sciences
                - ``'RMQ'`` -> Required Core - Mathematical & QuantitativeReasoning

        session
            decide which session of a term to look for. Default: empty string

                - ``'8W1'`` -> Eight Week - First
                - ``'8W2'`` -> Eight Week - Second
                - ``'11W'`` -> Eleven Week
                - ``'5W1'`` -> Five Week - First
                - ``'5W2'`` -> Five Week - Second
                - ``'5W3'`` -> Five Week - Third
                - ``'4W'`` -> Four Week
                - ``'4W1'`` -> Four Week - First
                - ``'4W4'`` -> Four Week - Fourth
                - ``'4W2'`` -> Four Week - Second
                - ``'4W3'`` -> Four Week - Third
                - ``'LT3'`` -> Less Than 3 Week
                - ``'MB2'`` -> Medical, Basic Sci Ses 2
                - ``'MBS'`` -> Medical, Basic Science
                - ``'MC2'`` -> Medical, Clinical Sci 2
                - ``'MCS'`` -> Medical, Clinical Science
                - ``'9W1'`` -> Nine Week - First
                - ``'9W2'`` -> Nine Week - Second
                - ``'PCL'`` -> Pre-College Programs
                - ``'1'`` -> Regular Academic Session
                - ``'2'`` -> Second Session
                - ``'7W1'`` -> Seven Week - First
                - ``'7W2'`` -> Seven Week - Second
                - ``'6W1'`` -> Six Week - First
                - ``'6W2'`` -> Six Week - Second
                - ``'10W'`` -> Ten Week
                - ``'3W1'`` -> Three Week - First
                - ``'3W2'`` -> Three Week - Second
                - ``'3W3'`` -> Three Week - Third
                - ``'12W'`` -> Twelve Week
                - ``'WIN'`` -> Winter

        subject
            capital letter course code (``'CSCI'``, ``'ENSCI'``, ``'LCD'``, etc...) Default: empty string

        _location
            name of location (varies by college+campus, check website) Default: empty string
Locations
---------

The different pages on CUNYFirst are all enumerated in locations_enum.py

.. code-block:: python

    class Locations():
        student_center = 0
        student_grades = 1
        transcript     = 2
        class_search   = 3
        enrollment     = 4
        ... rest of class, not really important

To use these enumerations, and to move to their respective pages:

.. code-block:: python

    import cunyfirstapi
    from cunyfirstapi.locations_enum import Locations
    # login with username and password in the constructor
    api = cunyfirstapi.CUNYFirstAPI('username', 'password')
    api.login()
    # to get the Location (not to be confused with Locations) object:
    loc = api.move_to(Locations.student_center)

    # to get the Actions object:
    act = loc.action()
    ... do stuff here...
    api.logout()


Each of the Locations objects inherits from the actions_locations.Location class

CUNYFirstAPI
------------

To login and logout using the CUNYFirstAPI object:  

.. code-block:: python

    import cunyfirstapi
    # login with username and password in the constructor
    api = cunyfirstapi.CUNYFirstAPI('username', 'password')
    api.login()
    ... do stuff here ...
    api.logout()


or if you would rather pass the username and password in to the login function:

.. code-block:: python

    import cunyfirstapi
    # login with username and password as parameters in the .login() function
    api = cunyfirstapi.CUNYFirstAPI()
    api.login('username', 'password')
    ... do stuff here ...
    api.logout()


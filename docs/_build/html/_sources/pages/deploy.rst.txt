Deployment
============
I used Pythonanywhere to deploy this dashboard. The general setup is to do development work on the local PC. All changes are pushed to the remote repository and then pulled down to the production server.
See https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/.


Create gitignore file (no extension)
---------------------------------------

.. code-block:: bash


    nano .gitignore
    # add secret key to file (e.g. fantasy/secret_key.txt)

    nano fantasy/secret_key.txt
    # update in the next step 


Changes in settings.py
-------------------------
Cut and paste the secret key to a txt document. Change debugging options.

.. code-block:: python

    # SECURITY WARNING: keep the secret key used in production secret!
    with open(os.path.join(BASE_DIR, 'secret_key.txt')) as f:
        SECRET_KEY = f.read().strip()
 
    # SECURITY WARNING: don't run with debug turned on in production!
    #DEBUG = True 
    # Use DEBUG = True in local development
    DEBUG = False
    # Use DEBUG = False turns off static files mapping
    ALLOWED_HOSTS = ['rayblick.pythonanywhere.com', '121.0.0.1']
    # Keep local host for dev testing

Create Pythonanywhere account
-------------------------------

Follow signup instructions at https://www.pythonanywhere.com


Clone project repo
---------------------

- Navigate to "Consoles tab"
- Navigate to "Start a new console" section
- Select "Bash" console and clone repo

.. code-block::  bash

    git clone https://github.com/rayblick/fantasy-surf-league.git 

- Create secret_key.txt in production


Pythonanywhere virtualenv (Django install)
---------------------------------------------

.. code-block:: bash

    $ mkvirtualenv --python=/usr/bin/python3.5 fantasy
    (fantasy)$ pip install django


Static mapping 
------------------

- Navigate to Web tab
- Navigate to static files
- Keep the URL as /static/
- Add the dashboard directory
    - /home/ray/fantasy-surf-league/fantasy/dashboard/static/


Pull any changes
--------------------
Last step is to pull in any changes from development. I am not making changes on Pythonanywhere.com.


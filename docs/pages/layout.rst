Project layout
===============
This project is separated into three main sections, including (1) data, (2) db, and (3) the django application (named "fantasy"). The development of this project evolved following this sequence of data collection, processing and visualisation. For more detail refer to the sections below.    


Tree
-----

.. code-block:: rst

    Project
    |
    ├── data
    │   ├── Events_DIM.csv #Manual data collection
    │   ├── Events_FACT.csv
    │   ├── Picks_FACT.csv
    │   ├── Player_DIM.csv
    │   └── Rounds_DIM.csv
    |
    ├── db
    │   ├── DB_CREATOR #Processes data to create fantasydb
    │   └── fantasydb #sqlite3 DB
    |
    ├── DEVLOG.md #Project change log
    |
    ├── fantasy # Django (redacted)
    │   ├── dashboard #App
    │   │   ├── static
    │   │   │   ├── css
    │   │   │   └── img
    │   │   ├── templates
    │   │   │   └── dashboard
    │   │   ├── templatetags
    │   │   ├── ...
    │   ├── db.sqlite3 # default django database
    │   ├── fantasy
    │   │   └── ...
    │   ├── fantasydb #sqlite3 (copy)
    │   └── manage.py
    |
    └── README.md


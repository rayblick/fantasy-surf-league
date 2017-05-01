Django App
============
 
The dashboard was created using Django and deployed on Pythonanywhere.com. Basic HTML and CSS syntax in this dashboard are not covered in this documentation.

Requirements
-------------
+ Python
+ Django
+ HTML
+ CSS

App Design
-------------
The template for this dashboard started with pen to paper before collecting data. I had listed all the features I wanted to display and I had a rough idea of the layout. The main feature that I wanted to include was a comparison table showing which surfers each player had selected and provide some metric of how well that surfer performed.  

The final design has four main features:
	- Information area (e.g current event)
	- Leaderboard (e.g player rank and position change)
	- Badges (e.g. lowest/highest points per event) 
	- Picks board (i.e. surfers, results, and selections by players)


Create Django Project and App
--------------------------------
Refer to https://docs.djangoproject.com/en/1.11/intro/tutorial01/ for help. 

.. code-block:: bash

	django-admin startproject fantasy
	python3.4 manage.py startapp dashboard


Generate Django Models from SQLite Database
---------------------------------------------
Copy and paste the database (fantasydb) to the parent directory of the fantasy project. Note that the code generated in models.py was reviewed and modified in several places. For example, several IntegerFields were auto-generated as TextFields.   

.. code-block:: bash

	# Generate code for models.py
	python3.4 manage.py inspectdb --database=fantasydb > dashboard/models.py


Database setup (fantasy/settings.py)
---------------------------------------

.. code-block:: python

	INSTALLED_APPS = [
		 'dashboard.apps..DashboardConfig',
		 ...
	]

	DATABASES = {
		'default': {
		    'ENGINE': 'django.db.backends.sqlite3',
		    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
		},
		# this is the new db 
		'fantasydb': { 
		    'ENGINE': 'django.db.backends.sqlite3',
		    'NAME': os.path.join(BASE_DIR, 'fantasydb'),
		    'USER': '',
		    'PASSWORD': '',
		    'HOST': '',
		    'PORT': '',
		},
	}



urls.py (dashboard app)
-------------------------
I am using two urls. The first url is the homepage that will route the user to the latest data (this functionality is done in views.py). The second url uses an integer in the url to locate the appropriate data. For example, http://127.0.0.1:8000/dashboard/2 will redirect the user to the data for the second event.    

.. code-block:: python

	from django.conf.urls import url
	from . import views

	urlpatterns = [
		url(r'^$', views.index, name='index'),
		url(r'^(?P<eventid>[0-9]+)/$', views.championshiptour, name='championshiptour'),
	]


Create User
--------------
.. code-block:: bash

	python3.4 manage.py createsuperuser
	# Follow prompts


Migrate Changes
------------------
.. code-block:: bash

	python3.4 manage.py makemigrations dashboard
	python3.4 manage.py migrate


Added Project Directories
---------------------------
New directories were created inside the dashboard app to store html pages, styling sheets and template filters. 


.. code-block:: rst

	fantasy
	│
	├── dashboard
	│   ├── admin.py
	│   ├── apps.py
	│   ├── models.py
	│   │
	│   ├── static #New
	│   │   ├── css 
	│   │   │   └── dashboard.css
	│   │   │
	│   │   └── img 
	│   │       ├── images.png
	│   │       .
	│   │
	│   ├── templates #New
	│   │   └── dashboard
	│   │       └── index.html
	│   │
	│   ├── templatetags #New
	│   │   ├── dashboard_extras.py
	│   │   ├── __init__.py
	│   │   .
	│   │
	│   .
	│
	.



Modifying views.py to Access Querysets
------------------------------------------
The dashboard has four main areas that displays different data in different structures (e.g. querysets, dicts, lists). 

views.py 
------------

.. code-block:: python

	from django.shortcuts import render
	from django.db.models import Max, Min, Sum, Avg
	from .models import FantasyPicks, FantasyPointsTable, FantasyLeaderBoard


	def index(request):
		"""
		Sends the user to the most recent events page.
		"""
		# get max event id
		maxevent = FantasyLeaderBoard.objects.using(
		  'fantasydb').aggregate(em=Max('event_id'))['em']

		# call the processing method to redirect
		return championshiptour(request, maxevent)


	def championshiptour(request, eventid):
		# Process data here...
		# Refer to comment strings in views.py

		# render page
		return render(request, 'dashboard/index.html', context)



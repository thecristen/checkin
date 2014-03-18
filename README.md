# Green Streets Walk/Ride Day Checkin

An application to quickly collect commute mode information from participants.

Features:

* Survey form for commute data like startpoint, endpoint and modes
* Leaderboard page overviews participating companies
* QRcode sent by email to receive "goodies" from to sponsors and partners

The project was originally developed at [MAPC][1] by Mariana Arcaya, Tim Reardon 
and Christian Spanring. In 2013 it has become an entirely volunteer project.

Past and present volunteer developers include:

* [Cristen Jones][3]
* [Owen Lynch][2]
* [Christian Spanring][4]

## Getting Started

### Main dependencies

The project is using [PostgreSQL][5]/[PostGIS][6] as database to store commute 
locations. Install PostGIS according to the instructions for your operating 
system and create a database.

The project is built using [Django][7], a python based web framework. Install
[Python][8] according to the instructions for your operating system.

Project dependencies are handled with [pip][9]. Install [pip][9] according to 
the instructions for your operating system.

It is recommended to use a virtual environments for Django projects. Install 
[virtualenvwrapper][10] according to the instructions for your operating system.

### Project setup

Once the main dependencies are installed, you can clone the project, ...

    $ git clone https://github.com/greenstreetsinitiative/checkin.git checkin
    $ cd checkin

setup a virtual environment ...

    $ mkvirtualenv greenstreets
    $ workon greenstreets

and install the required python (Django) modules:

	$ pip install -r requirements.txt

You'll need to set a few environment variables in your virtual environment 
`postactivate`, which you can find in `VIRTUAL_ENV_HOME/greenstreets/bin/`:

    export SECRET_KEY="abcdef"
    export DB_NAME="database name"
    export DB_USER="database user"
    export DB_PASSWORD="database user password"
    export DB_PORT="5432"
    export DB_HOST="localhost"

Then you can let Django setup your database ...

    $ python manage.py syncdb

and run the development server:

    $ python manage.py runserver

You should now see the project at [http://localhost:8000][11].

---

Copyright 2014 [Green Streets Initiative][12]


[1]: https://github.com/MAPC/greenstreets
[2]: https://github.com/olynch
[3]: https://github.com/thecristen
[4]: https://github.com/cspanring
[5]: http://www.postgresql.org/
[6]: http://postgis.net/
[7]: https://www.djangoproject.com/
[8]: http://python.org/
[9]: http://www.pip-installer.org/
[10]: http://virtualenvwrapper.readthedocs.org/
[11]: http://localhost:8000
[12]: http://gogreenstreets.org/

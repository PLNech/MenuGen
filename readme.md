# Configure the development environment

## Python

Install the following packages : `python3 python3-pip`

Then run from the root of the project

    sudo pip install virtualenv
    virtualenv -p python3 .venv
    source .venv/bin/activate
    pip install -r requirements.txt

To disable the python virtual environment, run

    deactivate

## Django

Initialize and configure the development database

    ./manage.py makemigrations
    ./manage.py migrate

Create your super user

    ./manage.py createsuperuser

# Run the development server

First check if you're using the virtualenv. If not, run

    source .venv/bin/activate

Then you can run the server with

    ./manage.py runserver

* project root - [http://127.0.0.1:8000](http://127.0.0.1:8000)
* administration interface - [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

# Migrate your local database

When models are edited, you must compute the necessary migrations from your database state, then migrate with

    ./manage.py makemigrations
    ./manage.py migrate

# Manage data in the database

Load initial data (so far the ingredients):

    ./manage.py loaddata initial_data

Create a fixture (snapshot from the data currently in the database):

    ./manage.py dumpdata > menus/fixtures/myfixture.json

Load a fixture:

    ./manage.py loaddata myfixture

Fill ingredients directly from the csv:

    ./manage.py fill_db

# References

* [Django Documentation](https://docs.djangoproject.com/en/1.7/)
* [Python Documentation](https://docs.python.org/3.4/)

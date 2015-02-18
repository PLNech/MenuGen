# README

## Configure the development environment

### Python

Install the following packages : `python3 python3-pip`

Then run from the root of the project

    sudo pip install virtualenv
    virtualenv -p python3 .venv
    source .venv/bin/activate
    pip install -r requirements.txt

To disable the python virtual environment, run

    deactivate

### Django

Initialize and configure the development database

    ./manage.py makemigrations
    ./manage.py migrate

Create your super user

    ./manage.py createsuperuser

## Run the development server

    ./manage.py runserver

You can now reach the project at [http://127.0.0.1:8000](http://127.0.0.1:8000), and the administration interface at [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

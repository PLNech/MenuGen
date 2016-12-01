# MenuGen | An Intelligent Generator of Balanced meals

MenuGen is a school project that solves an eternal issue : *What are we going to eat tonight?*

To solve this issue, MenuGen asks you a few questions about your morphology, your food tastes and allergies or diets, before generating well-balanced meals for the next week!

# How does it work?

First, we setup MenuGen:
- Scrape recipes on the internet, storing the ingredients along with the steps to cook it
- Match the ingredients to [OpenFoodFacts](http://fr-en.openfoodfacts.org/) to evaluate the nutritional value of each recipe
- Store these in a `PostGreSQL` database and wait for users

Then, when you want to generate a meal:
- Create an account, entering basic morphological informations that let us calculate your [Basal Metabolic Rate](https://en.wikipedia.org/wiki/Basal_metabolic_rate)
- Match this calorie count to the WHO nutritional recommendations to derive your needs in proteins/carbs/fats
- Run a Genetical Algorithm that will iterate on potential menus based on your tastes and diet to optimize the nutritional value of your meals
- Display the result in a nice dashboard where you can remove dishes, reorder meals, print a shopping list, etc.

# How do I use it?

For now there is no hosted instance of MenuGen. If you want to run it on your machine, follow these steps:

## Configure the development environment

### Python

Install the following packages: `python3 python3-pip`

Then run from the root of the project:

    sudo pip install virtualenv
    virtualenv -p python3 .venv
    source .venv/bin/activate
    pip install -r requirements.txt

To disable the python virtual environment, run `deactivate`

### Front-end

    cd application 

Install Bower + Grunt:

    npm install -g grunt-cli bower

Install Assets:

    npm install && bower install

Compile Assets:

    grunt


### Django

Initialize and configure the development database:

    ./manage.py makemigrations
    ./manage.py migrate

Create your super user:

    ./manage.py createsuperuser

## Run the development server

First check if you're using the virtualenv. If not, run

    source .venv/bin/activate

Then you can run the server with

    ./manage.py runserver

* project root - [http://127.0.0.1:8000](http://127.0.0.1:8000)
* administration interface - [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)

## Migrate your local database

When models are edited, you must compute the necessary migrations from your database state, then migrate with

    ./manage.py makemigrations
    ./manage.py migrate

## Manage data in the database

Load initial data (so far the ingredients):

    ./manage.py loaddata initial_data

Note: initial_data is reloaded every migration

Create a fixture (snapshot from the data currently in the database):

    ./manage.py dumpdata > menus/fixtures/myfixture.json

Load a fixture:

    ./manage.py loaddata myfixture

Fill ingredients directly from the csv:

    ./manage.py fill_db

import datetime
from menus.algorithms.dietetics import Calculator

WEIGHT = 75
HEIGHT = 170
AGE = 20
BIRTHDAY = datetime.datetime.now() - datetime.timedelta(days=365 * AGE)
NAME = 'Sans nom'
SEX = Calculator.SEX_H
EXERCISE = Calculator.EXERCISE_MODERATE
ACTIVITY = 2

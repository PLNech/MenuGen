import datetime
from dateutil.relativedelta import relativedelta

__author__ = 'PLNech'


class Calculator:
    EXERCISE_LOW = 'low'
    EXERCISE_LIGHT = 'light'
    EXERCISE_MODERATE = 'moderate'
    EXERCISE_ACTIVE = 'active'
    EXERCISE_EXTREME = 'extreme'

    NUTRIENT_FATS = 'fats'
    NUTRIENT_PROTEINS = 'proteins'
    NUTRIENT_CARBOHYDRATES = 'carbohydrates'

    SEX_H = 'man'
    SEX_F = 'woman'

    calories_per_gram = {
        NUTRIENT_FATS: 9,
        NUTRIENT_PROTEINS: 4,
        NUTRIENT_CARBOHYDRATES: 4
    }

    exercise_calories_ratio = {
        EXERCISE_LOW: 1.2,
        EXERCISE_LIGHT: 1.375,
        EXERCISE_MODERATE: 1.55,
        EXERCISE_ACTIVE: 1.725,
        EXERCISE_EXTREME: 1.9
    }

    exercise_proteins_ratio = {
        EXERCISE_LOW: 0.8,
        EXERCISE_LIGHT: 1.05,
        EXERCISE_MODERATE: 1.3,
        EXERCISE_ACTIVE: 1.55,
        EXERCISE_EXTREME: 1.8
    }

    sex_handicaps = {
        SEX_H: +5,
        SEX_F: -161
    }

    @staticmethod
    def average_percentage(min_percentage, max_percentage, calories):
        return calories * (min_percentage + max_percentage) / 2

    @staticmethod
    def estimate_needs_profile(profile):
        print('birthday:', profile.birthday)
        age = relativedelta(datetime.date.today(), profile.birthday).years
        return Calculator.estimate_needs(age, profile.height, profile.weight, profile.sex, profile.activity)

    @staticmethod
    def estimate_needs(age, size, weight, sex, exercise):
        """
        Return a DieteticsNeeds object describing the calculated needs

        :type age: int
        :type size: int (cm)
        :type weight: int (kg)
        :type sex: str SEX_H / SEX_F
        :type exercise: float EXERCISE_X
        :rtype: DieteticsNeeds
        """
        print("Calculating objectives for a %i year-old %s of %icm and %ikg, exercising %sly..." %
              (age, sex, size, weight, exercise))

        bmi = 10 * weight + 6.25 * size - 5 * age + Calculator.sex_handicaps[sex]
        calories = bmi * Calculator.exercise_calories_ratio[exercise]

        proteins_g = weight * Calculator.exercise_proteins_ratio[exercise]
        proteins = proteins_g * 4

        carbohydrates = Calculator.average_percentage(0.45, 0.65, calories)
        carbohydrates_g = carbohydrates / Calculator.calories_per_gram[Calculator.NUTRIENT_CARBOHYDRATES]
        fats = Calculator.average_percentage(0.20, 0.35, calories)
        fats_g = fats / Calculator.calories_per_gram[Calculator.NUTRIENT_FATS]

        print("Basal metabolic rate estimated at %.1f kcal/day." % bmi)
        print("Real calorific needs estimated at %.1f kcal/day." % calories)
        print("Proteinic needs estimated at %.1f kcal/day -> %.1f g/day." % (proteins, proteins_g))
        print("Carbohydrates needs estimated at %.1f kcal/day -> %.1f g/day." % (carbohydrates, carbohydrates_g))
        print("Fatty needs estimated at %.1f kcal/day -> %.1f g/day." % (fats, fats_g))

        return DieteticsNeeds(calories, proteins_g, carbohydrates_g, fats_g)

    @staticmethod
    def age_from_date(date):
        today = datetime.date.today()
        return today.year - date.birthday.year - ((today.month, today.day) <
                                                  (date.birthday.month, date.birthday.day))


class DieteticsNeeds:
    # FIXME Use min and max objectives
    def __init__(self, calories, proteins, carbohydrates, fats):
        self.calories = calories
        self.grams_fats = fats
        self.grams_carbohydrates = carbohydrates
        self.grams_proteins = proteins

    def __str__(self):
        return "%d kcal, %d g fats, %d g carbs, %d g proteins" % \
               (self.calories, self.grams_fats, self.grams_carbohydrates, self.grams_proteins)

    def __add__(self, other):
        d = DieteticsNeeds(0, 0, 0, 0)
        d.calories = self.calories + other.calories
        d.grams_fats = self.grams_fats + other.grams_fats
        d.grams_proteins = self.grams_proteins + other.grams_proteins
        d.grams_carbohydrates = self.grams_carbohydrates + other.grams_carbohydrates
        return d

    def __iadd__(self, other):
        self.calories += other.calories
        self.grams_fats += other.grams_fats
        self.grams_proteins += other.grams_proteins
        self.grams_carbohydrates += other.grams_carbohydrates
        return self


if __name__ == "__main__":
    given_age = 18
    given_size_cm = 180
    given_weight_kg = 70
    given_sex = 'woman'
    given_exercise = Calculator.EXERCISE_MODERATE
    Calculator.estimate_needs(given_age, given_size_cm, given_weight_kg, given_sex, given_exercise)

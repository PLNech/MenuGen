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
        :type exercise: str EXERCISE_X
        :rtype: DieteticsNeeds
        """
        print("Calculating objectives for a %d year-old %s of %dcm and %dkg, exercising %sly..." %
              (age, sex, size, weight, exercise))

        bmi = 10 * weight + 6.25 * size - 5 * age + Calculator.sex_handicaps[sex]
        calories = bmi * Calculator.exercise_calories_ratio[exercise]
        needs = DieteticsNeeds(calories)

        print("Basal metabolic rate estimated at %.1f kcal/day." % bmi)
        print("Real calorific needs estimated at %.1f kcal/day." % calories)
        print("Proteinic needs estimated between %.1f and %1.f g/day." % (needs.proteins_min, needs.proteins_max))
        print("Carbohydrates needs estimated between %.1f and %1.f g/day." % (needs.carbs_min, needs.carbs_max))
        print("Fatty needs estimated between %.1f and %1.f g/day." % (needs.fats_min, needs.fats_max))

        return needs

    @staticmethod
    def age_from_date(date):
        today = datetime.date.today()
        return today.year - date.birthday.year - ((today.month, today.day) <
                                                  (date.birthday.month, date.birthday.day))


class DieteticsNeeds:
    RATIO_PROT_MIN = 0.10
    RATIO_PROT_MAX = 0.35
    RATIO_CARB_MIN = 0.45
    RATIO_CARB_MAX = 0.65
    RATIO_FATS_MAX = 0.35
    RATIO_FATS_MIN = 0.20

    def __init__(self, calories):
        grams_per_cal_prot = Calculator.calories_per_gram[Calculator.NUTRIENT_PROTEINS]
        grams_per_cal_carb = Calculator.calories_per_gram[Calculator.NUTRIENT_CARBOHYDRATES]
        grams_per_cal_fats = Calculator.calories_per_gram[Calculator.NUTRIENT_FATS]

        self.calories = calories
        self.proteins_min = self.RATIO_PROT_MIN * calories / grams_per_cal_prot
        self.proteins_max = self.RATIO_PROT_MAX * calories / grams_per_cal_prot
        self.carbs_min = self.RATIO_CARB_MIN * calories / grams_per_cal_carb
        self.carbs_max = self.RATIO_CARB_MAX * calories / grams_per_cal_carb
        self.fats_min = self.RATIO_FATS_MIN * calories / grams_per_cal_fats
        self.fats_max = self.RATIO_FATS_MAX * calories / grams_per_cal_fats

    def __str__(self):
        return "%d kcal, %d-%d g fats, %d-%d g carbs, %d-%d g proteins." % \
               (self.calories, self.proteins_min, self.proteins_max,
                self.carbs_min, self.carbs_max,
                self.fats_min, self.fats_max)

    def __repr__(self):
        return 'DieteticsNeeds: ' + str(self)

    def __add__(self, other):
        d = DieteticsNeeds(0)
        d.calories = self.calories + other.calories
        d.proteins_min = self.proteins_min + other.proteins_min
        d.proteins_max = self.proteins_max + other.proteins_max
        d.carbs_min = self.carbs_min + other.carbs_min
        d.carbs_max = self.carbs_max + other.carbs_max
        d.fats_min = self.fats_min + other.fats_min
        d.fats_max = self.fats_max + other.fats_max
        return d

    def __iadd__(self, other):
        self.calories += other.calories
        self.proteins_min += other.proteins_min
        self.proteins_max += other.proteins_max
        self.carbs_min += other.carbs_min
        self.carbs_max += other.carbs_max
        self.fats_min += other.fats_min
        self.fats_max += other.fats_max
        return self


if __name__ == "__main__":
    given_age = 18
    given_size_cm = 180
    given_weight_kg = 70
    given_sex = 'man'
    given_exercise = Calculator.EXERCISE_MODERATE
    Calculator.estimate_needs(given_age, given_size_cm, given_weight_kg, given_sex, given_exercise)

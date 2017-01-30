import random

import math

from ingredient import Ingredient
from load_data import load_ingredients


class Meal:
    ingredients = []

    def __init__(self, ingredients=None):
        if ingredients:
            self.ingredients = ingredients

    def add_ingredient(self, ingredient):
        self.ingredients.append(ingredient)

    def total_calories(self):
        total_calories = (self.total_protein() * 4) + (self.total_carbohydrate() * 4) + (self.total_fat() * 9)

        return total_calories

    def total_protein(self):
        total_protein = 0
        for ingredient in self.ingredients:
            total_protein += ingredient.get_protein()

        return total_protein

    def total_carbohydrate(self):
        total_carbs = 0
        for ingredient in self.ingredients:
            total_carbs += ingredient.get_carbohydrate()

        return total_carbs

    def total_fat(self):
        total_fat = 0
        for ingredient in self.ingredients:
            total_fat += ingredient.get_fat()

        return total_fat

    def __str__(self):
        out = ''
        for i in ingredients:
            out += i.__str__() + "\n"
        return out

    def fitness(self, carb_ratio=0.333333, fat_ratio=0.33333, protein_ratio=0.33333, req_calories=2500):

        fat_cals = float((self.total_fat() * 9))
        carb_cals = float((self.total_carbohydrate() * 4))
        protein_cals = float((self.total_protein() * 4))

        req_fat_cals = req_calories * fat_ratio
        req_carb_cals = req_calories * carb_ratio
        req_protein_cals = req_calories * protein_ratio

        total_cals = fat_cals + carb_cals + protein_cals

        # fat_score = float(abs(1.0 - (fat_cals / req_fat_cals)))
        # carb_score = float(abs(1.0 - (carb_cals / req_carb_cals)))
        # protein_score =  float(abs(1.0 - (protein_cals / req_protein_cals)))

        fat_score = abs(fat_cals - req_fat_cals) * 1.0
        carb_score = abs(carb_cals - req_carb_cals) * 1.0
        protein_score = abs(protein_cals - req_protein_cals) * 1.0
        cal_score = abs(total_cals - req_calories) * 2.0

        score = 4 * 10000 / (float(fat_score + carb_score + protein_score + cal_score))

        return score


if __name__ == "__main__":
    data = load_ingredients()
    n = 5
    random.shuffle(data)

    p = Ingredient("BEST","cat",2492,208,92,208)
    Meal([p])
    meals = [Meal([p])]

    for i in range(0, 1000, n):
        ingredients = data[i:i + n]
        meals.append(Meal(ingredients))
    print "{}\t{}\t{}\t{}\t{}".format("calories", "carbs", "fats", "protein", "score")
    for meal in meals:
        print "{0}\t{1} ({2:.2f}%)\t{3} ({4:.2f}%)\t{5} ({6:.2f}%)\t{7:.2f}".format(
            meal.total_calories(),
            meal.total_carbohydrate(), float((meal.total_carbohydrate() * 4) / meal.total_calories() * 100),
            meal.total_fat(), float((meal.total_fat() * 9) / meal.total_calories() * 100),
            meal.total_protein(), float((meal.total_protein() * 4) / meal.total_calories() * 100),
            meal.fitness()
        )

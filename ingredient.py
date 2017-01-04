class Ingredient:
    name = 0
    category = 0
    calories = 0
    carbohydrate = 0
    fat = 0
    protein = 0

    def __init__(self, name, category, calories, carbohydrates, fat, protein):
        self.name = name
        self.category = category
        self.calories = calories
        self.carbohydrate = carbohydrates
        self.fat = fat
        self.protein = protein

    def get_calories(self):
        return self.calories

    def get_fat(self):
        return self.fat

    def get_carbohydrate(self):
        return self.carbohydrate

    def get_protein(self):
        return self.protein

    def __str__(self):
        return self.name

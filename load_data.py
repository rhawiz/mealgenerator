from datautils import execute_query
from ingredient import Ingredient


def load_ingredients():
    sql = "SELECT * FROM nutritiondata WHERE category not in ('baby_foods','fats_oils')"
    db_path = "nutritiondata.sqlite"
    data = execute_query(db_path, sql)
    ingredients = []
    columns = data.pop(0)
    for row in data:
        name = row[0]
        category = row[1]
        calories = float(row[3])
        protein = float(row[4])
        carbs = float(row[5])
        fat = float(row[6])

        ing = Ingredient(name, category, calories, protein, carbs, fat)
        ingredients.append(ing)

    return ingredients

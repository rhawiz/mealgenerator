from random import random, randint, choice

import re

from meal import Meal
from load_data import load_ingredients

ingredients = load_ingredients()


class GA:
    def __init__(self, protein_ratio, fat_ratio, carb_ratio, calories):
        self.carb_ratio = carb_ratio
        self.fat_ratio = fat_ratio
        self.protein_ratio = protein_ratio
        self.calories = calories

    def fitness(self, x):

        fat_cals = float((x.total_fat() * 9))
        carb_cals = float((x.total_carbohydrate() * 4))
        protein_cals = float((x.total_protein() * 4))

        req_fat_cals = self.calories * self.fat_ratio
        req_carb_cals = self.calories * self.carb_ratio
        req_protein_cals = self.calories * self.protein_ratio

        total_cals = fat_cals + carb_cals + protein_cals

        # TODO: factor in types of ingredients (e.g. meats, snacks, veg, drinks) as part of the fitness
        # TODO:      e.g. meat + snack + snack + veg > meat + meat + meat + snack
        # categories = []
        # for ing in x.ingredients:
        #     ing.category

        fat_score = abs(fat_cals - req_fat_cals) * 3.0
        carb_score = abs(carb_cals - req_carb_cals) * 3.0
        protein_score = abs(protein_cals - req_protein_cals) * 1.0
        cal_score = abs(total_cals - self.calories) * 2.0

        score = 4 * 10000 / (float(fat_score + carb_score + protein_score + cal_score))

        return score

    def crossover(self, male, female):
        assert isinstance(male, Meal)
        assert isinstance(female, Meal)

        male_genes = [i for i in male.ingredients[:len(male.ingredients) / 2]]
        female_genes = [i for i in female.ingredients[len(female.ingredients) / 2:]]
        child_ingredients = male_genes + female_genes
        child = Meal(ingredients=child_ingredients)

        return child

    def mutate(self, x, mutate):
        for individual in x:
            if mutate > random():
                pos_to_mutate = randint(0, len(individual.ingredients) - 1)
                individual.ingredients[pos_to_mutate] = choice(ingredients)
        return x

    def selection(self, pop, retain, random_select):

        graded = sorted([x for x in pop],
                        key=self.fitness,
                        reverse=True)

        retain_length = int(len(graded) * retain)
        parents = graded[:retain_length]

        # Introduce genetic diversity
        for individual in graded[retain_length:]:
            if random_select > random():
                parents.append(individual)

        return parents

    def evolve(self, pop, retain=0.5, random_select=0.1, mutate=0.05):
        all(isinstance(x, Meal) for x in pop)

        # Selection
        parents = self.selection(pop, retain, random_select)

        # Mutation
        parents = self.mutate(parents, mutate)

        # Crossover
        parents_length = len(parents)
        desired_length = len(pop) - parents_length
        children = []
        while len(children) < desired_length:
            male = randint(0, parents_length - 1)
            female = randint(0, parents_length - 1)
            if male != female:
                male = parents[male]
                female = parents[female]
                child = self.crossover(male, female)
                children.append(child)
        parents.extend(children)
        return parents


def random_subset(iterator, K):
    result = []
    N = 0

    for item in iterator:
        N += 1
        if len(result) < K:
            result.append(item)
        else:
            s = int(random() * N)
            if s < K:
                result[s] = item

    return result


if __name__ == '__main__':
    CARBS = 0.333
    FAT = 0.333
    PROTEIN = 0.333
    CALORIES = 800

    ga = GA(PROTEIN, FAT, CARBS, CALORIES)
    pop = []
    for i in xrange(0, 1000):
        ing = random_subset(ingredients, randint(5, 8))
        pop.append(Meal(ing))

    evolved = ga.evolve(pop)
    for i in range(0, 10):
        print "Gen {}".format(i)
        evolved = ga.evolve(evolved)
    evolved = sorted(evolved, key=ga.fitness, reverse=True)
    for i in evolved:
        print i, "\t", ga.fitness(i)
        ing = re.sub("\n", "\n\t", i.list_ingredients())
        ing = re.sub("^", "\t", ing)
        print ing

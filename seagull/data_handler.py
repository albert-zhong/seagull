import numpy as np
import os

import city
import file_handler
from gradient_descent import GradientDescent

# create a sub-class of GradientDescent that takes multiple y output values (1 for each Big Five trait)


class Models(object):

    TRAITS_TO_INDEX = {'openness': 0, 'conscientiousness': 1, 'extraversion': 2, 'agreeableness': 3, 'neuroticism': 4}

    def __init__(self, X, y, alpha=0.01, iterations=100):
        self.X = X
        self.y = y
        self.models = []
        for i in range(5):
            new_model = GradientDescent(X, y[i], alpha, iterations)
            self.models.append(new_model)

    def predict(self, x):
        predictions = []
        for i in range(5):
            prediction = self.models[i].predict(x)
            predictions.append(prediction)
        return predictions

    def train_model(self, trait):
        index = self.TRAITS_TO_INDEX[trait]
        self.models[index].learn()

    def train_all_models(self):
        for i in range(5):
            self.models[i].learn()

    def show_thetas(self):
        for i in range(5):
            print(self.models[i].theta)


def create_models():
    data_folder = os.path.join(os.getcwd(), os.pardir, "data")
    csv_paths = [file for file in os.listdir(data_folder) if os.path.isfile(os.path.join(data_folder, file))]
    city_objects = city.create_cities(*[path[:-4] for path in csv_paths])

    # creating the training set of input values
    # each row will represent a city; the first value will be 1, followed by word frequencies
    # all words and their order must match up for each city
    # for some reason x = [[1]] * len(city_objects) doesn't work, all rows end up being the same
    # x = [[1]] * len(city_objects) probably make all values point to the same array

    x = []
    for i in range(len(city_objects)):
        x.append([1])

    # this will also create the array of y (output values); each row represents a different OCEAN trait
    y = []
    for i in range(5):
        y.append([])

    all_dictionaries = {}  # creates a dictionary; keys are city names, values are their word frequency dictionaries
    for city_object in city_objects:
        all_dictionaries[city_object.city_name] = file_handler.convert_csv_to_dictionary(city_object)
        city_traits = city_object.get_traits()
        for i in range(5):
            y[i].append(city_traits[i])

    all_words = []  # creates a list of all words found in all dictionaries; afterwards this will become a set
    for dictionary in all_dictionaries:
        all_words += all_dictionaries[dictionary].keys()
    all_words = set(all_words)
    city_names = [city_object.city_name for city_object in city_objects]

    for word in all_words:
        for i, city_name in enumerate(city_names):
            if word in all_dictionaries[city_name]:
                x[i].append(all_dictionaries[city_name][word])
            else:
                x[i].append(0)

    return Models(np.array(x), np.array(y))


models = create_models()
models.train_all_models()
models.show_thetas()

import numpy as np
import os

import city
import file_handler
from gradient_descent import GradientDescent


class Model(GradientDescent):
    pass


def create_model():
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

    all_dictionaries = {}  # creates a dictionary; keys are city names, values are their word frequency dictionaries
    for city_object in city_objects:
        all_dictionaries[city_object.city_name] = file_handler.convert_csv_to_dictionary(city_object)

    all_words = []  # creates a list of all words found in all dictionaries; afterwards this will become a set
    for dictionary in all_dictionaries:
        all_words += all_dictionaries[dictionary].keys()
    all_words = set(all_words)
    city_names = [city_object.city_name for city_object in city_objects]

    for word in all_words:
        for i, city_name in enumerate(city_names):
            print("check " + word + " in " + city_name)
            if word in all_dictionaries[city_name]:
                x[i].append(all_dictionaries[city_name][word])
            else:
                x[i].append(0)

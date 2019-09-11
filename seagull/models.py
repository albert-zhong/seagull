import numpy as np

from data_handler import combine_dictionaries
from gradient_descent import GradientDescent


class Model(GradientDescent):

    def __init__(self, dictionaries, traits):
        x_array = [[1] for i in range(len(dictionaries))]

        self.word_order = []
        all_words = set()
        for dictionary in dictionaries:
            for word in dictionary.keys():
                if word not in all_words:
                    self.word_order.append(word)
                    all_words.add(word)

        for word in all_words:
            for i, dictionary in enumerate(dictionaries):
                x_array[i].append(dictionary.get(word, 0))

        super().__init__(X=np.array(x_array), y=np.array(traits))

    def predict(self, location):
        dictionary = combine_dictionaries(location.get_dictionary_from_csv_file(), location.get_dictionary_from_sql())
        x_array = [1]
        for word in self.word_order:
            x_array.append(dictionary.get(word, 0))
        return np.dot(self.theta, np.array(x_array))


def create_model_from_locations(locations, trait):
    all_dictionaries = []
    all_traits = []
    for location in locations:
        dictionary = combine_dictionaries(location.get_dictionary_from_csv_file(), location.get_dictionary_from_sql())
        all_dictionaries.append(dictionary)
        all_traits.append(location.traits[trait])

    return Model(all_dictionaries, all_traits)

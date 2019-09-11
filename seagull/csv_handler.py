import csv
from os import path

from data_handler import combine_dictionaries


# Takes a path to a .csv file, returns a dictionary of word -> frequency pairs
def csv_to_dictionary(csv_path):
    dictionary = {}

    if not path.exists(csv_path):
        return dictionary

    with open(csv_path, 'r') as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # skips header
        for word, frequency in reader:
            dictionary[word] = int(frequency)

    return dictionary


# Takes a dictionary, combines it with a dictionary in a .csv file, and writes a new combined dictionary to that .csv
def dictionary_to_csv(dictionary, csv_path):
    file_dictionary = csv_to_dictionary(csv_path)  # gets the dictionary currently on the .csv file
    new_dictionary = combine_dictionaries(dictionary, file_dictionary)

    with open(csv_path, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['word', 'frequency'])  # creates header
        for word, frequency in new_dictionary.items():
            writer.writerow([word, frequency])

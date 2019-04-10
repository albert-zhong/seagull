import csv
import re

import city


def parse_text_to_list(text):
    text = text.lower()

    text = re.sub(r"http\S+", "", text)  # Removes links
    text = re.sub(r"@\S+", "", text)  # Removes @user

    pattern = re.compile('([^\s\w]|_)+', re.UNICODE)  # Removes everything but spaces and alphanumeric chars
    text = pattern.sub('', text)

    words = text.split()

    return words


def create_csv_from_dictionary(dictionary, city_object):
    csv_path = city_object.path

    with open(csv_path, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(["word", "frequency"])
        for word in dictionary:
            writer.writerow([word, dictionary[word]])

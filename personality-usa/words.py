from collections import Counter
import operator
import csv
import re
import os

import city


def parse_text_to_list(text):
    text = text.lower()

    text = re.sub(r"http\S+", "", text)  # Removes links
    text = re.sub(r"@\S+", "", text)  # Removes @user

    pattern = re.compile('([^\s\w]|_)+', re.UNICODE)  # Removes everything but spaces and alphanumeric chars
    text = pattern.sub('', text)

    words = text.split()

    return words


def dictionary_to_csv(dictionary, path):
    csv_path = path

    file_exists = os.path.isfile(csv_path)  # Checks if CSV file already exists

    if file_exists:  # If the file already exists, just update the CSV
        current_dictionary = Counter(convert_csv_to_dictionary(csv_path))
        new_dictionary = Counter(dictionary)

        combined_dictionary = current_dictionary + new_dictionary
        convert_dictionary_to_csv(combined_dictionary, path)
    else:  # If the file doesn't exist yet, create a new CSV
        convert_dictionary_to_csv(dictionary, csv_path)


def convert_dictionary_to_csv(dictionary, csv_path):
    with open(csv_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["word", "frequency"])  # Create header

        for word, frequency in dictionary.items():
            writer.writerow([word, frequency])


def convert_csv_to_dictionary(csv_path):
    my_dict = {}

    with open(csv_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skips header

        for word, str_frequency in reader:
            my_dict[word] = int(str_frequency)  # Casts string frequencies to integer values

    return my_dict


def sort_dictionary(dictionary):
    sorted_list = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_list


def sort_csv(csv_path):
    my_dict = convert_csv_to_dictionary(csv_path)
    sorted_list = sort_dictionary(my_dict)

    with open(csv_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["word", "frequency"])  # Create header

        for word, frequency in sorted_list:
            writer.writerow([word, frequency])

    print("Done sorting!")


def create_relative_frequency_csv(csv_path):
    # Get total word count
    my_dict = convert_csv_to_dictionary(csv_path)
    total_word_count = 0
    for word_count in my_dict.values():
        total_word_count += word_count

    # Convert to sorted list so frequencies will be displayed in order
    sorted_list = sort_dictionary(my_dict)

    new_csv_path = csv_path[:-4] + "_rf" + ".csv"  # Removes ".csv" from old path, adds "_rf", then adds ".csv" again

    with open(new_csv_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["word", "relative_frequency"])  # Create header

        for word, absolute_frequency in sorted_list:
            writer.writerow([word, absolute_frequency/total_word_count])

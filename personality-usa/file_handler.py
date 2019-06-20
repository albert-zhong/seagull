from collections import Counter
import operator
import csv
import re


# This method takes some string, filters it, and returns a list of strings
def parse(text):
    text = text.lower()  # turns to lowercase
    text = re.sub(r"http\S+", "", text)  # Removes links
    text = re.sub(r"@\S+", "", text)  # Removes @user

    pattern = re.compile('([^\s\w]|_)+', re.UNICODE)  # Removes everything but spaces and alphanumeric chars
    text = pattern.sub('', text)
    words = text.split()

    return words


# Method to take any dictionary object and add it to any csv, use this
def dictionary_to_csv(city, dictionary):

    if city.file_exists():  # If the file already exists, combine current and new dictionary
        current_dictionary = Counter(convert_csv_to_dictionary(city))
        new_dictionary = Counter(dictionary)
        combined_dictionary = current_dictionary + new_dictionary
        convert_dictionary_to_new_csv(city, combined_dictionary)

    else:  # If the file doesn't exist yet, create a new CSV
        convert_dictionary_to_new_csv(city, dictionary)


# Internal method to convert a dictionary to a new CSV file, do not touch this
def convert_dictionary_to_new_csv(city, dictionary):
    csv_file_path = city.get_path()

    with open(csv_file_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["word", "frequency"])  # Create header

        for word, frequency in dictionary.items():
            writer.writerow([word, frequency])


# Internal method to convert a CSV file to a dictionary object, do not touch this
def convert_csv_to_dictionary(city):
    if not city.file_exists():
        raise Exception("%s.csv not found" % city.city_name)

    my_dict = {}
    csv_file_path = city.get_path()

    with open(csv_file_path, "r") as csv_file:
        reader = csv.reader(csv_file)
        next(reader)  # Skips header

        for word, str_frequency in reader:
            my_dict[word] = int(str_frequency)  # Casts string frequencies to integer values

    return my_dict


# This internal method takes a dictionary object, sorts it by descending frequency, and returns a list
def sort_dictionary(dictionary):
    sorted_list = sorted(dictionary.items(), key=operator.itemgetter(1), reverse=True)
    return sorted_list


# This method takes any City object and sorts its CSV file
def sort_csv(city):
    csv_file_path = city.get_path()
    current_dictionary = convert_csv_to_dictionary(csv_file_path)
    sorted_list = sort_dictionary(current_dictionary)

    with open(csv_file_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["word", "frequency"])  # Create header

        for word, frequency in sorted_list:
            writer.writerow([word, frequency])

    print("Done sorting!")


def create_relative_frequency_csv(city):
    csv_file_path = city.get_path()

    # Get total word count
    my_dict = convert_csv_to_dictionary(csv_file_path)
    total_word_count = 0
    for word_count in my_dict.values():
        total_word_count += word_count

    # Convert to sorted list so frequencies will be displayed in order
    sorted_list = sort_dictionary(my_dict)

    # Removes ".csv" from old path, adds "_rf", then adds ".csv" again
    new_csv_path = csv_file_path[:-4] + "_rf" + ".csv"

    with open(new_csv_path, "w", newline="") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["word", "relative_frequency"])  # Create header

        for word, absolute_frequency in sorted_list:
            writer.writerow([word, absolute_frequency / total_word_count])

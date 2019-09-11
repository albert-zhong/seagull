import re


# Takes some status text and returns a list of lowercase alphabetic words
def parse(text):
    text = text.lower()  # to lowercase
    text = re.sub(r"http\S+", "", text)  # removes links
    text = re.sub(r"@\S+", "", text)  # removes @user

    pattern = re.compile('([^\s\w]|_)+', re.UNICODE)  # regex pattern strips non-alphanumeric chars
    text = pattern.sub('', text)  # replaces non-alphanumeric chars with empty string
    words = text.split()  # splits string into a list of strings along spaces

    return words


# Takes two dictionaries, combines frequencies, returns a new dictionary
def combine_dictionaries(dict1, dict2):
    if len(dict1) > len(dict2):
        small_dictionary = dict2
        big_dictionary = dict1
    else:
        small_dictionary = dict2
        big_dictionary = dict1

    for word, frequency in small_dictionary.items():
        big_dictionary[word] = big_dictionary.get(word, 0) + frequency

    return big_dictionary

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

import csv
import os


class City (object):
    def __init__(self, path, city, state, geo_box, extraversion, neuroticism, agreeableness, conscientiousness, openness):
        self.path = path
        self.city = city
        self.state = state
        self.geo_box = geo_box
        self.e = extraversion
        self.n = neuroticism
        self.a = agreeableness
        self.c = conscientiousness
        self.o = openness
        self.path = path

    def __str__(self):
        return self.city + ", " + self.state + "\n" + str(self.geo_box) + \
               "\n" + "Extraversion: " + self.e + "\nNeuroticism: " + self.n + "\nAgreeableness: " + self.a + \
               "\nConscientiousness: " + self.c + "\nOpenness: " + self.o


def create_city_from_csv(csv_file_path, specific_city=None):
    cities = []  # Set of all City objects

    with open(csv_file_path, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)  # Skips the header, which is the first line
        for row in csv_reader:
            city = row[0]
            state = row[1]
            geo_box = [row[2], row[3], row[4], row[5]]
            extraversion = row[6]
            neuroticism = row[7]
            agreeableness = row[8]
            conscientiousness = row[9]
            openness = row[10]
            path = get_output_path(city)

            city_object = City(path, city, state, geo_box, extraversion, neuroticism,
                               agreeableness, conscientiousness, openness)
            cities.append(city_object)

    if specific_city is not None:  # Return a specific city if it was requested
        for c in cities:
            if c.city == specific_city:
                return c
    else:
        return cities


def get_output_path(city):
    here = os.getcwd()
    data_folder = "data"
    file_name = city + ".csv"
    file_path = os.path.join(here, os.pardir, data_folder, file_name)
    return file_path

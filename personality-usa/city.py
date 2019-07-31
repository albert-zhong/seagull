import csv
import os

from tweepy import Stream
from tweepy import OAuthHandler

from geostreaming import GeoListener, AsynchronousGeoListener
import codes


class City(object):
    def __init__(self, city_name, state, geo_box,
                 extraversion, neuroticism, agreeableness, conscientiousness, openness,):
        self.city_name = city_name
        self.state = state
        self.geo_box = geo_box
        self.extraversion = extraversion
        self.neuroticism = neuroticism
        self.agreeableness = agreeableness
        self.conscientiousness = conscientiousness
        self.openness = openness

    def __str__(self):
        return "%s, %s\n" % (self.city_name, self.state) + \
               "%s\n" % (str(self.geo_box)) + \
               "extraversion = %g\n" % self.extraversion + \
               "neuroticism = %g\n" % self.neuroticism + \
               "agreeableness = %g\n" % self.agreeableness + \
               "conscientiousness = %g\n" % self.conscientiousness + \
               "openness = %g\n" % self.openness + \
               "path = %s\n" % self.get_path()

    def get_path(self):
        here = os.getcwd()
        data_folder = "data"
        file_name = self.city_name + ".csv"
        file_path = os.path.join(here, os.pardir, data_folder, file_name)  # os.pardir is parent directory
        return file_path

    def file_exists(self):
        return os.path.exists(self.get_path()) and os.path.getsize(self.get_path()) > 0

    # IMPORTANT METHOD: Creates Twitter stream by authenticating with tweepy
    def create_steam(self, asynchronous=False):
        # Create Twitter stream
        auth = OAuthHandler(codes.consumer_key, codes.consumer_secret)
        auth.set_access_token(codes.access_token, codes.access_secret)

        # Create StreamListener
        if asynchronous:
            my_listener = AsynchronousGeoListener(self)
        else:
            my_listener = GeoListener(self)
        my_stream = Stream(auth, my_listener)

        my_stream.filter(languages=["en"], locations=self.geo_box)


DEFAULT_TEMPLATE_PATH = os.path.join(os.getcwd(), os.pardir, "templates", "cities_template.csv")


# This method looks through cities_template.csv to return a City object given a requested city_name
def create_city(city_name):
    with open(DEFAULT_TEMPLATE_PATH, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)  # Skips the header, which is the first line

        for row in csv_reader:
            if row[0] == city_name.lower():  # found specified city name in cities_template.csv
                return create_city_from_row(row)

    raise Exception("%s not found in %s" % (city_name, DEFAULT_TEMPLATE_PATH))


# This method looks through cities_template.csv to return a list of City objects given multiple city_names
def create_cities(*city_names):
    city_objects = []
    requested_cities = set([city_name.lower() for city_name in city_names])

    with open(DEFAULT_TEMPLATE_PATH, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)  # Skips the header, which is the first line

        for row in csv_reader:
            if row[0] in requested_cities:  # found a specified city name in cities_template.csv
                city_objects.append(create_city_from_row(row))

    return city_objects


# This method creates a list of ALL City objects given cities_template.csv
def create_all_cities():
    city_objects = []

    with open(DEFAULT_TEMPLATE_PATH, "r") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=",")
        next(csv_reader)  # Skips the header, which is the first line

        for row in csv_reader:
            city_objects.append(create_city_from_row(row))

    return city_objects


# Given a row from cities_template.csv, this method returns a City object
def create_city_from_row(row):
    city_name = row[0]
    state = row[1]
    geo_box = [float(row[i]) for i in range(2, 6)]  # creates list of geo_box coord integers
    extraversion = float(row[6])
    neuroticism = float(row[7])
    agreeableness = float(row[8])
    conscientiousness = float(row[9])
    openness = float(row[10])

    city_object = City(city_name, state, geo_box,
                       extraversion, neuroticism, agreeableness, conscientiousness, openness)
    return city_object

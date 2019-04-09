from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import re
import os
import csv

import codes


class GeoListener(StreamListener):

    def __init__(self, city_object, api=None):
        super().__init__(api=None)
        self.city_object = city_object
        self.counter = 0

    def on_status(self, status):
        text = status.text
        print(parse_text_to_list(text))

    def on_error(self, status_code):
        print("Encountered error with status code: " + status_code)
        if status_code == 420:  # Too many failed connections in a window of time
            return False  # Kill stream
        return True  # By default don't kill the stream

    def on_timeout(self):
        print("Timeout...")
        return True  # Don't kill the stream


def parse_text_to_list(text):
    text = text.lower()

    text = re.sub(r"http\S+", "", text)  # Removes links
    text = re.sub(r"@\S+", "", text)  # Removes @user

    pattern = re.compile('([^\s\w]|_)+', re.UNICODE)  # Removes everything but spaces and alphanumeric chars
    text = pattern.sub('', text)

    words = text.split()

    return words


def create_stream(city):

    # Create Twitter stream
    auth = OAuthHandler(codes.consumer_key, codes.consumer_secret)
    auth.set_access_token(codes.access_token, codes.access_secret)

    # Create StreamListener
    my_listener = GeoListener(city)
    my_stream = Stream(auth, my_listener)

    my_stream.filter(languages=["en"], locations=city.geo_box)

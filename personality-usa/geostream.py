from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

from collections import defaultdict

import file_handler
import codes


class GeoListener(StreamListener):

    def __init__(self, city_object, api=None):
        super().__init__(api=None)
        self.city_object = city_object
        self.counter = 0
        self.dictionary = {}  # Dictionary of words; keys are words, values are frequency

    def on_connect(self):
        print(">> Connected to Twitter stream!")

    def on_status(self, status):

        # Update counter and print to console
        self.counter += 1
        print(str(self.counter) + " tweets processed")

        # Parse text into a list of all words
        text = status.text
        word_list = file_handler.parse_text_to_list(text)

        # Add word counts to local dictionary variable
        for word in word_list:
            self.dictionary[word] = self.dictionary.setdefault(word, 0) + 1

        # Writes dictionary to CSV file every 10 tweets
        if self.counter % 100 == 0:
            print(">> Saving to CSV file!")
            file_handler.dictionary_to_csv(self.dictionary, self.city_object.path)

    def on_error(self, status_code):
        print("Encountered error with status code: " + status_code)
        if status_code == 420:  # Too many failed connections in a window of time
            return False  # Kill stream
        return True  # By default don't kill the stream

    def on_timeout(self):
        print("Timeout...")
        return True  # Don't kill the stream


def create_stream(city):

    # Create Twitter stream
    auth = OAuthHandler(codes.consumer_key, codes.consumer_secret)
    auth.set_access_token(codes.access_token, codes.access_secret)

    # Create StreamListener
    my_listener = GeoListener(city)
    my_stream = Stream(auth, my_listener)

    my_stream.filter(languages=["en"], locations=city.geo_box)

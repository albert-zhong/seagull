from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener

import os
import csv

import codes


class GeoListener(StreamListener):

    def __init__(self, path, api=None):
        super().__init__(api=None)
        self.path = path
        self.counter = 0

    def on_status(self, status):
        print(status)

    def on_error(self, status_code):
        print("Encountered error with status code: " + status_code)
        if status_code == 420:  # Too many failed connections in a window of time
            return False  # Kill stream
        return True  # By default don't kill the stream

    def on_timeout(self):
        print("Timeout...")
        return True  # Don't kill the stream

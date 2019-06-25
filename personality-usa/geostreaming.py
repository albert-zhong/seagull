from tweepy.streaming import StreamListener

import file_handler


class GeoListener(StreamListener):

    TWEETS_PER_SAVE = 2

    def __init__(self, city_object, api=None):  # Don't touch this
        super().__init__(api=None)
        self.city_object = city_object
        self.counter = 0
        self.dictionary = {}  # Dictionary of words; keys are words, values are frequency

    def on_connect(self):
        print(">> Connected to Twitter stream!")

    def on_status(self, status):

        # Update counter and print to console
        self.counter += 1
        print("%d tweets processed" % self.counter)

        # Parse text into a list of all words
        text = status.text
        word_list = file_handler.parse(text)

        # Add word counts to local dictionary variable
        for word in word_list:
            self.dictionary[word] = self.dictionary.setdefault(word, 0) + 1

        # Writes dictionary to CSV file every 100 tweets
        if self.counter % self.TWEETS_PER_SAVE == 0:
            print(">> Saving to CSV file!")
            file_handler.dictionary_to_csv(self.city_object, self.dictionary)

    def on_error(self, status_code):
        print("Encountered error with status code: %d" % status_code)
        if status_code == 420:  # Too many failed connections in a window of time
            return False  # Kill stream
        return True  # By default don't kill the stream

    def on_timeout(self):
        print("Timeout...")
        return True  # Don't kill the stream


class AsynchronousGeoListener(GeoListener):
    def on_status(self, status):
        # Update counter and print to console
        self.counter += 1
        print("%d tweets processed for %s" % (self.counter, self.city_object.city_name))

        # Parse text into a list of all words
        text = status.text
        word_list = file_handler.parse(text)

        # Add word counts to local dictionary variable
        for word in word_list:
            self.dictionary[word] = self.dictionary.setdefault(word, 0) + 1

        # Writes dictionary to CSV file once 100 tweets is reached, then exits
        if self.counter == self.TWEETS_PER_SAVE:
            print(">> Saving %s to CSV file!" % self.city_object.city_name)
            file_handler.dictionary_to_csv(self.city_object, self.dictionary)
            return False

from tweepy.streaming import StreamListener
from tweepy import Stream
from tweepy import OAuthHandler

from csv_handler import dictionary_to_csv as csv_save
from data_handler import parse


class GeoStream:
    def __init__(self, consumer_key, consumer_secret, access_token, access_secret,
                 location, use_sql=False):

        # Twitter API authentication
        self.consumer_key = consumer_key
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret = access_secret

        self.location = location

        if use_sql and not self.location.database:
            raise Exception('Requires a MySQL database if use_sql=True')
        elif not use_sql and not self.location.csv_path:
            raise Exception('Requires a file output path if use_sql=False')

        self.use_sql = use_sql

    def start(self, limit_tweets=100):
        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_secret)

        if not self.use_sql:
            my_listener = CSVGeoListener(csv_path=self.location.csv_path, limit_tweets=limit_tweets)
        else:
            my_listener = SQLGeoListener(database=self.location.database,
                                         table_name=self.location.name,
                                         limit_tweets=limit_tweets
                                         )

        my_stream = Stream(auth, my_listener)
        my_stream.filter(locations=self.location.geo_box)


class CSVGeoListener(StreamListener):
    def __init__(self, csv_path, limit_tweets, api=None):
        super().__init__(api=None)
        self.csv_path = csv_path
        self.limit_tweets = limit_tweets
        self.counter = 0
        self.dictionary = {}

    def on_connect(self):
        print(f"Connected! Outputting tweets to {self.csv_path}")

    def on_status(self, status):
        self.counter += 1
        print(f"Tweets processed: {self.counter}")

        for word in parse(status.text):
            self.dictionary[word] = self.dictionary.get(word, 0) + 1

        if self.counter == self.limit_tweets:
            csv_save(self.dictionary, self.csv_path)
            return False

    def on_error(self, status_code):
        csv_save(self.dictionary, self.csv_path)
        print(f"Encountered error with status code {status_code}")
        if status_code == 420:  # Too many failed connections in a window of time
            return False
        return True

    def on_timeout(self):
        csv_save(self.dictionary, self.csv_path)
        print("Timeout...")
        return True


class SQLGeoListener(StreamListener):
    def __init__(self, database, table_name, limit_tweets, api=None):
        super().__init__(api=None)
        self.database = database
        self.table_name = table_name
        self.limit_tweets = limit_tweets
        self.counter = 0
        self.dictionary = {}

    def on_connect(self):
        print(f"Connected! Outputting tweets to {self.database}")

    def on_status(self, status):
        self.counter += 1
        print(f"Tweets processed: {self.counter}")

        for word in parse(status.text):
            if len(word) < 16:
                self.dictionary[word] = self.dictionary.get(word, 0) + 1

        if self.counter == self.limit_tweets:
            self.database.dictionary_to_sql(self.dictionary, self.table_name)
            return False

    def on_error(self, status_code):
        self.database.dictionary_to_sql(self.dictionary, self.table_name)
        print(f"Encountered error with status code {status_code}")
        if status_code == 420:  # Too many failed connections in a window of time
            return False
        return True

    def on_timeout(self):
        self.database.dictionary_to_sql(self.dictionary, self.table_name)
        print("Timeout...")
        return True

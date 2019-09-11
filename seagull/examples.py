from geostreaming import GeoStream
from locations import get_preset_location
from sql_handler import Database

my_database = Database(
    host='127.0.0.1',
    user='albert',
    password='root',
    db_name='tweets',
)

consumer_key = "consumer key here"
consumer_secret = "consumer secret here"
access_token = "access token here"
access_secret = "access secret here"

nyc = get_preset_location('NEW_YORK')
my_geostream = GeoStream(consumer_key, consumer_secret, access_token, access_secret, nyc, database=my_database)
my_geostream.start(limit_tweets=10)

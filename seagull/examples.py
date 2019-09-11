from geostreaming import GeoStream
from locations import get_preset_location
from models import create_model_from_locations
from sql_handler import Database


my_db = Database(
    host='localhost',
    user='albert',
    password='root',
    db_name='tweets'
)

consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""

nyc = get_preset_location('NEW_YORK', csv_path='../csv/nyc.csv')
my_geostream = GeoStream(consumer_key, consumer_secret, access_token, access_secret, nyc)
my_geostream.start(limit_tweets=5)

my_model = create_model_from_locations([nyc], trait='openness')
my_model.train()
print(my_model.predict(location=nyc))

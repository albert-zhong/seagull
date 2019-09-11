# seagull
linear regression model predicting a U.S city's Big Five personality traits based on its public tweets

## Usage: examples.py
```python
# Import all
from geostreaming import GeoStream
from locations import get_preset_location
from models import create_model_from_locations
from sql_handler import Database


# Create a database object and enter in names for host, user, password, and a database to create tables in
my_db = Database(
    host='localhost',
    user='albert',
    password='root',
    db_name='tweets'
)

# Add your Twitter API codes
consumer_key = ""
consumer_secret = ""
access_token = ""
access_secret = ""

# Creates a Location object from a preset location (I picked New York).
# You can manually create a Location object or find a list of preset locations in locations.py.
# You must specify at least database=[Database object] or csv_path=[../path/to/file.csv]
nyc = get_preset_location('NEW_YORK', database=my_db, csv_path='../csv/nyc.csv')

# Creates a GeoStream object based on your API codes, Location object, and desired output system.
# By default, use_sql is set to False. Set it to True if you want to output to your MySQL server.
my_geostream = GeoStream(consumer_key, consumer_secret, access_token, access_secret, nyc, use_sql=True)

# Start the stream and a set a limit to how many tweets it will process before it stops.
my_geostream.start(limit_tweets=1)

# Create a gradient descent algorithm from some locations, and select the trait you want as the y-variable output
# In this case, x-variables are the word frequencies and y-variables are OCEAN trait.
# For example, if we had a dictionary of {'hello': 5, 'world': 2, 'python': 10} for New York and an extraversion of
# 0.05, the matrix would look like this:
# x = [[1 5 2 10]]
# y = [0.05]
# If Seattle had a dictionary of {'hello': 10, 'coffee': 7} and an extraversion of -0.04, the training data would be:
# x = [[1 5 2 10 0], [1 10 0 0 7]]
# y = [0.05, -0.04]
# If a location doesn't have any frequency for a word that another location does have, then it will simply be 0.
# Each row represents a new location.

my_model = create_model_from_locations([nyc], trait='openness')

# Trains the model
my_model.train()

# Prints the theta values for a prediction based on an input row of x-variable values
print(my_model.predict(location=nyc))
```

from csv_handler import csv_to_dictionary


class Location:
    def __init__(self, name, geo_box, traits=None, csv_path=None, database=None):
        if not csv_path and not database:
            raise Exception('Needs at least a csv_path output or a database')

        self.name = name
        self.geo_box = geo_box
        self.traits = traits
        self.traits = {
            'extraversion': traits[0],
            'neuroticism': traits[1],
            'agreeableness': traits[2],
            'conscientiousness': traits[3],
            'openness': traits[4],
        }

        self.csv_path = csv_path
        self.database = database

    def get_dictionary_from_csv_file(self):
        if self.csv_path:
            return csv_to_dictionary(self.csv_path)
        return {}

    def get_dictionary_from_sql(self):
        if self.database:
            return self.database.sql_to_dictionary()
        return {}


def get_preset_location(name, csv_path=None, database=None):
    if name not in CITIES:
        raise Exception(f"{name} not found in preset locations list")

    return Location(name=name, geo_box=CITIES[name][0], traits=CITIES[name][1], csv_path=csv_path, database=database)


CITIES = {
    'NEW_YORK': [[-74.25909, 40.477399, -73.700181, 40.916178], [0.05, -0.04, -0.17, -0.03, 0.15]],
    'LOS_ANGELES': [[-118.562114, 33.951176, -118.187084, 34.16603], [0.09, -0.12, -0.06, -0.06, 0.17]],
    'CHICAGO': [[-87.940101, 41.643919, -87.523984, 42.023022], [0.12, -0.1, -0.11, 0.05, 0.14]],
    'HOUSTON': [[-95.909742, 29.53707, -95.012053, 30.110351], [0.04, -0.08, -0.04, -0.01, 0.03]],
    'PHOENIX': [[-112.399186, 33.209328, -111.665849, 33.701999], [-0.01, -0.03, 0.02, 0.0, 0.03]],
    'SEATTLE': [[-122.459696, 47.481002, -122.224433, 47.734136], [-0.04, 0.0, 0.0, -0.07, 0.16]],
    'PORTLAND': [[-122.836749, 45.432536, -122.472025, 45.652881], [-0.05, -0.02, 0.04, -0.0, 0.1]],
    'SAN_FRANCISCO': [[-122.524687, 37.72869, -122.356545, 37.815604], [0.05, -0.05, -0.04, -0.11, 0.15]],
    'DETROIT': [[-83.287959, 42.255192, -82.910439, 42.450232], [0.13, -0.13, -0.18, 0.09, 0.06]],
    'PHILADELPHIA': [[-75.280298, 39.867005, -74.955831, 40.137959], [0.03, -0.02, -0.15, 0.03, 0.12]],
    'WASHINGTON_DC': [[-77.119766, 38.79163, -76.909366, 38.995852], [0.1, -0.18, -0.13, 0.07, 0.12]],
    'MIAMI': [[-80.31976, 25.709052, -80.139157, 25.855783], [0.15, -0.15, -0.07, 0.01,0.19]],
    'ATLANTA': [[-84.5511, 33.6478, -84.2896, 33.8868], [0.13, -0.16, -0.09, 0.05, 0.11]],
    'NEW_ORLEANS': [[-90.14003, 29.865481, -89.625176, 30.199469], [0.15, -0.11, -0.05, 0.05, 0.18]],
    'BIRMINGHAM': [[-87.085831, 33.360474, -86.570977, 33.682093], [0.08, -0.07, 0.01, 0.05, 0.08]],
    'DALLAS': [[-97.102244, 32.585664, -96.582952, 33.010338], [0.08, -0.07, -0.02, -0.01, 0.09]],
}

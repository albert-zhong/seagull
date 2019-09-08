import city as c


def main():
    collect_stream("san_francisco")


def collect_all_streams():
    all_cities_objects = c.create_all_cities()
    for city_object in all_cities_objects:
        city_object.create_steam(asynchronous=True)


def collect_stream(city_name):
    city_object = c.create_city(city_name)
    city_object.create_steam()


if __name__ == "__main__":
    main()

import geostream
import city


def main():
    la_city = city.create_city_from_csv("../data/cities.csv", "la")
    geostream.create_stream(la_city)


if __name__ == "__main__":
    main()

import geostream
import city
import words

# seattle = city.create_city_from_csv("../data/cities.csv", "seattle")
# geostream.create_stream(seattle)


def main():
    words.create_relative_frequency_csv("../data/seattle.csv")


if __name__ == "__main__":
    main()

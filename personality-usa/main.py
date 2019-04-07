import city


def main():
    nyc = city.create_city_from_csv("../data/cities.csv", "la")
    print(nyc)


if __name__ == "__main__":
    main()

import city


def main():
    my_cities = city.create_city_from_csv("../data/cities.csv")
    for c in my_cities:
        print(c)


if __name__ == "__main__":
    main()

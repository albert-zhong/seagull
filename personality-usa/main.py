import geostreaming as gs
import city as c
import file_handler


def main():
    new_york_city = c.create_city("nyc")
    new_york_city.create_steam()


if __name__ == "__main__":
    main()

import geostreaming as gs
import city as c
import file_handler


def main():
    seattle = c.create_city("Seattle")
    print(seattle.file_exists())


if __name__ == "__main__":
    main()

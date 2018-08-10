from pymongo import MongoClient
from csv_to_json_cities import process_file

DATAFILE = "../Data/cities.csv"


def insert_cities(infile, db):
    data = process_file(infile)
    db.cities.insert(data)


if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    insert_cities(DATAFILE, db)
    print (db.cities.find_one())

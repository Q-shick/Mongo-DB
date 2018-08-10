from pymongo import MongoClient
from csv_to_json_autos import process_file

DATAFILE = "../Data/autos_full.csv"


def insert_autos(infile, db):
    data = process_file(infile)
    db.autos.insert(data)


if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    insert_autos(DATAFILE, db)
    print (db.autos.find_one())

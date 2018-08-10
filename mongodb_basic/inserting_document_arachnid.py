from pymongo import MongoClient
from csv_to_json_arachnid import process_file

DATAFILE = "../Data/arachnid.csv"


def insert_arachnid(infile, db):
    data = process_file(infile)
    db.arachnid.insert(data)


if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017")
    db = client.examples

    insert_arachnid(DATAFILE, db)
    print (db.arachnid.find_one())

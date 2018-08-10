from pymongo import MongoClient
import json
from pprint import pprint

DATAFILE = "../Data/twitter.json"


if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017")
    db = client.twitter
    # read json file
    json_data = []
    for line in open(DATAFILE, 'r', encoding = "utf8"):
        json_data.append(json.loads(line))
    # insert bson to mongodb
    db.tweets.insert(json_data)
    pprint (db.tweets.find_one())

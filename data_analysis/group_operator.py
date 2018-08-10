from pymongo import MongoClient
from pprint import pprint


def get_db(db_name):
    client = MongoClient('localhost:27017')
    db = client[db_name]
    return db

def make_pipeline():
    pipeline = [{"$group" : {"_id" : "$source",
                             "count" : {"$sum" : 1}}},
                            {"$sort" : {"count" : -1}}]
    return pipeline

def aggregate(db, pipeline):
    return [doc for doc in db.aggregate(pipeline)]

if __name__ == '__main__':
    db = get_db('twitter')
    pipeline = make_pipeline()
    result = aggregate(db.tweets, pipeline)
    for source in result[:10]:
        pprint (source)

from pymongo import MongoClient
from pprint import pprint
from group_operator import get_db, aggregate


def make_pipeline():
    pipeline = [
        {"$match" : {"country" : "India"}},
        {"$unwind" : "$isPartOf"},
        {"$group" : {"_id" : "$isPartOf",
                     "count" : {"$sum" : 1}}},
        {"$sort" : {"count" : -1}},
        {"$limit" : 10}
    ]

    return pipeline


if __name__ == '__main__':
    db = get_db('examples')
    result = aggregate(db.cities, make_pipeline())

    pprint(result)

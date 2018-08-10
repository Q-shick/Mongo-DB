from pymongo import MongoClient
from pprint import pprint
from group_operator import get_db, aggregate


def make_pipeline():
    pipeline = [
        {"$match" : {"country" : "India"}},
        {"$unwind" : "$isPartOf"},
        {"$group" : {"_id" : "$isPartOf",
                     "region_average" : {"$avg" : "$population"}}},
        {"$group" : {"_id" : "Regional Average in India",
                     "avg" : {"$avg" : "$region_average"}}}
    ]
    
    return pipeline


if __name__ == '__main__':
    db = get_db('examples')
    result = aggregate(db.cities, make_pipeline())

    pprint(result)

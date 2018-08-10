from pymongo import MongoClient
from pprint import pprint
from group_operator import get_db, aggregate


def make_pipeline():
    # complete the aggregation pipeline
    pipeline = [
        {"$unwind" : "$user.screen_name"},
        {"$group" : {"_id" : "$user.screen_name",
                     "count" : {"$sum" : 1},
                     "tweet_texts" : {"$push" : "$text"}}},
        {"$sort" : {"count" : -1}},
        {"$limit" : 5}
    ]

    return pipeline


if __name__ == '__main__':
    db = get_db('twitter')
    result = aggregate(db.tweets, make_pipeline())

    pprint(result)

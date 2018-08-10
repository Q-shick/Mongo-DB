from pymongo import MongoClient
from pprint import pprint
from group_operator import get_db, aggregate


def make_pipeline():
    pipeline = [
        {"$match" : {"user.time_zone" : {"$eq" : "Brasilia"},
                     "user.statuses_count" : {"$gte" : 100}}},
        {"$project" : {"followers" : "$user.followers_count",
                       "screen_name" : "$user.screen_name",
                       "tweets" : "$user.statuses_count"}},
        {"$sort" : {"followers" : -1}},
        {"$limit" : 10}
    ]

    return pipeline


if __name__ == '__main__':
    db = get_db('twitter')
    result = aggregate(db.tweets, make_pipeline())

    pprint(result)

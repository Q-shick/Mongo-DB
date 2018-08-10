from pymongo import MongoClient
from datetime import datetime
import pprint


def range_query(year):
    query = {"foundingDate": {"$gt": datetime(year, 12, 31, 0, 0)}}
    return query

def exist_query(field):
    query = {field: {"$exists": 1}}
    return query

def regex_query(keyword):
    query = {"motto": {"$regex": keyword}}
    return query

def get_db():
    client = MongoClient('localhost:27017')
    db = client.examples
    return db


if __name__ == "__main__":
    # For local use
    db = get_db()

    # query with founding date
    print ("Enter the year:")
    year = input()
    new_cities = db.cities.find(range_query(int(year)))
    print ("\nCities founded after the year", year, ":", new_cities.count(), "\n[Exmaple]")
    pprint.pprint(new_cities[0])

    # query with government type
    print ("Enter the field:")
    field = input()
    field_exist = db.cities.find(exist_query(field))
    print ("\nCities with field", field, ":", field_exist.count(), "\n[Exmaple]")
    pprint.pprint(field_exist[0])

    # regex exist_query
    print ("Enter the keyword:")
    keyword = input()
    motto = db.cities.find(regex_query(keyword))
    print ("\nCities with motto including ", keyword, ":", motto.count(), "\n[Exmaple]")
    pprint.pprint(motto[0])

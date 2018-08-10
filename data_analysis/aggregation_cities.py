from pymongo import MongoClient
from pprint import pprint
from group_operator import get_db, aggregate


def common_name_pipeline():
    pipeline = [
        {"$match" : {"name" : {"$exists" : 1}}},
        {"$group" : {"_id" : "$name",
                     "count" : {"$sum" : 1}}},
        {"$sort" : {"count" : -1}},
        {"$limit" : 10}
    ]

    return pipeline


def regional_cities_pipeline():
    pipeline = [
        {"$match" : {"country" : "India",
                     "$and" : [{"lon" : {"$gte" : 75}}, {"lon" : {"$lte" : 80}}]}},
        {"$unwind" : "$isPartOf"},
        {"$group" : {"_id" : "$isPartOf",
                     "count" : {"$sum" : 1}}},
        {"$sort" : {"count" : -1}},
        {"$limit" : 10}
    ]

    return pipeline


def country_regional_average_pipeline():
    pipeline = [
        {"$unwind" : "$isPartOf"},
        {"$group" : {"_id" : {"country" : "$country", "region" : "$isPartOf"},
                     "avgRegionalPopulation" : {"$avg" : "$population"}}},
        {"$match" : {"_id.country" : {"$exists" : 1}}},
        {"$group" : {"_id" : "$_id.country",
                     "avgRegionalPopulation" : {"$avg" : "$avgRegionalPopulation"}}},
        {"$sort" : {"avgRegionalPopulation" : -1}},
        {"$limit" : 10}
    ]

    return pipeline


if __name__ == '__main__':
    db = get_db('examples')
    # query most common city names
    print ("\nWhat is the most common city name in our cities collection?")
    most_common_city_names = aggregate(db.cities, common_name_pipeline())
    pprint (most_common_city_names)
    # largest number of cities in India between 75~80 longitude
    print ("\nWhich Region in India has the largest number of cities with longitude between 75 and 80?")
    most_regional_cities = aggregate(db.cities, regional_cities_pipeline())
    pprint (most_regional_cities)
    # largest number of cities in India between 75~80 longitude
    print ("\nWhat is the average regional population by country?")
    country_regional_average_population = aggregate(db.cities, country_regional_average_pipeline())
    pprint (country_regional_average_population)

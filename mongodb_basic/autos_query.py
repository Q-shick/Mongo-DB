import pprint
from pymongo import MongoClient

def in_query():
    query = {"$and" : [{"manufacturer" : {"$in": ["Ford Motor Company", "BMW"]}},
                       {"assembly" : {"$in" : ["Germany", "United States"]}}
                      ]
            }
    return query

def all_query():
    query = {"modelYears" : {"$all" : [2005, 2006, 2007, 2008, 2009]}}
    return query

def dot_query():
    query = {"dimensions.weight" : {"$gt" : 500000}}
    return query

def get_db():
    client = MongoClient('localhost:27017')
    db = client.examples
    return db


if __name__ == "__main__":
    db = get_db()

    # in query for makes and assembled country
    manufacturer_assembly = db.autos.find(in_query(), {"name": 1, "manufacturer": 1, "assembly": 1, "_id":0})
    print ("Ford autos in Germany/US/Japan:", manufacturer_assembly.count())
    pprint.pprint(manufacturer_assembly[0])

    # all query for model years
    model_years = db.autos.find(all_query(), {"name": 1, "manufacturer": 1, "modelYears": 1, "_id":0})
    print ("Model produced throughout 2005~2009:", model_years.count())
    pprint.pprint(model_years[0])

    # dot query for weight
    car_weight = db.autos.find(dot_query(), {"name": 1, "manufacturer": 1, "dimensions": 1, "_id":0})
    print ("Heavy cars with weight over 500000:", car_weight.count())
    pprint.pprint(car_weight[0])

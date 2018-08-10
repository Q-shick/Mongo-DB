from pymongo import MongoClient
import pprint


if __name__ == "__main__":
    db = MongoClient("localhost:27017").examples

    # update using save query
    save_city = db.cities.find_one({"name" : "München",
                               "country" : "Germany"})
    city["isoCountryCode"] = "DEU"
    db.cities.save(city)
    print ("Add ISO code using 'save'")
    pprint.pprint(city)

    # undo using unset query
    db.cities.update({"name" : "München",
                      "country" : "Germany"},
                     {"$unset" : {"isoCountryCode" : ""}})
    unset_city = db.cities.find_one({"name" : "München",
                               "country" : "Germany"})
    print ("\nDelete ISO code using 'unset'")
    pprint.pprint(city)

    # update multiple elements with set query
    db.cities.update({"country" : "Germany"},
                     {"$set" : {"isoCountryCode" : "DEU"}}, multi = True)
    cities = db.cities.find({"country" : "Germany"})
    print ("\nAdd ISO code to all German cities using 'update'")
    for city in cities[:3]:
        pprint.pprint(city)

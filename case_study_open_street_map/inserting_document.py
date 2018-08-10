from pymongo import MongoClient
import xml.etree.cElementTree as ET
import json
from pprint import pprint
from improving_street_names import mapping, is_street_name, update_name
from preparing_database import process_map

OSMFILE = "../Data/memphis.osm"


if __name__ == "__main__":
    client = MongoClient("mongodb://localhost:27017")
    db = client.openStreetMap
    # improve street names
    # osmfile = open(OSMFILE, "r", encoding = "utf8")
    # for event, elem in ET.iterparse(osmfile, events=("start",)):
    #     if elem.tag == "node" or elem.tag == "way":
    #         for tag in elem.iter("tag"):
    #             if is_street_name(tag):
    #                 tag.attrib['v'] = update_name(tag.attrib['v'], mapping)
    # osmfile.close()
    # read json file
    #data = process_map(OSMFILE, False)
    json_data = []
    for line in open("../Data/memphis.json", 'r', encoding = "utf8"):
        json_data.append(json.loads(line))
    # insert bson to mongodb
    db.memphis.insert(json_data)
    pprint(db.memphis.find_one())

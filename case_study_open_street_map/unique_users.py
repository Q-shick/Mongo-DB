import xml.etree.cElementTree as ET
from pprint import pprint
import re

FILENAME = "../Data/memphis.osm"


def get_user(element):
    if "uid" in element.attrib.keys():
        return element.attrib["uid"]
    return None


def process_map(filename):
    users = set()
    for _, element in ET.iterparse(filename):
        user = get_user(element)
        if user != None:
            users.add(user)

    return users


def test():
    users = process_map(FILENAME)
    print ("Number of unique users who committed to the map:", len(users))


if __name__ == "__main__":
    test()

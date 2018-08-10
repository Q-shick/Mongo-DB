import xml.etree.cElementTree as ET
from pprint import pprint

FILENAME = "../Data/memphis.osm"


def count_tags(filename):
    tags = {}
    for event, elem in ET.iterparse(filename, events = ("start",)):
        if event == "start":
            elem = elem.tag
            if elem in tags.keys():
                tags[elem] += 1
            else:
                tags[elem] = 1

    return tags


def test():
    tags = count_tags(FILENAME)
    pprint(tags)


if __name__ == "__main__":
    test()

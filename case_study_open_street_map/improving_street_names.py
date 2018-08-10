import xml.etree.cElementTree as ET
from collections import defaultdict
import re
from pprint import pprint

OSMFILE = "../Data/memphis.osm"
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons", "North", "East", "West", "South", "Circle"]

mapping = { "St": "Street", "St.": "Street",
            "Ave": "Avenue", "Ave.": "Avenue",
            "Blvd": "Boulevard", "Blvd.": "Boulevard",
            "Dr": "Drive", "Dr.": "Drive",
            "Ct": "Court", "Ct.": "Court",
            "Pl": "Place", "Pl.": "Place",
            "Sq": "Square", "Sq.": "Square",
            "Ln": "Lane", "Ln.": "Lane",
            "Rd": "Road", "Rd.": "Road",
            "Tr": "Trail", "Tr.": "Trail",
            "Prky": "Parkway", "PRKY.": "Parkway",
            "Cmns": "Commons", "CMNS": "Commons",
            "N": "North", "E": "East", "W": "West", "S": "South",
            "N.": "North", "E.": "East", "W.": "West", "S.": "South",
            "Cir": "Circle",
          }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r", encoding = "utf8")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    osm_file.close()
    return street_types


def update_name(name, mapping):
    for key, value in mapping.items():
        name = name.replace(key, value)

    return name


def test():
    st_types = audit(OSMFILE)
    print("Result of auditing")
    pprint(dict(st_types))

    for st_type, ways in st_types.items():
        if st_type in mapping.keys():
            for name in ways:
                better_name = update_name(name, mapping)
                print(name, "=>", better_name)


if __name__ == '__main__':
    test()

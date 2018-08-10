import codecs
import csv
import json
import pprint

CITIES = '../Data/cities.csv'

FIELDS = ["name", "timeZone_label", "utcOffset", "homepage", "governmentType_label",
          "isPartOf_label", "areaCode", "populationTotal", "elevation",
          "maximumElevation", "minimumElevation", "populationDensity",
          "wgs84_pos#lat", "wgs84_pos#long", "areaLand", "areaMetro", "areaUrban"]


def is_integer(value):
    try:
        int(value.strip())
        return True
    except ValueError:
        return False


def is_float(value):
    try:
        float(value.strip())
        return True
    except ValueError:
        return False


def audit_file(filename, fields):
    fieldtypes = {}
    for field in FIELDS:
        fieldtypes[field] = set()

    with open(CITIES, "r", encoding = "utf8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if row["URI"].startswith("http://dbpedia.org"):
                for field in FIELDS:
                    if row[field] == "NULL" or row[field] == "":
                        fieldtypes[field].add(type(None))
                    elif row[field].startswith('{'):
                        fieldtypes[field].add(type([]))
                    elif is_integer(row[field]):
                        fieldtypes[field].add(type(1))
                    elif is_float(row[field]):
                        fieldtypes[field].add(type(1.1))
                    else:
                        fieldtypes[field].add(type("str"))

    return fieldtypes


def test():
    fieldtypes = audit_file(CITIES, FIELDS)

    pprint.pprint(fieldtypes)

    assert fieldtypes["areaLand"] == set([type(1.1), type([]), type(None)])
    assert fieldtypes['areaMetro'] == set([type(1.1), type(None)])


if __name__ == "__main__":
    test()

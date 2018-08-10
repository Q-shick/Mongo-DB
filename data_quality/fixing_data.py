import codecs
import csv
import json
import pprint
import sys
sys.path.append("../data_quality")
from auditing_data import is_float

CITIES = '../Data/cities.csv'


def fix_area(area):
    if is_float(area):
        return float(area)
    elif area[0] == "{":
        area_list = area.replace("{", "").replace("}", "").split("|")
        return float(max(area_list, key = lambda ar : len(ar.split("e")[0])))
    else:
        return None


def fix_name(name):
    if name[0] == "{":
        return name.replace("{", "").replace("}", "").split("|")
    elif name == "NULL" or name == "":
        return []
    else:
        return [name]


def process_file(filename):
    # CHANGES TO THIS FUNCTION WILL BE IGNORED WHEN YOU SUBMIT THE EXERCISE
    data = []

    with open(filename, "r", encoding = "utf8") as f:
        reader = csv.DictReader(f)

        #skipping the extra metadata
        for i in range(3):
            l = next(reader)

        # processing file
        for line in reader:
            if "areaLand" in line:
                line["areaLand"] = fix_area(line["areaLand"])
            if "name" in line:
                line["name"] = fix_name(line["name"])
            data.append(line)

    return data


def test():
    data = process_file(CITIES)

    print ("Three example of Land Area")
    pprint.pprint(data[0]["areaLand"])
    pprint.pprint(data[1234]["areaLand"])
    pprint.pprint(data[12345]["areaLand"])

    print ("Three example of Country Name")
    pprint.pprint(data[0]["name"])
    pprint.pprint(data[4]["name"])
    pprint.pprint(data[621]["name"])


if __name__ == "__main__":
    test()

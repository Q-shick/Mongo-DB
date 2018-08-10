from pymongo import MongoClient
import csv
import json
import io
from datetime import datetime
from csv_to_json_autos import skip_lines, is_number, empty_val


field_map = {
    'areaCode': "areaCode",
    'areaLand': "areaLand",
    'country_label': "country",
    'elevation': "elevation",
    'foundingDate': "foundingDate",
    'governmentType_label': "governmentType",
    'homepage': "homepage",
    'isPartOf_label': "isPartOf",
    "wgs84_pos#lat" : "lat",
    'leaderTitle': "leaderTitle",
    "wgs84_pos#long" : "lon",
    'motto': "motto",
    'name': "name",
    'populationTotal': "population",
    'postalCode': "postalCode",
    'timeZone_label': "timeZone",
    'utcOffset': "utcOffset"
}

fields = field_map.keys()


def is_integer(val):
    try:
        int(val)
        return True
    except ValueError:
        return False

def toDate(val): # mm/dd/yyyy   yyyy-mm-dd
    if val[0] == "{":
        val = val.replace("{", "").replace("}", "").split("|")[0]

    if is_integer(val[:4]):
        date = datetime.strptime(val, "%Y-%m-%d")
    else:
        date = datetime.strptime(val, "%m/%d/%Y")

    return date


def toList(val):
    if val[0] == '{':
        val = val.replace("{", "").replace("}", "")

    return val.split("|")


def process_file(input_file):
    input_data = csv.DictReader(open(input_file, encoding = "utf8"))
    cities = []
    skip_lines(input_data, 4)
    for row in input_data:
        city = {}
        for field, val in row.items():
            if field not in fields or empty_val(val):
                continue

            if field == "populationTotal":
                if is_integer(val):
                    val = int(val)
                else:
                    val = ""
            elif field == "foundingDate":
                val = toDate(val)
            elif field in ["areaLand", "elevation", "lat", "lon"]:
                if is_number(val):
                    val = float(val)
                else:
                    val = ""
            elif field in ["areaCode", "governmentType_label", "homepage", "name",
                           "isPartOf_label", "timeZone_label", "utcOffset"]:
                val = toList(val)

            city[field_map[field]] = val
        cities.append(city)
    return cities

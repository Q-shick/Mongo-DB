import codecs
import csv
import json
import pprint
import re

DATAFILE = '../Data/arachnid.csv'
FIELDS ={'rdf-schema#label': 'label',
         'URI': 'uri',
         'rdf-schema#comment': 'description',
         'synonym': 'synonym',
         'name': 'name',
         'family_label': 'family',
         'class_label': 'class',
         'phylum_label': 'phylum',
         'order_label': 'order',
         'kingdom_label': 'kingdom',
         'genus_label': 'genus'}


def clean_label(val):
    r = re.compile('[^\(.+\)]*')
    val = r.search(val).group().strip()
    return val


def parse_array(val):
    if val is None:
        return None

    if (val[0] == "{") and (val[-1] == "}"):
        val = val.lstrip("{")
        val = val.rstrip("}")
        val_array = val.split("|")
        val_array = [i.strip() for i in val_array]
        return val_array

    return [val]


def process_file(filename):
    fields = FIELDS
    process_fields = fields.keys()
    data = []
    with open(filename, "r") as f:
        reader = csv.DictReader(f)
        # skip the first 3 lines
        for i in range(3):
            l = next(reader)
        # read line by line
        for line in reader:
            arachnid = {}
            classification = {}
            for field, val in line.items():
                # process only the field map
                if field not in process_fields:
                    continue
                # all "NULL"s converted to None
                if val == "NULL":
                    val = None
                # process each field
                if field == "rdf-schema#label":
                    arachnid[fields[field]] = clean_label(val)
                elif field == "name":
                    if val is None or not(val.isalnum()):
                        arachnid[fields[field]] = arachnid["label"]
                    else:
                        arachnid[fields[field]] = val
                elif field == "synonym":
                    arachnid[fields[field]] = parse_array(val)
                elif field in ["family_label", "class_label", "phylum_label",
                               "order_label", "kingdom_label", "genus_label"]:
                    classification[fields[field]] = val
                else:
                    arachnid[fields[field]] = val
                arachnid["classification"] = classification
            data.append(arachnid)

    return data


def test():
    data = process_file(DATAFILE)
    print ("Your first entry:")
    pprint.pprint(data[0])
    first_entry = {
        "synonym": None,
        "name": "Argiope",
        "classification": {
            "kingdom": "Animal",
            "family": "Orb-weaver spider",
            "order": "Spider",
            "phylum": "Arthropod",
            "genus": None,
            "class": "Arachnid"
        },
        "uri": "http://dbpedia.org/resource/Argiope_(spider)",
        "label": "Argiope",
        "description": "The genus Argiope includes rather large and spectacular spiders that often have a strikingly coloured abdomen. These spiders are distributed throughout the world. Most countries in tropical or temperate climates host one or more species that are similar in appearance. The etymology of the name is from a Greek name meaning silver-faced."
    }

    assert len(data) == 76
    assert data[0] == first_entry
    assert data[17]["name"] == "Ogdenia"
    assert data[48]["label"] == "Hydrachnidiae"
    assert data[14]["synonym"] == ["Cyrene Peckham & Peckham"]

if __name__ == "__main__":
    test()

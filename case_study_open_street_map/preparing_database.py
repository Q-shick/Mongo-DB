import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

FILENAME = "../Data/memphis.osm"

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]


def shape_element(element):
    node = {}
    if element.tag == "node" or element.tag == "way" :
        # first level
        node["created"] = {}
        node["type"] = element.tag
        lat, lon = 0.0, 0.0
        for key in element.attrib.keys():
            if key in CREATED:
                node["created"][key] = element.attrib[key]
            elif key == "lat":
                lat = float(element.attrib[key])
            elif key == "lon":
                lon = float(element.attrib[key])
            else:
                node[key] = element.attrib[key]
        node["pos"] = [lat, lon]
        # second level
        node["address"] = {}
        node["node_refs"] = []
        for child in element:
            if child.tag == "tag":
                if re.match(problemchars, child.attrib['k']):
                    continue
                elif re.match(lower_colon, child.attrib['k']):
                    addr_key, addr_value = child.attrib['k'].split(":")
                    if addr_key == "addr":
                        node["address"][addr_value] = child.attrib['v']
                else:
                    node[child.attrib['k']] = child.attrib['v']
            elif child.tag == "nd":
                node["node_refs"].append(child.attrib['ref'])
        # empty 'address' and 'node_refs' if none
        if node["address"] == {}:
            node.pop("address")
        if node["node_refs"] == []:
            node.pop("node_refs")
        return node
    # ignore or other tags
    else:
        return None


def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def test():
    data = process_map(FILENAME, True)
    pprint.pprint(data[0])


if __name__ == "__main__":
    test()

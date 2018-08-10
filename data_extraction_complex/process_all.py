from bs4 import BeautifulSoup
import os
import sys
sys.path.append("../data_extraction_fundamental")
from exploring_json import pretty_print

DATADIR = "../Data/Flights"


def process_all(datadir):
    files = os.listdir(DATADIR)
    return files


def process_file(f):
    """
    This function extracts data from the file given as the function argumen
    in a list of dictionaries.
    """
    data = []
    info = {}
    info["courier"], info["airport"] = f[:6].split("-") # filename: FL-ATL

    with open("{}/{}".format(DATADIR, f), "r") as html: # DATADIR/filename
        soup = BeautifulSoup(html, "lxml")
        for flight in soup.find_all("tr", {"class":"dataTDRight"}):
            td = flight.find_all("td")
            print(td)

            if (td[1].text).strip() != "TOTAL":
                info["year"] = int(td[0].text)
                info["month"] = int(td[1].text)
                info["flights"] = {"domestic": int((td[2].text).replace(",", "")),
                                   "international": int((td[3].text).replace(",", ""))}
            data.append(info)

    return data


def test():
    print ("Running a simple test...")
    files = process_all(DATADIR)
    data = []
    # Test will loop over three data files.
    for f in files:
        data += process_file(f)

    for entry in data[:3]:
        assert type(entry["year"]) == int
        assert type(entry["month"]) == int
        assert type(entry["flights"]["domestic"]) == int
        assert len(entry["airport"]) == 3
        assert len(entry["courier"]) == 2

    print ("Success!")
    for i in range(3):
        pretty_print (data[i], 2)

test()

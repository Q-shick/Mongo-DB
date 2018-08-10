import os

DATADIR = "../DATA/"
DATAFILE = "beatles-diskography.csv"


def parse_file(datafile):
    data = []
    header = ""

    with open(datafile, "r") as f:
        for line in f:
            line = line.strip().split(",")

            if header is "":
                header = line
            else:
                data.append(dict(zip(header, line)))

    return data


def test():
    # a simple test of your implemetation
    datafile = os.path.join(DATADIR, DATAFILE)
    d = parse_file(datafile)
    firstline = {'Title': 'Please Please Me', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '22 March 1963', 'US Chart Position': '-', 'RIAA Certification': 'Platinum', 'BPI Certification': 'Gold'}
    tenthline = {'Title': '', 'UK Chart Position': '1', 'Label': 'Parlophone(UK)', 'Released': '10 July 1964', 'US Chart Position': '-', 'RIAA Certification': '', 'BPI Certification': 'Gold'}

    assert d[0] == firstline
    assert d[9] == tenthline

    print("Successfully Parsing CSV!\nExample: ", d[0])


test()

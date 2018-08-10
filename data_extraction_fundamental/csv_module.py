import csv
import os

DATADIR = "../Data/"
DATAFILE = "745090.csv"


def parse_file(datafile):
    name = ""
    data = []
    with open(datafile,'r') as csvfile:
        nrel = csv.reader(csvfile)
        name = next(nrel)[1]
        # skip the header
        next(nrel)
        for row in nrel:
            data.append(row)

    return (name, data)


def test():
    datafile = os.path.join(DATADIR, DATAFILE)
    name, data = parse_file(datafile)

    assert name == "MOUNTAIN VIEW MOFFETT FLD NAS"
    assert data[0][1] == "01:00"
    assert data[2][0] == "01/01/2005"
    assert data[2][5] == "2"


if __name__ == "__main__":
    test()

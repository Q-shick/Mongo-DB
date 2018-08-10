import os
import xlrd
from zipfile import ZipFile

DATADIR = "../DATA/"
DATAFILE = "2013_ERCOT_Hourly_Load_Data.xls"


def open_zip(datafile):
    with ZipFile('{0}.zip'.format(datafile), 'r') as myzip:
        myzip.extractall(DATADIR)


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)

    sheet_data = [[sheet.cell_value(row, col)
                   for col in range(sheet.ncols)]
                   for row in range(sheet.nrows)]

    coast = sheet.col_values(1, start_rowx = 1, end_rowx = None)

    max_value = max(coast)
    max_index = coast.index(max_value) + 1 # due to the header
    min_value = min(coast)
    min_index = coast.index(min_value) + 1 # due to the header
    avg_value = sum(coast)/len(coast)

    data = {
            'maxtime': xlrd.xldate_as_tuple(sheet.cell_value(max_index, 0), 0),
            'maxvalue': max_value,
            'mintime': xlrd.xldate_as_tuple(sheet.cell_value(min_index, 0), 0),
            'minvalue': min_value,
            'avgcoast':avg_value
    }

    return data


def test():
    open_zip(DATADIR + DATAFILE)
    data = parse_file(DATADIR + DATAFILE)

    assert data['maxtime'] == (2013, 8, 13, 17, 0, 0)
    assert round(data['maxvalue'], 10) == round(18779.02551, 10)

    print("Successfully Parsing CSV!\nMax Time: ", data['maxtime'])


test()

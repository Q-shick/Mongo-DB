import xlrd
import os
import csv
from exploring_json import pretty_print

DATAFILE = "../Data/2013_ERCOT_Hourly_Load_Data.xls"
OUTFILE = "../Data/2013_Max_Loads.csv"


def parse_file(datafile):
    workbook = xlrd.open_workbook(datafile)
    sheet = workbook.sheet_by_index(0)
    data = {}
    # process all rows that contain station data
    region = sheet.row_values(0, start_colx = 1, end_colx = 9)
    print(region)
    # iterate each region
    for i, value in enumerate(region):
        region_values = sheet.col_values(i + 1, start_rowx = 1, end_rowx = None)
        max_value = max(region_values)
        max_index = region_values.index(max_value) + 1 # due to the header
        max_time = xlrd.xldate_as_tuple(sheet.cell_value(max_index, 0), 0)
        # write data to the region
        data[value] = {"max_value": max_value, "max_time": max_time}

    pretty_print(data, indent = 2)
    return data


def save_file(data, filename):
    with open(filename, "w") as f:
        w = csv.writer(f, delimiter='|')
        # header
        w.writerow(["Station", "Year", "Month", "Day", "Hour", "Max Load"])
        # content
        for s in data:
            year, month, day, hour, _ , _= data[s]["max_time"]
            w.writerow([s, year, month, day, hour, data[s]["max_value"]])


def test():
    data = parse_file(DATAFILE)
    save_file(data, OUTFILE)

    number_of_rows = 0
    stations = []

    ans = {'FAR_WEST': {'Max Load': '2281.2722140000024',
                        'Year': '2013',
                        'Month': '6',
                        'Day': '26',
                        'Hour': '17'}}
    correct_stations = ['COAST', 'EAST', 'FAR_WEST', 'NORTH',
                        'NORTH_C', 'SOUTHERN', 'SOUTH_C', 'WEST']
    fields = ['Year', 'Month', 'Day', 'Hour', 'Max Load']

    with open(OUTFILE) as of:
        csvfile = csv.DictReader(of, delimiter="|")
        for line in csvfile:
            station = line['Station']
            if station == 'FAR_WEST':
                for field in fields:
                    # Check if 'Max Load' is within .1 of answer
                    if field == 'Max Load':
                        max_answer = round(float(ans[station][field]), 1)
                        max_line = round(float(line[field]), 1)
                        assert max_answer == max_line

                    # Otherwise check for equality
                    else:
                        assert ans[station][field] == line[field]

            number_of_rows += 1
            stations.append(station)

        # Output should be 8 lines not including header
        assert number_of_rows == 8
        # Check Station Names
        assert set(stations) == set(correct_stations)


if __name__ == "__main__":
    test()

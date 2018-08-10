"""
Your task is to check the "productionStartYear" of the DBPedia autos datafile for valid values.
The following things should be done:
- check if the field "productionStartYear" contains a year
- check if the year is in range 1886-2014
- convert the value of the field to be just a year (not full datetime)
- the rest of the fields and values should stay the same
- if the value of the field is a valid year in the range as described above,
  write that line to the output_good file
- if the value of the field is not a valid year as described above,
  write that line to the output_bad file
- discard rows (neither write to good nor bad) if the URI is not from dbpedia.org
- you should use the provided way of reading and writing data (DictReader and DictWriter)
  They will take care of dealing with the header.

You can write helper functions for checking the data and writing the files, but we will call only the
'process_file' with 3 arguments (inputfile, output_good, output_bad).
"""
import csv
import pprint

INPUT_FILE = '../Data/autos.csv'
OUTPUT_GOOD = '../Data/autos-valid.csv'
OUTPUT_BAD = '../Data/FIXME-autos.csv'


def year_check(year):
    if year == "NULL":
        return False

    year = int(year[:4])

    if year < 1886 or year > 2014:
        return False

    return True


def process_file(input_file, output_good, output_bad):
    valid_data = []
    invalid_data = []

    with open(input_file, "r") as f:
        reader = csv.DictReader(f) # DictReader is more readable than just Reader
        header = reader.fieldnames
        for row in reader:
            if row["URI"].startswith("http://dbpedia.org"):
                year = row["productionStartYear"]
                if year_check(year):
                    valid_data.append(row)
                else:
                    invalid_data.append(row)

    with open(output_good, "w", newline = "") as good:
        writer = csv.DictWriter(g, delimiter = ",", fieldnames = header)
        writer.writeheader()
        for row in valid_data:
            writer.writerow(row)

    with open(output_bad, "w", newline = "") as bad:
        writer = csv.DictWriter(bad, delimiter = ",", fieldnames = header)
        writer.writeheader()
        for row in invalid_data:
            writer.writerow(row)


def test():
    process_file(INPUT_FILE, OUTPUT_GOOD, OUTPUT_BAD)


if __name__ == "__main__":
    test()

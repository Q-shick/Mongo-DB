import xml.etree.ElementTree as ET
PATENTS = "../Data/patent.data"


def get_root(fname):
    tree = ET.parse(fname)
    return tree.getroot()


def split_file(filename):
    """
    Split the input file into separate files, each containing a single patent.
    As a hint - each patent declaration starts with the same line that was
    causing the error found in the previous exercises.

    The new files should be saved with filename in the following format:
    "{}-{}".format(filename, n) where n is a counter, starting from 0.
    """
    delimiter = "<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
    with open(filename, 'r') as rf:
        files = rf.read()
        files = files.split(delimiter)
    del files[0]

    for i in range(len(files)):
        fname = "{}-{}".format(PATENTS, i)
        wf = open(fname, 'w')
        wf.write(delimiter)
        wf.write(files[i])


def test():
    split_file(PATENTS)
    for n in range(4):
        try:
            fname = "{}-{}".format(PATENTS, n)
            f = open(fname, "r")
            if not f.readline().startswith("<?xml"):
                print ("You have not split the file {} in the correct boundary!".format(fname))
            f.close()
        except:
            print ("Could not find file {}. Check if the filename is correct!".format(fname))


test()

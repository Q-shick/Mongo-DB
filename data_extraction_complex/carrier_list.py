from bs4 import BeautifulSoup
page = "../Data/options.html"


def extract_carriers(page):
    data = []

    with open(page, "r") as html:
        # do something here to find the necessary values
        soup = BeautifulSoup(html, "lxml")

        for code in soup.find_all('option'):
            code = code['value']
            if len(code) == 2:
                data.append(code)

    return data


def test():
    data = extract_carriers(page)
    assert len(data) == 16
    assert "FL" in data
    assert "NK" in data
    print("Carrier List\n", data)


test()

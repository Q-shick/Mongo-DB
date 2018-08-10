#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Complete the 'extract_airports()' function so that it returns a list of airport
codes, excluding any combinations like "All".

Refer to the 'options.html' file in the tab above for a stripped down version
of what is actually on the website. The test() assertions are based on the
given file.
"""

from bs4 import BeautifulSoup
import re
page = "../Data/options.html"


def extract_airports(page):
    data = []
    with open(page, "r") as html:
        soup = BeautifulSoup(html, "lxml")
        for option in soup.find_all("option"):
            option = option["value"]
            if len(option) == 3 and option != "All":
                data.append(option)

    return data


def test():
    data = extract_airports(page)
    assert len(data) == 15
    assert "ATL" in data
    assert "ABR" in data
    print("Airport List\n", data)

test()

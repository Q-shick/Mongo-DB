from bs4 import BeautifulSoup
import requests
import json

s = requests.Session()
r = s.get("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2")
soup = BeautifulSoup(r.text)
viewstate = soup.find(id = "__VIEWSTATE")['value']
eventvalidation = soup.find(id = "__EVENTVALIDATION")['value']

r = s.post("http://www.transtats.bts.gov/Data_Elements.aspx?Data=2",
                    data={'AirportList': "BOS",
                          'CarrierList': "VX",
                          'Submit': 'Submit',
                          "__EVENTTARGET": "",
                          "__EVENTARGUMENT": "",
                          "__EVENTVALIDATION": eventvalidation,
                          "__VIEWSTATE": viewstate})

f = open("../Data/virgin_logan.html", "w")
f.write(r.text)

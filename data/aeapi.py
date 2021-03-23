from bs4 import BeautifulSoup
from flask import Response
import requests
import re

class API(object):
    def __init__(self):
        self.exchange_url = "https://kur.doviz.com"
        self.earthquake_url = "http://www.koeri.boun.edu.tr/scripts/lst7.asp"

class Earthquake(object):
    def __init__(self):
        self.test = "TEST"

    def get_earthquakes(self):
        data = []
        try:
            response = requests.get(API().earthquake_url)
            soup = BeautifulSoup(response.text, "html.parser")
            listed = soup.find("pre")
            splitted = re.split("\n", str(listed))
            earthquake = splitted[7].split()
            for line in splitted[7:-2]:
                earthquake = line.split()
                date = earthquake[0]
                time = earthquake[1]
                latitude = earthquake[2]
                longitude = earthquake[3]
                depth = earthquake[4]
                magnitude_md = earthquake[5]
                magnitude_ml = earthquake[6]
                magnitude_mw = earthquake[7]
                location = ' '.join(earthquake[8:-1])
                sol = earthquake[-1]
                if sol == "Ýlksel":
                    sol = "Ilksel"
                if magnitude_md == "-.-":
                    magnitude_md = None
                if magnitude_mw == "-.-":
                    magnitude_mw = None
                if magnitude_ml == "-.-":
                    magnitude_ml = None
                google_maps = f"https://www.google.com/maps/search/?api=1&query={latitude},{longitude}"

                js = {"date": date, "time": time,
                        "latitude": latitude, "longitude": longitude,
                        "depth": depth, "magnitude_md": magnitude_md,
                        "magnitude_ml": magnitude_ml, "magnitude_mw": magnitude_mw,
                        "location": location, "state": sol,
                        "google_maps": google_maps}
                data.append(js)
            return data
        except requests.exceptions.ConnectionError:
            return Response(404)

class Exchange(object):
    def __init__(self):
        self.test = "TEST"

    def get_exchanges(self):
        data = {}
        try:
            response = requests.get(API().exchange_url)
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table")
            body = table.find("tbody")
            rows = body.find_all("tr")
            for row in rows:
                cols = row.find_all("td")
                cols = [ele.text.strip() for ele in cols]
                if cols[0]:
                    data[cols[0][:3]] = {"currency_name":cols[0][6:],
                                         "currency_code":cols[0][:3],
                                         "currency_buy":cols[1],
                                         "currency_sell":cols[2],
                                         "currency_high":cols[3],
                                         "currency_low":cols[4],
                                         "currency_change":cols[5],
                                         "time":cols[6]}

            return data
        except requests.exceptions.ConnectionError:
            return Response(404)
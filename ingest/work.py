#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.time_utils import iso_format, current_date_time
import requests


class Forecast():
    """
    Scrape the observed conditions NWS API for home.
    Home, sweet home!
    """
    def __init__(self, config):
        # Date
        self.today = iso_format()
        # Config
        self.header = config["header"]
        self.url = config["url"]
        self.table = config["table"]
        # Data
        self.home_fc = {}

    def call_api(self):
        """Call the API and store the returned forecast periods."""
        response = requests.get(url=self.url, headers=self.header, timeout=15)
        response.raise_for_status()
        api_data = response.json()
        self.home_fc = api_data["properties"]["periods"]

    def parse_data(self, data):
        """Parse the API response data."""
        fc = []
        for entry in data:
            row = []
            row.append(current_date_time())
            row.append(entry["startTime"])
            row.append(entry["isDaytime"])
            row.append(entry["temperature"])
            row.append(entry["probabilityOfPrecipitation"]["value"])
            row.append(float(entry["windSpeed"].split()[-2]))
            row.append(entry["windDirection"])
            row.append(entry["relativeHumidity"]["value"])
            row.append(entry["shortForecast"])
            fc.append(row)
        return fc

    def run(self):
        """Run the forecast scraper and return the forecast data."""
        self.call_api()
        return self.parse_data(self.home_fc)


if __name__ == "__main__":
    ### Testing ###
    from config import loader
    config = loader.Loader()
    hfc = Forecast(config.hfc_config())
    hfc.run()

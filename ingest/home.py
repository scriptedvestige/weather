#!/usr/bin/env python3
import sys
sys.path.append(".")

from utils.time_utils import iso_format, filename_format, current_date_time
from utils.file_utils import forecast_output
import requests
import json

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
        """Call API and write data to forecast.txt"""
        api_data = requests.get(url=self.url, headers=self.header).json()
        self.home_fc = api_data["properties"]["periods"]
        filename = forecast_output(zone="home", date=filename_format())
        # self.save_file(filename=filename, forecast=self.home_fc)

    ''' def save_file(self, filename, forecast):
        """Save forcast data to json file.  For testing and debug."""
        with open(filename, "w") as file:
            json.dump(forecast, file, indent=4) '''

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
            row.append(entry["windSpeed"].split()[-2])
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
    """ from config import loader
    config = loader.Loader()
    hfc = Forecast(config.hfc_config())
    hfc.run() """

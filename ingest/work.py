#!/usr/bin/env python3
import sys
sys.path.append(".")

from utils.time_utils import iso_format, filename_format, current_date_time
from utils.file_utils import forecast_output
import requests
import json


class Forecast:
    """
    Scrape the NWS forecast API for work.
    Eww, work. -_-
    """
    def __init__(self, config):
        # Date
        self.today = iso_format()
        # Config
        self.header = config["header"]
        self.url = config["url"]
        self.table = config["table"]
        # Data
        self.work_fc = {}

    def call_api(self):
        """Call API and write data to forecast.txt"""
        filename = forecast_output(zone="work", date=filename_format())
        api_data = requests.get(url=self.url, headers=self.header).json()
        self.work_fc = api_data["properties"]["periods"]
        self.save_file(filename=filename, forecast=self.work_fc)

    def save_file(self, filename, forecast):
        """Save forcast data to json file."""
        with open(filename, "w") as file:
            json.dump(forecast, file, indent=4)

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
            row.append(entry["detailedForecast"])
            row.append(entry["icon"])
            fc.append(row)
        return fc
    
    def run(self):
        """Run the forecast scraper and return the forecast data."""
        self.call_api()
        return self.parse_data(self.work_fc)
    

if __name__ == "__main__":
    from config import loader
    config = loader.Loader()
    wfc = Forecast(config.wfc_config())
    wfc.run()

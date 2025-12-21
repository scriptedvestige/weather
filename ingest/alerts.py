#!/usr/bin/env python3
import sys
sys.path.append(".")

from utils.time_utils import iso_format, filename_format, current_date_time
from utils.file_utils import forecast_output
import requests
import json


class Alerts:
    """Scrape alerts from the NWS alerts API."""
    def __init__(self, config):
        # Date
        self.today = iso_format()
        # Config
        self.header = config["header"]
        self.url = config["url"]
        self.table = config["table"]
        # Data
        self.alerts = {}

    def call_api(self):
        """Call API and write data to json file."""
        api_data = requests.get(url=self.url, headers=self.header).json()
        self.alerts = api_data["features"]
        filename = forecast_output(zone="alerts", date=filename_format())
        self.save_file(filename=filename, alerts=self.alerts)

    def save_file(self, filename, alerts):
        """Save alerts data to json file.  For testing and debug."""
        with open(filename, "w") as file:
            json.dump(alerts, file, indent=4)

    def run(self):
        """Run the alerts module."""
        self.call_api()

#!/usr/bin/env python3
import sys
sys.path.append(".")

from utils.time_utils import iso_delta, filename_format
from utils.file_utils import forecast_output
import requests
import json


class SevereWeather:
    """Scrape alerts from the NWS alerts API."""
    def __init__(self, config, prev_alert):
        # Date
        self.yesterday = iso_delta(-1)
        # Config
        self.header = config["header"]
        self.urls = config["url"]
        self.table = config["table"]
        # Data
        self.alerts = []
        self.prev_alert = prev_alert
        self.prev_ids = []

    def list_ids(self):
        """Pull the IDs out of the list of tuples."""
        for tup in self.prev_alert:
            self.prev_ids.append(tup[0])

    def update_url(self, url):
        """Modify the URL with current start date."""
        current = f"{self.yesterday}T00:00:00-08:00"
        return url.format(start=current)

    def call_api(self):
        """Call API and write data to json file."""
        for entry in self.urls:
            updated_url = self.update_url(entry)
            api_data = requests.get(url=updated_url, headers=self.header).json()
            self.parse_data(data=api_data["features"])#, prev_alert=self.prev_alert)
        # filename = forecast_output(zone="alerts", date=filename_format())
        # self.save_file(filename=filename, alerts=self.raw_alerts)

    def save_file(self, filename, alerts):
        """Save alerts data to json file.  For testing and debug."""
        with open(filename, "w") as file:
            json.dump(alerts, file, indent=4)

    def parse_data(self, data):
        """Parse the data returned from the API call and insert into table."""
        if len(data) > 0:
            for entry in data:
                if entry["properties"]["id"] not in self.prev_ids:
                    row = []
                    row.append(entry["properties"]["sent"])
                    row.append(entry["properties"]["onset"])
                    row.append(entry["properties"]["ends"])
                    row.append(entry["properties"]["id"])
                    row.append(entry["properties"]["severity"])
                    row.append(entry["properties"]["certainty"])
                    row.append(entry["properties"]["event"])
                    row.append(entry["properties"]["parameters"]["NWSheadline"][0])
                    desc = entry["properties"]["description"].replace("\n", " ")
                    row.append(desc)
                    self.alerts.append(tuple(row))

    def run(self):
        """Run the alerts module."""
        self.call_api()
        return self.alerts


if __name__ == "__main__":
    """Testing."""
    from config import loader
    from output import database
    config = loader.Loader()
    # db = database.Insert(config=config.db_config())
    # prev_alert = db.query(db.get_swa_data())
    swa = SevereWeather(config=config.alerts_config(), prev_alert=None)#prev_alert)
    swa.run()

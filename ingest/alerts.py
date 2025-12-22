#!/usr/bin/env python3
import sys
sys.path.append(".")

from utils.time_utils import iso_delta, filename_format
from utils.file_utils import forecast_output
import requests
import json


class SevereWeather:
    """Scrape alerts from the NWS alerts API."""
    def __init__(self, config, ids):
        # Date
        self.yesterday = iso_delta(-1)
        # Config
        self.header = config["header"]
        self.url = config["url"]
        self.table = config["table"]
        # Data
        self.raw_alerts = {}
        self.prev_alerts = ids

    def list_ids(self):
        """Pull the IDs out of the list of tuples."""
        all_ids = []
        for tup in self.prev_alerts:
            all_ids.append(tup[0])
        return all_ids

    def update_url(self):
        """Modify the URL with current start date."""
        current = f"{self.yesterday}T00:00:00-08:00"
        return self.url.format(start=current)

    def call_api(self):
        """Call API and write data to json file."""
        updated_url = self.update_url()
        api_data = requests.get(url=updated_url, headers=self.header).json()
        self.raw_alerts = api_data["features"]
        ''' filename = forecast_output(zone="alerts", date=filename_format())
        self.save_file(filename=filename, alerts=self.raw_alerts)

    def save_file(self, filename, alerts):
        """Save alerts data to json file.  For testing and debug."""
        with open(filename, "w") as file:
            json.dump(alerts, file, indent=4) '''

    def parse_data(self, data, ids):
        """Parse the data returned from the API call."""
        alerts = []
        if len(self.raw_alerts) > 0:
            for entry in data:
                if entry["properties"]["id"] not in ids:
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
                    alerts.append(row)
            return alerts
        else:
            return None

    def run(self):
        """Run the alerts module."""
        ids_list = self.list_ids()
        self.call_api()
        return self.parse_data(data=self.raw_alerts, ids=ids_list)


if __name__ == "__main__":
    """Testing."""
    from config import loader
    from output import database
    config = loader.Loader()
    db = database.Inserter(config=config.db_config())
    prev_alerts = db.query(db.get_swa_ids())
    swa = SevereWeather(config=config.alerts_config(), ids=prev_alerts)
    swa.run()

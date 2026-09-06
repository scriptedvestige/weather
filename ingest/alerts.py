#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.time_utils import iso_delta
import requests


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
        self.prev_alert = prev_alert or []
        # Build a set of (onset, ends, event, description) tuples for fast lookup.
        self.prev_keys = set(self.prev_alert)

    def update_url(self, url):
        """Modify the URL with current start date, in UTC to match the NWS API and avoid DST issues."""
        current = f"{self.yesterday}T00:00:00Z"
        return url.format(start=current)

    def call_api(self):
        """Call each configured endpoint and parse the results."""
        for entry in self.urls:
            updated_url = self.update_url(entry)
            response = requests.get(url=updated_url, headers=self.header, timeout=15)
            response.raise_for_status()
            api_data = response.json()
            self.parse_data(data=api_data["features"])

    def parse_data(self, data):
        """Parse the data returned from the API call. An alert is only inserted
        if its onset/ends/event/description combination hasn't already been seen —
        this catches genuinely new or changed alerts even though NWS assigns
        a new ID to every update of the same underlying alert."""
        for entry in data:
            props = entry["properties"]
            onset = props["onset"]
            ends = props["ends"]
            event = props["event"]
            desc = (props["description"] or "").replace("\n", " ")
            key = (onset, ends, event, desc)
            if key not in self.prev_keys:
                headline_list = props.get("parameters", {}).get("NWSheadline", [""])
                headline = headline_list[0] if headline_list else ""
                row = (
                    props["sent"],
                    onset,
                    ends,
                    props["id"],
                    props["severity"],
                    props["certainty"],
                    event,
                    headline,
                    desc,
                )
                self.alerts.append(row)
                self.prev_keys.add(key)  # avoid inserting the same content twice within one run, across multiple endpoints

    def run(self):
        """Run the alerts module."""
        self.call_api()
        return self.alerts


if __name__ == "__main__":
    """Testing."""
    from config import loader
    config = loader.Loader()
    swa = SevereWeather(config=config.alerts_config(), prev_alert=[])
    print(swa.run())

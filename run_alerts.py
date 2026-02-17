#!/usr/bin/env python3
import traceback
from datetime import datetime
from functools import wraps

from utils.file_utils import log_path
from config.loader import Loader
from ingest import alerts
from output import database

LOG_PATH = log_path()

# ----- DECORATOR ----- #
def safe_run(module_name):
    """Decorator that runs a function safely and logs any exceptions."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                with open(LOG_PATH, "a") as log:
                    log.write(f"\n[{datetime.now()}] Error in {module_name}:\n")
                    log.write(f"{e}\n")
                    log.write(traceback.format_exc())
                    log.write("\n" + "-"*60 + "\n")
                raise
        return wrapper
    return decorator

# ----- MODULE RUNNER ----- #
@safe_run("Alerts")
def run_alerts(config, prev_alert):
    swa = alerts.SevereWeather(config=config, prev_alert=prev_alert)
    return swa.run()

def scrape_alerts():
     # Create config loader object
    config = Loader()
    
    # Create database injector
    db = database.Insert(config=config.db_config())

    # Pull last alert
    prev_alert = db.query(db.get_swa_data())
    
    # Check for new alerts and insert into alerts table.
    swa_data = run_alerts(config=config.alerts_config(), prev_alert=prev_alert)
    if swa_data != None:
        db.insert(statement=db.swa_statement(), data=swa_data)

if __name__ == "__main__":
    scrape_alerts()
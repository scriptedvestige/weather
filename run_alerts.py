#!/usr/bin/env python3
import sys
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
    """Decorator that runs a function safely, logs any exception, then re-raises
    so the process exits non-zero and the failure is impossible to miss."""
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

# ----- PIPELINE ----- #
@safe_run("Severe Weather Scraper")
def scrape_alerts():
    """Pull the last known alert, fetch current alerts, insert anything new."""
    config = Loader()
    db = database.Insert(config=config.db_config())

    # Pull last alert.
    prev_alert = db.query(db.get_swa_new())

    # Check for new alerts and insert into alerts table.
    swa = alerts.SevereWeather(config=config.alerts_config(), prev_alert=prev_alert)
    swa_data = swa.run()
    if swa_data is not None:
        db.insert(statement=db.swa_statement(), data=swa_data)


if __name__ == "__main__":
    try:
        scrape_alerts()
    except Exception:
        # Already logged inside safe_run — this just ensures cron sees a real failure exit code.
        sys.exit(1)

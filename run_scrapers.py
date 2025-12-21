#!/usr/bin/env python3
import traceback
from datetime import datetime
from functools import wraps

from utils.file_utils import log_path
from config.loader import Loader
from ingest import work, home, alerts
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
        return wrapper
    return decorator

# ----- MODULE RUNNERS ----- #
@safe_run("Work Forecast")
def run_wfc(config):
    """Create and run work scraper."""
    wfc = work.Forecast(config)
    return wfc.run()

@safe_run("Home Forecast")
def run_hfc(config):
    """Create and run home scraper."""
    hfc = home.Forecast(config)
    return hfc.run()

@safe_run("Alerts")
def run_alerts(config):
    severe = alerts.Alerts(config)
    severe.run()

def nom_nom_nom():
    """I'm hongry!"""
    # Create config loader object
    config = Loader()
    # Create database injector
    db = database.Inserter(config.db_config())

    wfc_data = run_wfc(config.wfc_config())
    db.insert(statement=db.wfc_statement(), data=wfc_data)

    hfc_data = run_hfc(config.hfc_config())
    db.insert(statement=db.hfc_statement(), data=hfc_data)

    run_alerts(config.alerts_config())


if __name__ == "__main__":
    nom_nom_nom()

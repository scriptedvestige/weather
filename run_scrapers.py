#!/usr/bin/env python3
import sys
import traceback
from datetime import datetime
from functools import wraps

from utils.file_utils import log_path
from config.loader import Loader
from ingest import work, home
from output import database

LOG_PATH = log_path()

# ----- DECORATOR ----- #
def safe_run(module_name):
    """Decorator that runs a function safely, logs any exception, and returns
    False on failure instead of raising — so independent steps keep running."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                func(*args, **kwargs)
                return True
            except Exception as e:
                with open(LOG_PATH, "a") as log:
                    log.write(f"\n[{datetime.now()}] Error in {module_name}:\n")
                    log.write(f"{e}\n")
                    log.write(traceback.format_exc())
                    log.write("\n" + "-"*60 + "\n")
                return False
        return wrapper
    return decorator

def safe_fetch(module_name):
    """Like safe_run, but for functions that return data — logs and returns None on failure."""
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
                return None
        return wrapper
    return decorator

# ----- MODULE RUNNERS ----- #
@safe_fetch("Work Forecast")
def run_wfc(config):
    """Create and run work scraper."""
    wfc = work.Forecast(config)
    return wfc.run()

@safe_fetch("Home Forecast")
def run_hfc(config):
    """Create and run home scraper."""
    hfc = home.Forecast(config)
    return hfc.run()

@safe_run("Work Forecast Insert")
def insert_wfc(db, data):
    db.insert(statement=db.wfc_statement(), data=data)

@safe_run("Home Forecast Insert")
def insert_hfc(db, data):
    db.insert(statement=db.hfc_statement(), data=data)


def nom_nom_nom():
    """I'm hongry!"""
    config = Loader()
    db = database.Insert(config=config.db_config())
    ok = True

    # Run the work forecast scraper and insert into the work_forecast table.
    wfc_data = run_wfc(config=config.wfc_config())
    if wfc_data is not None:
        ok &= insert_wfc(db, wfc_data)
    else:
        ok = False

    # Run the home forecast scraper and insert into the home_forecast table.
    hfc_data = run_hfc(config=config.hfc_config())
    if hfc_data is not None:
        ok &= insert_hfc(db, hfc_data)
    else:
        ok = False

    return ok


if __name__ == "__main__":
    if not nom_nom_nom():
        sys.exit(1)

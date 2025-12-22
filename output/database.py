#!/usr/bin/env python3
import sys
sys.path.append(".")

from utils.file_utils import log_path
from datetime import datetime
import psycopg2
import traceback


class Inserter:
    """Inject data fed to the module into the appropriate database table."""
    def __init__(self, config):
        self.LOG_PATH = log_path()
        # DB Config
        self.db_host = config["host"]
        self.db_port = config["port"]
        self.db_name = config["database"]
        self.db_user = config["user"]
        self.db_password = config["password"]

    def wfc_statement(self):
        """Build the insert statement for work forecast data."""
        return """INSERT into work_forecast 
            (updated, starttime, isdaytime, temp, precip, windspeed, winddir, detail, icon) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

    def hfc_statement(self):
        """Build the insert statement for home forecast data."""
        return """INSERT into home_forecast 
            (updated, starttime, isdaytime, temp, precip, windspeed, winddir, humidity, shortfc) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    
    def swa_statement(self):
        """Build the insert statement for the severe weather alerts."""
        return """INSERT into alerts 
            (updated, onset, ends, severity, certainty, event, headline, description, instruction) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

    def insert(self, statement, data):
        """Connect to the database and insert data."""
        try:
            connection = psycopg2.connect(
                user = self.db_user,
                password = self.db_password,
                host = self.db_host,
                port = self.db_port,
                database = self.db_name)
            cursor = connection.cursor()
            cursor.executemany(statement, data)
            connection.commit()
            cursor.close()
            connection.close()
        except Exception as e:
            with open(self.LOG_PATH, "a") as log:
                    log.write(f"\n[{datetime.now()}] Error inserting into table: {statement.split()[2]}\n")
                    log.write(f"{e}\n")
                    log.write(traceback.format_exc())
                    log.write("\n" + "-"*60 + "\n")


if __name__ == "__main__":
    ### Testing ###
    """ from config import loader
    cfg = loader.Loader()
    inj = Inserter(cfg.db_config())
    stmt = inj.wfc_statement()
    inj.insert() """
    

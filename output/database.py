#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.file_utils import log_path
from datetime import datetime
import psycopg2
import traceback


class Insert:
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
            (updated, starttime, isdaytime, temp, precip, windspeed, winddir, humidity, shortfc) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""

    def hfc_statement(self):
        """Build the insert statement for home forecast data."""
        return """INSERT into home_forecast 
            (updated, starttime, isdaytime, temp, precip, windspeed, winddir, humidity, shortfc) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s);"""
    
    def swa_statement(self):
        """Build the insert statement for the severe weather alerts."""
        return """INSERT into alerts 
            (updated, onset, ends, id, severity, certainty, event, headline, description) 
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (updated, onset, id) DO NOTHING;"""
    
    def get_swa_new(self):
        """Get onset/ends/event/description for currently active alerts, used for content-based dedup."""
        return """SELECT onset, ends, event, description from alerts where ends >= NOW() order by updated desc;"""

    def query(self, statement):
        """Connect to the database and run a SELECT statement."""
        connection = None
        try:
            connection = psycopg2.connect(
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                database=self.db_name)
            cursor = connection.cursor()
            cursor.execute(statement)
            records = cursor.fetchall()
            cursor.close()
            return records
        except Exception as e:
            with open(self.LOG_PATH, "a") as log:
                log.write(f"\n[{datetime.now()}] Error querying table: {statement.split()[2]}\n")
                log.write(f"{e}\n")
                log.write(traceback.format_exc())
                log.write("\n" + "-"*60 + "\n")
            raise
        finally:
            if connection is not None:
                connection.close()

    def insert(self, statement, data):
        """Connect to the database and insert data."""
        connection = None
        try:
            connection = psycopg2.connect(
                user=self.db_user,
                password=self.db_password,
                host=self.db_host,
                port=self.db_port,
                database=self.db_name)
            cursor = connection.cursor()
            cursor.executemany(statement, data)
            connection.commit()
            cursor.close()
        except Exception as e:
            with open(self.LOG_PATH, "a") as log:
                log.write(f"\n[{datetime.now()}] Error inserting into table: {statement.split()[2]}\n")
                log.write(f"{e}\n")
                log.write(traceback.format_exc())
                log.write("\n" + "-"*60 + "\n")
            raise
        finally:
            if connection is not None:
                connection.close()


if __name__ == "__main__":
    ### Testing ###
    """ from config import loader
    cfg = loader.Loader()
    inj = Inserter(cfg.db_config())
    stmt = inj.wfc_statement()
    inj.insert() """

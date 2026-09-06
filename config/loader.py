#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from utils.file_utils import config_path, env_path
from dotenv import load_dotenv
import json
import os


class Loader:
    """
    Load and return the configuration data to pass to the other modules.
    All aboard!
    """
    def __init__(self):
        # Load .env
        load_dotenv(dotenv_path=env_path())
        self.db_name = os.getenv("DB_NAME")
        self.db_host = os.getenv("DB_HOST")
        self.db_port = os.getenv("DB_PORT")
        self.db_user = os.getenv("DB_USER")
        self.db_password = os.getenv("DB_PASS")
        # Validate .env
        if not all([self.db_name, self.db_host, self.db_port, self.db_user, self.db_password]):
            raise ValueError("Missing required database environment variables.")
        # NWS Config File
        self.path = config_path("nws")
        self.config = self.load_json()

    def load_json(self):
        """Load the NWS config file."""
        try:
            with open(self.path, "r") as config:
                return json.load(config)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            raise ValueError(f"Failed to load NWS config at {self.path}: {e}")

    def db_config(self):
        """Return database config data."""
        return {
            "host": self.db_host,
            "port": self.db_port,
            "database": self.db_name,
            "user": self.db_user,
            "password": self.db_password
        }

    def wfc_config(self):
        """Return the work forecast configuration."""
        return {
            "header": self.config["header"],
            "url": self.config["work_fc"]["url"],
            "table": self.config["work_fc"]["table"]
        }
    
    def hfc_config(self):
        """Return the home forecast configuration."""
        return {
            "header": self.config["header"],
            "url": self.config["home_fc"]["url"],
            "table": self.config["home_fc"]["table"]
        }
    
    def alerts_config(self):
        """Return the alerts configuration."""
        return {
            "header": self.config["header"],
            "url": [self.config["alerts"]["url"], self.config["fire"]["url"]],
            "table": self.config["alerts"]["table"]
        }
        

if __name__ == "__main__":
    ### Testing ###
    c = Loader()
    # print(c.db_config())
    # print(c.wfc_config())

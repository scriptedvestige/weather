#!/usr/bin/env python3

from config.loader import Loader
from ingest import work, home
from output import database

def nom_nom_nom():
    """I'm hongry!"""
    # Create config loader object
    config = Loader()
    # Create database injector
    db = database.Inserter(config.db_config())
    # Create and run work scrapers
    wfc = work.Forecast(config.wfc_config())
    wfc_data = wfc.run()
    # Insert data into database
    db.insert(statement=db.wfc_statement(),data=wfc_data)
    
    """ config.hfc_config() """


if __name__ == "__main__":
    nom_nom_nom()

#!/usr/bin/env python3

from datetime import datetime, timedelta

def iso_format():
    """Return current date in full ISO 8601 format."""
    return datetime.now().strftime("%Y-%m-%d")
    
def iso_delta(count):
    """Return ISO 8601 date for count days in the future."""
    return (datetime.now() + timedelta(days=count)).strftime("%Y-%m-%d")

def filename_format():
    """Return current date in compact ISO 8601 format for file names."""
    return datetime.now().strftime("%Y%m%d")
    
def filename_delta(count):
    """Return the date delta in filename format."""
    return (datetime.now() + timedelta(days=count)).strftime("%Y%m%d")

def current_date_time():
    """Return current date and time in format yyyy-mm-dd hh:mm:ss"""
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
    
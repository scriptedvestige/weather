#!/usr/bin/env python3

from pathlib import Path

root_dir = Path.cwd()

def check_file(path):
    """Check if a file path exists."""
    pass

def config_path(name):
    """Configuration directory path."""
    return root_dir / "config" / f"{name}_config.json"
    
def forecast_output(zone, date):
    """Daily weather output filename."""
    return root_dir / "output" / f"nws_{zone}_{date}.json"

#!/usr/bin/env python3

from pathlib import Path

def root_dir():
    """Define the path of the project root directory."""
    return Path(__file__).resolve().parent.parent

def check_file(path):
    """Check if a file path exists."""
    return Path(path).exists()

def log_path():
    """Path for orchestrator run log."""
    return root_dir() / "run.log"

def config_path(name):
    """Configuration directory path."""
    return root_dir() / "config" / f"{name}_config.json"
    
def forecast_output(zone, date):
    """Daily weather output filename."""
    return root_dir() / "output" / f"nws_{zone}_{date}.json"

def env_path():
    """Path to the project's .env file."""
    return root_dir() / ".env"

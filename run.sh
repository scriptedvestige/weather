#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG="$DIR/cron.log"

echo "Running Forecast At: $(date)" >> "$LOG" 2>&1

cd "$DIR" || { echo "Failed to cd to project dir" >> "$LOG"; exit 1; }

"$DIR/w_venv/bin/python" "$DIR/run_scrapers.py" >> "$LOG" 2>&1

echo "Finished Forecast At: $(date)" >> "$LOG" 2>&1

echo "--------------------" >> "$LOG" 2>&1

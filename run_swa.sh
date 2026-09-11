#!/bin/bash
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG="$DIR/cron.log"

echo "Running SWA At: $(date)" >> "$LOG" 2>&1

cd "$DIR" || { echo "Failed to cd to project dir" >> "$LOG"; exit 1; }

"$DIR/w_venv/bin/python" "$DIR/run_alerts.py" >> "$LOG" 2>&1

echo "Finished SWA At: $(date)" >> "$LOG" 2>&1

echo "--------------------------------------------------" >> "$LOG" 2>&1

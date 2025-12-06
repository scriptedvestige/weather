#!/bin/bash

LOG=/project/root/dir/cron.log

echo "Running At: $(date)" >> "$LOG" 2>&1

cd /project/root/dir || { echo "Failed to cd to project dir" >> "$LOG"; exit 1; }

/project/root/dir/w_venv/bin/python /project/root/dir/run_scrapers.py >> "$LOG" 2>&1

echo "Finished At: $(date)" >> "$LOG" 2>&1

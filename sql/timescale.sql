-- Create the timescaledb extension:
CREATE EXTENSION IF NOT EXISTS timescaledb;

-- Convert table to timescaledb hypertable:
SELECT create_hypertable('work_forecast', 'updated');
CREATE TABLE home_forecast (
    updated TIMESTAMPTZ NOT NULL,
    starttime TIMESTAMPTZ NOT NULL,
    isdaytime BOOLEAN NOT NULL,
    temp DOUBLE PRECISION,
    precip DOUBLE PRECISION,
    windspeed DOUBLE PRECISION,
    winddir TEXT,
    humidity DOUBLE PRECISION,
    shortfc TEXT,
    PRIMARY KEY (starttime, updated)
);

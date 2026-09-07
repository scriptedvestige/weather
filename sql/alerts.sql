CREATE TABLE alerts (
    updated TIMESTAMPTZ NOT NULL,
    onset TIMESTAMPTZ NOT NULL,
    ends TIMESTAMPTZ NOT NULL,
    id TEXT,
    severity TEXT,
    certainty TEXT,
    event TEXT,
    headline TEXT,
    description TEXT,
    PRIMARY KEY (updated, onset, id)
);

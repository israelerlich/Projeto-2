CREATE TABLE IF NOT EXISTS visit_counter (
    id SERIAL PRIMARY KEY,
    label TEXT UNIQUE NOT NULL,
    total INTEGER NOT NULL DEFAULT 0
);

INSERT INTO visit_counter (label, total)
VALUES ('homepage', 0)
ON CONFLICT (label) DO NOTHING;

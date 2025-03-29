CREATE TABLE endpoint_calls (
    id SERIAL PRIMARY KEY,
    endpoint VARCHAR(50) NOT NULL,
    call_count int
);
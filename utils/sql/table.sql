CREATE TABLE IF NOT EXISTS transaction
(
    event_id String,
    timestamp String,
    consumer_id String,
    bank_id String,
    amount Float64,
    country_code String,
    execution_date String,
    merchant_id String
) ENGINE = MergeTree()
ORDER BY event_id
PRIMARY KEY event_id
{# TTL timestamp + INTERVAL 60 DAY #}
-- Replace the topic and columns with values for the Debezium table being
-- replicated.
SET 'execution.checkpointing.interval' = '10 s';
SET 'execution.checkpointing.mode' = 'EXACTLY_ONCE';

CREATE TEMPORARY TABLE customers_cdc (
  id BIGINT,
  first_name STRING,
  last_name STRING,
  email STRING,
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
  'connector' = 'kafka',
  'topic' = 'dbserver1.public.customers',
  'properties.bootstrap.servers' = 'kafka-4-backend:29092',
  'properties.group.id' = 'flink-delta-customers',
  'properties.security.protocol' = 'SSL',
  'properties.ssl.truststore.location' = '/etc/kafka/tls/ca.crt',
  'properties.ssl.truststore.type' = 'PEM',
  'scan.startup.mode' = 'earliest-offset',
  'value.format' = 'debezium-json'
);

CREATE TEMPORARY TABLE customers_delta (
  id BIGINT,
  first_name STRING,
  last_name STRING,
  email STRING,
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
  'connector' = 'delta',
  'table_path' = 's3://delta-lakehouse/customers',
  'write.mode' = 'upsert',
  'schema_evolution.mode' = 'newcolumn'
);

INSERT INTO customers_delta
SELECT id, first_name, last_name, email
FROM customers_cdc;

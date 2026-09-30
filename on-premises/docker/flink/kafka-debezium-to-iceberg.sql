-- Replace the topic and columns with values for the Debezium table being
-- replicated. The source and sink primary keys must match.
SET 'execution.checkpointing.interval' = '10 s';
SET 'execution.checkpointing.mode' = 'EXACTLY_ONCE';

CREATE CATALOG iceberg_catalog WITH (
  'type' = 'iceberg',
  'catalog-type' = 'hadoop',
  'warehouse' = 's3://trino-lakehouse/flink-cdc',
  'io-impl' = 'org.apache.iceberg.aws.s3.S3FileIO',
  's3.endpoint' = 'http://rustfs-http:9000',
  's3.path-style-access' = 'true',
  'client.region' = 'us-east-1'
);

CREATE DATABASE IF NOT EXISTS iceberg_catalog.public;

CREATE TABLE IF NOT EXISTS iceberg_catalog.public.customers (
  id BIGINT,
  first_name STRING,
  last_name STRING,
  email STRING,
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
  'format-version' = '2',
  'write.upsert.enabled' = 'true'
);

CREATE TEMPORARY TABLE customers_cdc (
  id BIGINT,
  first_name STRING,
  last_name STRING,
  email STRING,
  PRIMARY KEY (id) NOT ENFORCED
) WITH (
  'connector' = 'kafka',
  'topic' = 'postgres.public.customers',
  'properties.bootstrap.servers' = 'kafka-4-backend:29092',
  'properties.group.id' = 'flink-iceberg-customers',
  'properties.security.protocol' = 'SSL',
  'properties.ssl.truststore.location' = '/etc/kafka/tls/ca.crt',
  'properties.ssl.truststore.type' = 'PEM',
  'scan.startup.mode' = 'earliest-offset',
  'value.format' = 'debezium-json'
);

INSERT INTO iceberg_catalog.public.customers
SELECT id, first_name, last_name, email
FROM customers_cdc;

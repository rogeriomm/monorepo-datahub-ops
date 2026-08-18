#!/usr/bin/env zsh

DIR="../docker"

echo "Postgres"

openssl x509 \
  -in $DIR/postgres/certificates/server.crt \
  -noout \
  -text


echo "Trino"

openssl x509 \
  -in $DIR/trino/certificates/trino.crt \
  -noout \
  -text

echo "Kafka"


echo "SeaweedFS"

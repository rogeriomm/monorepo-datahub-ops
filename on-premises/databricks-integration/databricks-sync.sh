#!/usr/bin/env zsh

cd ..

databricks bundle validate --strict

databricks bundle deploy

databricks bundle run put-trino-client-keystore-password

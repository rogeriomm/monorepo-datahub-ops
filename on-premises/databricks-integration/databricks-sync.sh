#!/usr/bin/env zsh

cd ..

databricks bundle validate --strict

databricks bundle deploy

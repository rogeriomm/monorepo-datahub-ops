#!/usr/bin/env bash

if [[ -n "$1" ]]; then
  ansible-playbook playbook.yml -K "$1"
else
  ansible-playbook playbook.yml -K
fi


#!/bin/sh

set -eu

token_file="$(dirname "$0")/obsidian-rag-token"

if [ ! -r "$token_file" ]; then
  echo "Obsidian RAG token file is missing or unreadable: $token_file" >&2
  exit 1
fi

token=$(sed -n '1p' "$token_file")

case "$token" in
  omcp_*) ;;
  *)
    echo "Obsidian RAG token file does not contain an omcp_ key" >&2
    exit 1
    ;;
esac

printf '{"Authorization":"Bearer %s"}\n' "$token"

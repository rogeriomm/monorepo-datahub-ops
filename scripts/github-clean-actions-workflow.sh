#!/usr/bin/env bash
set -euo pipefail

# Disable the pager so we get raw output
export GH_PAGER=cat

OWNER="rogeriomm"
REPO="$1"

echo "⏳  Fetching all workflow run IDs for $OWNER/$REPO…"

# --paginate will walk through all pages of the REST endpoint
run_ids=$(gh api --paginate \
                 -H "Accept: application/vnd.github+json" \
                 /repos/$OWNER/$REPO/actions/runs \
                 --jq '.workflow_runs[].id')

if [[ -z "$run_ids" ]]; then
  echo "✔️  No workflow runs found—nothing to delete."
  exit 0
fi

count=$(wc -w <<<"$run_ids")
echo "⚠️  Found $count runs. Deleting them now…"

for id in $run_ids; do
  printf " → Deleting run %-6s… " "$id"
  gh api --method DELETE \
         -H "Accept: application/vnd.github+json" \
         /repos/$OWNER/$REPO/actions/runs/$id \
         --silent \
    && echo "done"
done

echo "✅  All workflow runs deleted."


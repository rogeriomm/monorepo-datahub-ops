#!/usr/bin/env bash
set -euo pipefail

#–– 1) Disable the interactive pager just for this script
export GH_PAGER=cat

#–– 2) Repo coordinates
OWNER="rogeriomm"
REPO="monorepo-datahub-ops"

#–– 3) Fetch & delete logs
for run_id in $(gh run list --repo "$OWNER/$REPO" \
                           --limit 1000 \
                           --json id \
                           -q '.[].id'); do
  echo "→ Deleting logs for run #$run_id…"
  http_status=$(gh api \
    --method DELETE \
    "/repos/$OWNER/$REPO/actions/runs/$run_id/logs" \
    --silent --write-status)
  if [[ "$http_status" != "204" ]]; then
    echo "  ⚠️  unexpected HTTP status: $http_status" >&2
  fi
done

echo "✅ Done. All logs deleted."


#!/bin/zsh

# Ensure we are in a git repo
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  echo "Not inside a Git repository."
  exit 1
fi

# Get repo in owner/name format
REPO=$(gh repo view --json nameWithOwner -q .nameWithOwner)

# Get all running workflow run IDs
RUN_IDS=($(gh run list --repo "$REPO" --limit 100 --status in_progress --json databaseId -q '.[].databaseId'))

if [[ ${#RUN_IDS[@]} -eq 0 ]]; then
  echo "No in-progress runs to cancel."
  exit 0
fi

# Cancel each run

for run_id in "${RUN_IDS[@]}"; do
  echo "Cancelling run: $run_id"
  gh run cancel "$run_id" --repo "$REPO"
done

echo "✅ All applicable runs have been canceled."

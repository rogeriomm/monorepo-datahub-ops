#!/usr/bin/env bash
set -euo pipefail

POD_NAME="debug"
IMAGE="ubuntu:22.04"

# 1. If the debug pod doesn't exist, launch it running tail -f so it never exits
if ! kubectl get pod "${POD_NAME}" &>/dev/null; then
  echo "🚀 Creating debug pod '${POD_NAME}'…"
  kubectl run "${POD_NAME}" \
    --restart=Never \
    --image="${IMAGE}" \
    --command -- \
    tail -f /dev/null

  echo "⏳ Waiting for pod to be Ready…"
  kubectl wait --for=condition=Ready pod/"${POD_NAME}" --timeout=60s
else
  echo "⏩ Reusing existing pod '${POD_NAME}'."
fi

# 2. Exec you into a full login bash shell
kubectl exec -it "${POD_NAME}" -- bash -il


#!/usr/bin/env zsh

kubectl get services -n pg-sample
PWD=$(kubectl get secret cluster-sample-app -n pg-sample -o jsonpath='{.data.password}' | base64 -d)

USER="app"
read -r IP PORT <<< "$(kubectl -n pg-sample get service pg-cluster-external \
        -o jsonpath='{.status.loadBalancer.ingress[0].ip}{" "}{.spec.ports[0].targetPort}')"

echo "${USER}@${IP}:${PORT} ${PWD}"

kubectl get secret cluster-sample-ca -n pg-sample -o jsonpath='{.data.ca\.crt}' | base64 -d > ca.crt

echo "
 select datname from pg_database;
 select 1;
 \q
"

PGPASSWORD="${PWD}" psql "postgresql://${USER}@${IP}:${PORT}/app?sslmode=verify-ca&sslrootcert=ca.crt"

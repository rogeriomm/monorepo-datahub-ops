# https://www.gabrielebartolini.it/articles/2024/03/cloudnativepg-recipe-3-what-no-superuser-access/
# https://www.gabrielebartolini.it/articles/2025/09/run-postgresql-18-on-kubernetes-today-with-cloudnativepg/
kubectl exec -ti -c postgres cluster-sample-1 \
  -- psql -c 'SELECT type, database, user_name, address,
              auth_method, options FROM pg_hba_file_rules
              ORDER BY rule_number'


kubectl exec -ti -c postgres cluster-sample-1 -- psql -c 'SELECT usename FROM pg_shadow WHERE passwd IS NULL'

kubectl get secret cluster-sample-app -n pg-sample -o jsonpath='{.data.password}' | base64 -d
kubectl get secret cluster-sample-ca -n pg-sample -o jsonpath='{.data.ca\.crt}' | base64 -d > ca.crt
openssl x509 -in ca.crt -text -noout
mkdir -p ~/.postgresql
cp ca.crt ~/.postgresql/root.crt



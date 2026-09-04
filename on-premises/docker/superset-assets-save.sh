docker compose exec superset \
  superset export_datasources -f /app/superset-assets/datasources.zip

docker compose exec superset \
  superset export-dashboards -f /app/superset-assets/dashboards.zip
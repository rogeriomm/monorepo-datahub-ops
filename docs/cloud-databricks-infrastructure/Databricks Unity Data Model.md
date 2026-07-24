# Databricks Unity Catalog — Entity Relationship Model

## Core object hierarchy

```mermaid
erDiagram
    METASTORE ||--o{ CATALOG : contains
    CATALOG ||--o{ SCHEMA : contains

    SCHEMA ||--o{ TABLE : contains
    SCHEMA ||--o{ VIEW : contains
    SCHEMA ||--o{ MATERIALIZED_VIEW : contains
    SCHEMA ||--o{ METRIC_VIEW : contains
    SCHEMA ||--o{ VOLUME : contains
    SCHEMA ||--o{ ROUTINE : contains
    SCHEMA ||--o{ MODEL : contains
    SCHEMA ||--o{ SERVICE : contains
    SCHEMA ||--o{ SECRET : contains
    SCHEMA ||--o{ FEATURE : contains

    TABLE ||--o{ COLUMN : contains
    VIEW ||--o{ COLUMN : exposes
    MATERIALIZED_VIEW ||--o{ COLUMN : exposes
    METRIC_VIEW ||--o{ COLUMN : exposes

    TABLE ||--o{ CONSTRAINT : defines
    CONSTRAINT ||--o{ CONSTRAINT_COLUMN : uses
    COLUMN ||--o{ CONSTRAINT_COLUMN : participates_in

    TABLE ||--o{ INDEX : defines
    INDEX ||--o{ INDEX_COLUMN : uses
    COLUMN ||--o{ INDEX_COLUMN : participates_in

    ROUTINE ||--o{ ROUTINE_PARAMETER : accepts
    ROUTINE ||--o| ROUTINE_RETURN : returns

    MODEL ||--o{ MODEL_VERSION : contains
```

## Information Schema entities

```mermaid
erDiagram
    CATALOGS ||--o{ SCHEMATA : contains

    SCHEMATA ||--o{ TABLES : contains
    SCHEMATA ||--o{ VIEWS : contains
    SCHEMATA ||--o{ ROUTINES : contains
    SCHEMATA ||--o{ VOLUMES : contains

    TABLES ||--o{ COLUMNS : contains
    TABLES ||--o{ TABLE_CONSTRAINTS : defines
    TABLES ||--o{ TABLE_PRIVILEGES : receives
    TABLES ||--o{ COLUMN_TAGS : classifies
    TABLES ||--o{ TABLE_TAGS : classifies

    VIEWS ||--o{ VIEW_TABLE_USAGE : depends_on
    VIEWS ||--o{ VIEW_COLUMN_USAGE : depends_on
    VIEWS ||--o{ VIEW_ROUTINE_USAGE : invokes

    ROUTINES ||--o{ PARAMETERS : accepts
    ROUTINES ||--o{ ROUTINE_COLUMNS : returns
    ROUTINES ||--o{ ROUTINE_PRIVILEGES : receives

    TABLE_CONSTRAINTS ||--o{ KEY_COLUMN_USAGE : uses
    TABLE_CONSTRAINTS ||--o{ CONSTRAINT_COLUMN_USAGE : references
    TABLE_CONSTRAINTS ||--o{ REFERENTIAL_CONSTRAINTS : participates_in

    CATALOGS ||--o{ CATALOG_PRIVILEGES : receives
    SCHEMATA ||--o{ SCHEMA_PRIVILEGES : receives
    COLUMNS ||--o{ COLUMN_PRIVILEGES : receives

    CATALOGS ||--o{ CATALOG_TAGS : classifies
    SCHEMATA ||--o{ SCHEMA_TAGS : classifies
    COLUMNS ||--o{ COLUMN_TAGS : classifies

    VOLUMES ||--o{ VOLUME_PRIVILEGES : receives
    VOLUMES ||--o{ VOLUME_TAGS : classifies
```

## Simplified logical hierarchy

```text
Metastore
└── Catalog
    └── Schema
        ├── Table
        │   ├── Column
        │   ├── Constraint
        │   ├── Tag
        │   └── Privilege
        │
        ├── View
        │   ├── Column
        │   ├── Table dependency
        │   ├── Column dependency
        │   ├── Routine dependency
        │   ├── Tag
        │   └── Privilege
        │
        ├── Materialized view
        ├── Metric view
        │
        ├── Routine
        │   ├── Parameter
        │   ├── Return column
        │   ├── Tag
        │   └── Privilege
        │
        ├── Volume
        │   ├── Tag
        │   └── Privilege
        │
        ├── Model
        │   └── Model version
        │
        ├── Service
        ├── Secret
        └── Feature
```

## Metastore-level entities

```mermaid
erDiagram
    METASTORE ||--o{ CATALOG : contains

    METASTORE ||--o{ STORAGE_CREDENTIAL : contains
    METASTORE ||--o{ SERVICE_CREDENTIAL : contains
    METASTORE ||--o{ EXTERNAL_LOCATION : contains
    METASTORE ||--o{ CONNECTION : contains
    METASTORE ||--o{ EXTERNAL_METADATA : contains

    METASTORE ||--o{ SHARE : contains
    METASTORE ||--o{ PROVIDER : contains
    METASTORE ||--o{ RECIPIENT : contains
    METASTORE ||--o{ CLEAN_ROOM : contains

    STORAGE_CREDENTIAL ||--o{ EXTERNAL_LOCATION : authorizes
    SERVICE_CREDENTIAL ||--o{ CONNECTION : authenticates

    CONNECTION ||--o{ FOREIGN_CATALOG : exposes
    FOREIGN_CATALOG ||--o{ FOREIGN_SCHEMA : contains
    FOREIGN_SCHEMA ||--o{ FOREIGN_TABLE : contains

    SHARE }o--o{ TABLE : includes
    SHARE }o--o{ VIEW : includes
    SHARE }o--o{ VOLUME : includes
    SHARE }o--o{ RECIPIENT : granted_to

    PROVIDER ||--o{ PROVIDER_SHARE : provides
    PROVIDER_SHARE ||--o{ SHARED_CATALOG : mounted_as

    CLEAN_ROOM }o--o{ SHARE : uses
    CLEAN_ROOM }o--o{ CATALOG : collaborates_with
```

## Governance relationships

```mermaid
erDiagram
    PRINCIPAL ||--o{ GRANT : receives
    SECURABLE_OBJECT ||--o{ GRANT : protected_by
    PRIVILEGE ||--o{ GRANT : assigns

    PRINCIPAL {
    }

    SECURABLE_OBJECT {
    }

    PRIVILEGE {
    }

    GRANT {
    }

    TAG ||--o{ TAG_ASSIGNMENT : assigned_through
    SECURABLE_OBJECT ||--o{ TAG_ASSIGNMENT : classified_by

    POLICY }o--o{ PRINCIPAL : applies_to
    POLICY }o--o{ SECURABLE_OBJECT : governs

    TABLE ||--o{ ROW_FILTER : governed_by
    COLUMN ||--o{ COLUMN_MASK : governed_by

    ROUTINE ||--o{ ROW_FILTER : implements
    ROUTINE ||--o{ COLUMN_MASK : implements
```

## Data lineage relationships

```mermaid
erDiagram
    TABLE }o--o{ TABLE : data_lineage
    VIEW }o--o{ TABLE : depends_on
    VIEW }o--o{ VIEW : depends_on
    MATERIALIZED_VIEW }o--o{ TABLE : depends_on
    MATERIALIZED_VIEW }o--o{ VIEW : depends_on

    COLUMN }o--o{ COLUMN : column_lineage

    NOTEBOOK }o--o{ TABLE : reads_or_writes
    JOB }o--o{ TABLE : reads_or_writes
    PIPELINE }o--o{ TABLE : produces_or_consumes
    DASHBOARD }o--o{ TABLE : queries

    EXTERNAL_METADATA }o--o{ TABLE : lineage_to
    EXTERNAL_METADATA }o--o{ EXTERNAL_METADATA : lineage_to
```

# SQL metadata queries

## Catalogs

```sql
SELECT *
FROM system.information_schema.catalogs;
```

## Schemas

```sql
SELECT *
FROM system.information_schema.schemata;
```

## Tables and views

The `TABLES` relation contains tables, views, materialized views, streaming tables and other relation types.

```sql
SELECT *
FROM system.information_schema.tables;
```

## Columns

```sql
SELECT *
FROM system.information_schema.columns;
```

## Views

```sql
SELECT *
FROM system.information_schema.views;
```

## Volumes

```sql
SELECT *
FROM system.information_schema.volumes;
```

## Routines

```sql
SELECT *
FROM system.information_schema.routines;
```

## Routine parameters

```sql
SELECT *
FROM system.information_schema.parameters;
```

## Routine return columns

```sql
SELECT *
FROM system.information_schema.routine_columns;
```

## Table constraints

```sql
SELECT *
FROM system.information_schema.table_constraints;
```

## Constraint columns

```sql
SELECT *
FROM system.information_schema.key_column_usage;
```

## Foreign-key relationships

```sql
SELECT *
FROM system.information_schema.referential_constraints;
```

## View-to-table dependencies

```sql
SELECT *
FROM system.information_schema.view_table_usage;
```

## View-to-column dependencies

```sql
SELECT *
FROM system.information_schema.view_column_usage;
```

## View-to-routine dependencies

```sql
SELECT *
FROM system.information_schema.view_routine_usage;
```

## Catalog privileges

```sql
SELECT *
FROM system.information_schema.catalog_privileges;
```

## Schema privileges

```sql
SELECT *
FROM system.information_schema.schema_privileges;
```

## Table privileges

```sql
SELECT *
FROM system.information_schema.table_privileges;
```

## Column privileges

```sql
SELECT *
FROM system.information_schema.column_privileges;
```

## Routine privileges

```sql
SELECT *
FROM system.information_schema.routine_privileges;
```

## Volume privileges

```sql
SELECT *
FROM system.information_schema.volume_privileges;
```

## Catalog tags

```sql
SELECT *
FROM system.information_schema.catalog_tags;
```

## Schema tags

```sql
SELECT *
FROM system.information_schema.schema_tags;
```

## Table tags

```sql
SELECT *
FROM system.information_schema.table_tags;
```

## Column tags

```sql
SELECT *
FROM system.information_schema.column_tags;
```

## Volume tags

```sql
SELECT *
FROM system.information_schema.volume_tags;
```

# Query to enumerate available Information Schema entities

This query lists the metadata views that are actually available in your Databricks environment:

```sql
SELECT
    table_name AS entity_name
FROM system.information_schema.tables
WHERE table_catalog = 'system'
  AND table_schema = 'information_schema'
ORDER BY table_name;
```

# Query to generate the Catalog → Schema → Relation hierarchy

```sql
SELECT
    c.catalog_name,
    s.schema_name,
    t.table_name,
    t.table_type
FROM system.information_schema.catalogs AS c
LEFT JOIN system.information_schema.schemata AS s
    ON c.catalog_name = s.catalog_name
LEFT JOIN system.information_schema.tables AS t
    ON s.catalog_name = t.table_catalog
   AND s.schema_name = t.table_schema
ORDER BY
    c.catalog_name,
    s.schema_name,
    t.table_name;
```

# Query to extract declared foreign-key relationships

```sql
SELECT
    fk.constraint_catalog,
    fk.constraint_schema,
    fk.constraint_name,

    fk.table_catalog AS child_catalog,
    fk.table_schema AS child_schema,
    fk.table_name AS child_table,

    pk.table_catalog AS parent_catalog,
    pk.table_schema AS parent_schema,
    pk.table_name AS parent_table

FROM system.information_schema.referential_constraints AS rc

JOIN system.information_schema.table_constraints AS fk
    ON rc.constraint_catalog = fk.constraint_catalog
   AND rc.constraint_schema = fk.constraint_schema
   AND rc.constraint_name = fk.constraint_name

JOIN system.information_schema.table_constraints AS pk
    ON rc.unique_constraint_catalog = pk.constraint_catalog
   AND rc.unique_constraint_schema = pk.constraint_schema
   AND rc.unique_constraint_name = pk.constraint_name

ORDER BY
    child_catalog,
    child_schema,
    child_table,
    parent_catalog,
    parent_schema,
    parent_table;
```

# Conceptual model

```text
Principal
    │
    └── receives Privilege
            │
            └── on Securable Object

Securable Object
    ├── Metastore
    ├── Catalog
    ├── Schema
    ├── Table
    ├── View
    ├── Volume
    ├── Routine
    ├── Model
    ├── Service
    ├── Secret
    ├── Feature
    ├── Storage Credential
    ├── Service Credential
    ├── External Location
    ├── Connection
    ├── Share
    ├── Provider
    ├── Recipient
    ├── Clean Room
    └── External Metadata
```
# See also
 - [[unity-catalog.ipynb]]
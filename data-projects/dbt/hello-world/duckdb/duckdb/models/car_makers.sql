{{ config(materialized='table') }}

select
    id,
    description as maker
from {{ source('car', 'maker') }}
order by id

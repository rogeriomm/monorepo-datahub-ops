SELECT country_code, country_name
FROM {{ ref('country_codes')}}
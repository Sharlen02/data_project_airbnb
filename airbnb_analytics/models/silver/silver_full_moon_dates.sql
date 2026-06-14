WITH source AS (

    SELECT *
    FROM {{ ref('seed_full_moon_dates') }}

)

SELECT
    CAST(full_moon_date AS DATE) AS full_moon_date

FROM source
WHERE full_moon_date IS NOT NULL
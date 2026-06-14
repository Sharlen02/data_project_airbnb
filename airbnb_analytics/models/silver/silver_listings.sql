{{ config(materialized='table', schema='silver') }}

SELECT
    CAST(id AS INTEGER) AS listing_id,
    listing_url,
    TRIM(name) AS listing_name,
    LOWER(TRIM(room_type)) AS room_type,
    CAST(minimum_nights AS INTEGER) AS minimum_nights,
    CAST(host_id AS INTEGER) AS host_id,

    CAST(
        REPLACE(REPLACE(TRIM(price), '$', ''), ',', '')
        AS DOUBLE
    ) AS price,

    created_at::TIMESTAMP AS created_at,
    updated_at::TIMESTAMP AS updated_at

FROM {{ ref('bronze_listings') }}

WHERE id IS NOT NULL
  AND price IS NOT NULL
  AND TRIM(price) != ''
  AND TRIM(price) != '$0.00'
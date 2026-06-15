{{ config(materialized='table', schema='gold') }}

SELECT
    room_type,
    COUNT(*)                        AS nb_listings,
    ROUND(AVG(price), 2)            AS avg_price,
    ROUND(MIN(price), 2)            AS min_price,
    ROUND(MAX(price), 2)            AS max_price,
    ROUND(AVG(minimum_nights), 1)   AS avg_min_nights

FROM {{ ref('silver_listings') }}

GROUP BY room_type
ORDER BY avg_price DESC 
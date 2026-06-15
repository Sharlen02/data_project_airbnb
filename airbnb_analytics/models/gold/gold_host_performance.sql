{{ config(materialized='table', schema='gold') }}

SELECT
    h.host_is_superhost,
    COUNT(DISTINCT h.host_id)    AS nb_hosts,
    COUNT(DISTINCT l.listing_id) AS nb_listings,
    ROUND(AVG(l.price), 2)       AS avg_price,
    ROUND(MIN(l.price), 2)       AS min_price,
    ROUND(MAX(l.price), 2)       AS max_price,
    COUNT(r.listing_id)          AS nb_reviews

FROM {{ ref('silver_hosts') }}          h
LEFT JOIN {{ ref('silver_listings') }}  l ON l.host_id = h.host_id
LEFT JOIN {{ ref('silver_reviews') }}   r ON r.listing_id = l.listing_id

GROUP BY h.host_is_superhost
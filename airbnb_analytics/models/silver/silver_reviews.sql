{{ config(materialized='table', schema='silver') }}

SELECT
    ROW_NUMBER() OVER () AS review_id,
    CAST(r.listing_id AS INTEGER) AS listing_id,
    r.date::DATE AS review_date,
    TRIM(r.reviewer_name) AS reviewer_name,
    TRIM(r.comments) AS comments,
    LOWER(TRIM(r.sentiment)) AS sentiment

FROM {{ ref('bronze_reviews') }} r

INNER JOIN {{ ref('silver_listings') }} l
    ON CAST(r.listing_id AS INTEGER) = l.listing_id

WHERE r.listing_id IS NOT NULL
  AND r.date IS NOT NULL
  AND r.sentiment IS NOT NULL
  AND TRIM(r.sentiment) != ''
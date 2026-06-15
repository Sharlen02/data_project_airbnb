{{ config(materialized='table', schema='gold') }}

SELECT
    DATE_TRUNC('month', review_date)    AS review_month,
    sentiment,
    COUNT(*)                            AS nb_reviews

FROM {{ ref('silver_reviews') }}

GROUP BY review_month, sentiment
ORDER BY review_month, sentiment
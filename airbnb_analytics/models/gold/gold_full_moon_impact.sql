{{ config(materialized='table', schema='gold') }}

WITH full_moon_days AS (
    SELECT full_moon_date
    FROM {{ ref('silver_full_moon_dates') }}
),

reviews_with_context AS (
    SELECT
        r.review_date,
        r.sentiment,
        CASE
            WHEN r.review_date IN (SELECT full_moon_date FROM full_moon_days)
            THEN 'Pleine lune'
            ELSE 'Nuit normale'
        END AS period_type
    FROM {{ ref('silver_reviews') }} r
)

SELECT
    period_type,
    sentiment,
    COUNT(*)                            AS nb_reviews,
    ROUND(
        COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY period_type),
        2
    )                                   AS pct_within_period

FROM reviews_with_context

GROUP BY period_type, sentiment
ORDER BY period_type, sentiment
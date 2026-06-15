-- Échoue si le total des pourcentages par période ne fait pas 100%
SELECT
    period_type,
    ROUND(SUM(pct_within_period), 0) AS total_pct
FROM {{ ref('gold_full_moon_impact') }}
GROUP BY period_type
HAVING ROUND(SUM(pct_within_period), 0) != 100
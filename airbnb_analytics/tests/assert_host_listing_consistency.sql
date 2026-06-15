-- Échoue si Gold contient plus de listings que Silver
SELECT *
FROM (
    SELECT COUNT(DISTINCT listing_id) AS silver_count
    FROM {{ ref('silver_listings') }}
) s,
(
    SELECT SUM(nb_listings) AS gold_count
    FROM {{ ref('gold_listings_summary') }}
) g
WHERE g.gold_count > s.silver_count
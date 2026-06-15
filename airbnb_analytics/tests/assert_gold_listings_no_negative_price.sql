-- Échoue si avg_price ou min_price sont négatifs dans Gold
SELECT *
FROM {{ ref('gold_listings_summary') }}
WHERE avg_price < 0
   OR min_price < 0
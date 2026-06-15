-- Échoue si minimum_nights est négatif ou nul
SELECT *
FROM {{ ref('silver_listings') }}
WHERE minimum_nights <= 0
-- Échoue si des prix négatifs ou nuls existent
SELECT *
FROM {{ ref('silver_listings') }}
WHERE price <= 0
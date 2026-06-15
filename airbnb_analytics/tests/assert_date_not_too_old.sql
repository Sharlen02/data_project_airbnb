-- Échoue si des avis ont une date avant 2008 (création Airbnb)
SELECT *
FROM {{ ref('silver_reviews') }}
WHERE review_date < '2008-01-01'
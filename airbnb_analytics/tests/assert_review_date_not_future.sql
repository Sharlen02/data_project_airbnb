-- Échoue si des avis ont une date dans le futur
SELECT *
FROM {{ ref('silver_reviews') }}
WHERE review_date > CURRENT_DATE
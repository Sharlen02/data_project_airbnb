-- Échoue si des valeurs de sentiment inattendues existent
SELECT *
FROM {{ ref('silver_reviews') }}
WHERE sentiment NOT IN ('positive', 'negative', 'neutral')
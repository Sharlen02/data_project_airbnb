WITH source AS (

    SELECT *
    FROM {{ ref('bronze_hosts') }}

),

renamed AS (

    SELECT
        CAST(id AS INTEGER) AS host_id,
        TRIM(name) AS host_name,

        CASE
            WHEN is_superhost = 1 THEN TRUE
            WHEN is_superhost = 0 THEN FALSE
            ELSE NULL
        END AS host_is_superhost,

        CAST(created_at AS TIMESTAMP) AS created_at,
        CAST(updated_at AS TIMESTAMP) AS updated_at

    FROM source
    WHERE id IS NOT NULL

)

SELECT *
FROM renamed
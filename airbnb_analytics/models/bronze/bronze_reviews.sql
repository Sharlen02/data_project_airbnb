{{ config(materialized='table', schema='bronze') }}

SELECT * FROM {{ ref('reviews') }}
{{ config(materialized='table') }}

select * from read_csv_auto(
    'seeds/reviews.csv',
    ignore_errors=true,
    strict_mode=false
)

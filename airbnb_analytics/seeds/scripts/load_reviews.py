import duckdb
import os

base     = os.path.dirname(os.path.abspath(__file__))
db_path  = os.path.join(base, '..', '..', 'dev.duckdb')
csv_path = os.path.join(base, '..', 'reviews.csv')

con = duckdb.connect(db_path)

# Créer le schema s'il n'existe pas
con.execute("CREATE SCHEMA IF NOT EXISTS main_seeds")

con.execute("""
    CREATE OR REPLACE TABLE main_seeds.reviews AS
    SELECT *
    FROM read_csv(
        ?,
        columns = {
            'listing_id':    'INTEGER',
            'date':          'TIMESTAMP',
            'reviewer_name': 'VARCHAR',
            'comments':      'VARCHAR',
            'sentiment':     'VARCHAR'
        },
        ignore_errors = true,
        strict_mode   = false
    )
""", [csv_path])

count = con.execute("SELECT COUNT(*) AS nb FROM main_seeds.reviews").fetchone()[0]
print(f"Reviews chargées : {count} lignes")
con.close() 
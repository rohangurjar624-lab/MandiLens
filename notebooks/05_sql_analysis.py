

import pandas as pd
import sqlite3
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent

csv_path = project_folder / "data" / "cleaned_mandi_prices.csv"
db_path = project_folder / "data" / "mandilens.db"

# Read cleaned data
df = pd.read_csv(csv_path)

# Create database and table
with sqlite3.connect(db_path) as conn:
    df.to_sql(
        "mandi_prices",
        conn,
        if_exists="replace",
        index=False
    )

    print("--- TOTAL RECORDS ---")
    result = pd.read_sql_query(
        "SELECT COUNT(*) AS total_records FROM mandi_prices",
        conn
    )
    print(result.to_string(index=False))

    print("\n--- STATE-WISE RECORD COUNT ---")
    result = pd.read_sql_query("""
        SELECT State, COUNT(*) AS total_records
        FROM mandi_prices
        GROUP BY State
        ORDER BY total_records DESC
        LIMIT 10
    """, conn)
    print(result.to_string(index=False))

    print("\n--- TOP 10 COMMODITIES ---")
    result = pd.read_sql_query("""
        SELECT Commodity, COUNT(*) AS total_records
        FROM mandi_prices
        GROUP BY Commodity
        ORDER BY total_records DESC
        LIMIT 10
    """, conn)
    print(result.to_string(index=False))

    # Madhya Pradesh commodity price analysis
    print("\n--- MADHYA PRADESH: COMMODITY PRICE ANALYSIS ---")

    result = pd.read_sql_query("""
        SELECT
            Commodity,
            COUNT(*) AS market_records,
            ROUND(AVG(Modal_Price), 2) AS avg_modal_price,
            MIN(Modal_Price) AS lowest_modal_price,
            MAX(Modal_Price) AS highest_modal_price
        FROM mandi_prices
        WHERE State = 'Madhya Pradesh'
        GROUP BY Commodity
        ORDER BY avg_modal_price DESC
    """, conn)

    print(result.to_string(index=False))

    result.to_csv(
        project_folder / "data" / "mp_commodity_summary.csv",
        index=False
    )

    print("\nMP summary exported successfully!")

print("\nDatabase saved at:", db_path)


import pandas as pd
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
file_path = project_folder / "data" / "madhya_pradesh_prices.csv"

df = pd.read_csv(file_path)

modal_col = "Modal_x0020_Price"

# Highest-priced commodities
print("\n--- TOP 10 HIGHEST MODAL PRICES ---")
highest = df.sort_values(by=modal_col, ascending=False)

print(
    highest[["District", "Market", "Commodity", modal_col]]
    .head(10)
    .to_string(index=False)
)

# Lowest-priced commodities
print("\n--- TOP 10 LOWEST MODAL PRICES ---")
lowest = df.sort_values(by=modal_col, ascending=True)

print(
    lowest[["District", "Market", "Commodity", modal_col]]
    .head(10)
    .to_string(index=False)
)

# Average price by commodity
print("\n--- AVERAGE PRICE BY COMMODITY ---")
average_prices = (
    df.groupby("Commodity")[modal_col]
    .mean()
    .sort_values(ascending=False)
)

print(average_prices.to_string())

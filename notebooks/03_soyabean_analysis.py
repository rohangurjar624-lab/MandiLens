
import pandas as pd
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
file_path = project_folder / "data" / "madhya_pradesh_prices.csv"

df = pd.read_csv(file_path)

soyabean = df[
    df["Commodity"].str.strip().str.lower() == "soyabean"
].copy()

print("Total Soyabean records:", len(soyabean))

if soyabean.empty:
    print("No Soyabean records found.")
else:
    columns = [
        "District",
        "Market",
        "Variety",
        "Min_x0020_Price",
        "Max_x0020_Price",
        "Modal_x0020_Price"
    ]

    soyabean = soyabean.sort_values(
        by="Modal_x0020_Price",
        ascending=False
    )

    print("\n--- SOYABEAN MARKET COMPARISON ---")
    print(soyabean[columns].to_string(index=False))

    print("\nHighest modal price:")
    print(soyabean.iloc[0]["Market"],
          soyabean.iloc[0]["Modal_x0020_Price"])

    print("\nLowest modal price:")
    print(soyabean.iloc[-1]["Market"],
          soyabean.iloc[-1]["Modal_x0020_Price"])

    print("\nAverage modal price:",
          round(soyabean["Modal_x0020_Price"].mean(), 2))



import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))

plt.bar(
    soyabean["Market"],
    soyabean["Modal_x0020_Price"]
)

plt.title("Soyabean Modal Price by Market - Madhya Pradesh")
plt.xlabel("Market")
plt.ylabel("Modal Price (₹)")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()

plt.savefig(
    project_folder / "data" / "soyabean_market_comparison.png",
    dpi=150
)

plt.show()


plt.figure(figsize=(10, 6))

bars = plt.bar(
    soyabean["Market"],
    soyabean["Modal_x0020_Price"]
)

plt.title("Soyabean Modal Price by Market - Madhya Pradesh")
plt.xlabel("Market")
plt.ylabel("Modal Price (₹)")
plt.xticks(rotation=30, ha="right")

plt.bar_label(bars, fmt="₹%.0f", padding=4)

plt.tight_layout()
plt.savefig(
    project_folder / "data" / "soyabean_market_comparison.png",
    dpi=150
)
plt.show()
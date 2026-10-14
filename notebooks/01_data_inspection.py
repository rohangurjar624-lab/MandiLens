from pathlib import Path
import pandas as pd

project_folder = Path(__file__).resolve().parent.parent
file_path = project_folder / "data" / "data123.csv"

print("File exists:", file_path.exists())
print("File size:", file_path.stat().st_size, "bytes")

df = pd.read_csv(file_path)

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isnull().sum())


print("\n--- DATASET OVERVIEW ---")

print("\nUnique states:", df["State"].nunique())
print("Unique districts:", df["District"].nunique())
print("Unique markets:", df["Market"].nunique())
print("Unique commodities:", df["Commodity"].nunique())

print("\nDate range:")
dates = pd.to_datetime(
    df["Arrival_Date"],
    dayfirst=True,
    errors="coerce"
)
print("Earliest date:", dates.min())
print("Latest date:", dates.max())
print("Invalid dates:", dates.isna().sum())

print("\nDuplicate rows:", df.duplicated().sum())

print("\nPrice summary:")
print(df[[
    "Min_x0020_Price",
    "Max_x0020_Price",
    "Modal_x0020_Price"
]].describe())


print("\n--- PRICE VALIDATION ---")

min_col = "Min_x0020_Price"
max_col = "Max_x0020_Price"
modal_col = "Modal_x0020_Price"

invalid_min = df[min_col] > df[modal_col]
invalid_max = df[modal_col] > df[max_col]

print("Minimum price > modal price:", invalid_min.sum())
print("Modal price > maximum price:", invalid_max.sum())

print("\nRows with inconsistent prices:")
print(df[invalid_min | invalid_max][[
    "State",
    "Market",
    "Commodity",
    min_col,
    modal_col,
    max_col
]].head(10))

print("\n--- TOP 10 COMMODITIES BY RECORD COUNT ---")
print(df["Commodity"].value_counts().head(10))

print("\n--- TOP 10 MARKETS BY RECORD COUNT ---")
print(df["Market"].value_counts().head(10))

print("\n--- MADHYA PRADESH DATA ---")
mp_data = df[df["State"].str.strip().str.lower() == "madhya pradesh"]
print("Records:", len(mp_data))
print("Districts:", mp_data["District"].nunique())
print("Markets:", mp_data["Market"].nunique())
print("Commodities:", mp_data["Commodity"].nunique())

output_path = project_folder / "data" / "madhya_pradesh_prices.csv"
mp_data.to_csv(output_path, index=False)
print("\nMP dataset saved to:", output_path)
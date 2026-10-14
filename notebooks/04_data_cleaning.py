
import pandas as pd
from pathlib import Path

project_folder = Path(__file__).resolve().parent.parent
file_path = project_folder / "data" / "data123.csv"

df = pd.read_csv(file_path)

# Clean column names
df = df.rename(columns={
    "Min_x0020_Price": "Min_Price",
    "Max_x0020_Price": "Max_Price",
    "Modal_x0020_Price": "Modal_Price"
})

# Remove extra spaces from text columns
text_columns = df.select_dtypes(include=["str", "object"]).columns

for column in text_columns:
    df[column] = df[column].str.strip()

# Convert arrival date
df["Arrival_Date"] = pd.to_datetime(
    df["Arrival_Date"],
    dayfirst=True,
    errors="coerce"
)

# Ensure price columns are numeric
price_columns = ["Min_Price", "Max_Price", "Modal_Price"]

for column in price_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

# Create useful feature: price range
df["Price_Range"] = df["Max_Price"] - df["Min_Price"]

# Save cleaned data
output_path = project_folder / "data" / "cleaned_mandi_prices.csv"
df.to_csv(output_path, index=False)

print("Original records:", len(df))
print("Missing values after cleaning:")
print(df.isnull().sum())

print("\nCleaned file saved at:", output_path)
print("Dataset shape:", df.shape)


print("\n--- DATA QUALITY CHECK ---")

print("Duplicate rows:", df.duplicated().sum())

print(
    "Invalid price ranges:",
    (df["Min_Price"] > df["Max_Price"]).sum()
)

print(
    "Modal price below minimum:",
    (df["Modal_Price"] < df["Min_Price"]).sum()
)

print(
    "Modal price above maximum:",
    (df["Modal_Price"] > df["Max_Price"]).sum()
)

print(
    "Negative prices:",
    (df[["Min_Price", "Max_Price", "Modal_Price"]] < 0)
    .any(axis=1).sum()
)

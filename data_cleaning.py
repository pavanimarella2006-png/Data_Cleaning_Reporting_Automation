import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# --------------------------------------------------
# 1. Create project folders
# --------------------------------------------------

base_folder = Path(__file__).parent

raw_folder = base_folder / "raw_data"
cleaned_folder = base_folder / "cleaned_data"
reports_folder = base_folder / "reports"

cleaned_folder.mkdir(exist_ok=True)
reports_folder.mkdir(exist_ok=True)

# --------------------------------------------------
# 2. Find the input file automatically
# --------------------------------------------------

excel_files = list(raw_folder.glob("*.xlsx"))
csv_files = list(raw_folder.glob("*.csv"))

if excel_files:
    file_path = excel_files[0]
    df = pd.read_excel(file_path)

elif csv_files:
    file_path = csv_files[0]
    df = pd.read_csv(file_path)

else:
    print("ERROR: No Excel or CSV file found.")
    print("Please put your dataset inside the raw_data folder.")
    exit()

print("File loaded successfully:", file_path.name)

# --------------------------------------------------
# 3. Display original data
# --------------------------------------------------

print("\nOriginal data:")
print(df.head())

print("\nOriginal shape:", df.shape)

# --------------------------------------------------
# 4. Check missing values
# --------------------------------------------------

print("\nMissing values:")
print(df.isnull().sum())

# --------------------------------------------------
# 5. Remove duplicate rows
# --------------------------------------------------

duplicate_count = df.duplicated().sum()

print("\nDuplicate rows:", duplicate_count)

df = df.drop_duplicates()

# --------------------------------------------------
# 6. Handle missing values
# --------------------------------------------------

# Fill missing numeric values with the median
numeric_columns = df.select_dtypes(include="number").columns

for column in numeric_columns:
    df[column] = df[column].fillna(df[column].median())

# Fill missing text values with "Unknown"
text_columns = df.select_dtypes(include="object").columns

for column in text_columns:
    df[column] = df[column].fillna("Unknown")

# --------------------------------------------------
# 7. Remove extra spaces from text columns
# --------------------------------------------------

for column in text_columns:
    df[column] = df[column].astype(str).str.strip()

# --------------------------------------------------
# 8. Save cleaned data
# --------------------------------------------------

cleaned_file = cleaned_folder / "cleaned_sales_data.xlsx"

df.to_excel(cleaned_file, index=False)

print("\nCleaned data saved successfully!")

# --------------------------------------------------
# 9. Create summary report
# --------------------------------------------------

summary_data = {
    "Metric": [
        "Original Rows",
        "Cleaned Rows",
        "Duplicate Rows Removed",
        "Total Columns"
    ],
    "Value": [
        len(df) + duplicate_count,
        len(df),
        duplicate_count,
        len(df.columns)
    ]
}

summary_df = pd.DataFrame(summary_data)

summary_file = reports_folder / "summary_report.xlsx"

summary_df.to_excel(summary_file, index=False)

print("Summary report saved successfully!")

# --------------------------------------------------
# 10. Create charts for numeric columns
# --------------------------------------------------

numeric_columns = df.select_dtypes(include="number").columns

for column in numeric_columns:

    plt.figure(figsize=(8, 5))

    df[column].plot(kind="hist")

    plt.title("Distribution of " + column)
    plt.xlabel(column)
    plt.ylabel("Frequency")

    plt.tight_layout()

    chart_file = reports_folder / (column + "_chart.png")

    plt.savefig(chart_file)

    plt.close()

print("Charts created successfully!")

# --------------------------------------------------
# 11. Final message
# --------------------------------------------------

print("\n===================================")
print("DATA CLEANING COMPLETED SUCCESSFULLY")
print("===================================")
print("Cleaned data:", cleaned_file)
print("Summary report:", summary_file)
print("Reports folder:", reports_folder)
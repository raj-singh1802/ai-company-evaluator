import pandas as pd

# Load MCA file
df = pd.read_csv(
    "data/mca_companies.csv",
    encoding="latin-1",
    low_memory=False
)

# Clean columns
df.columns = df.columns.str.strip()

print("Columns:")
print(df.columns.tolist())

# Change if needed
company_col = "Company Name"

# Keep only company names
small_df = df[[company_col]]

# Drop null values
small_df = small_df.dropna()

# Convert to string
small_df[company_col] = (
    small_df[company_col]
    .astype(str)
)

# Remove duplicates
small_df = small_df.drop_duplicates()

# Sort names
small_df = small_df.sort_values(
    by=company_col
)

# Reset index
small_df = small_df.reset_index(drop=True)

small_df = small_df.head(500000)

# Save compressed version
small_df.to_csv(
    "data/mca_companies_small.csv",
    index=False
)

print(
    f"Final rows: {len(small_df)}"
)
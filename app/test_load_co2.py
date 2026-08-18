import pandas as pd

df = pd.read_csv(
    "data/co2_profiles.csv",
    sep="\t"
)

print(df.head())

print()
print(df.columns)

print()
print(f"Aantal regels: {len(df)}")
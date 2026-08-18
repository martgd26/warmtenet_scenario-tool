import pandas as pd

df = pd.read_csv("data/electricity_profile.csv",sep="\t")

profile_col = "Electriciteitsprofiel from ned.nl (standaard dag profiel)"

df[profile_col] = (df[profile_col].str.replace("%", "", regex=False).astype(float)/100)

print(df.head())

print()
print(f"Som profiel = {df[profile_col].sum():.6f}")

annual_electricity_demand = 2500

df["hourly_electricity_demand"] = (annual_electricity_demand*df[profile_col])

print()

print(f"Totaal jaarverbruik = "f"{df['hourly_electricity_demand'].sum():.2f} kWh")
import pandas as pd

from calculations.scenario_1 import (calculate_hourly_heat_demand,calculate_heatpump_electricity,calculate_total_electricity_demand,calculate_household_electricity,calculate_city_electricity_demand,calculate_city_co2_emissions,calculate_city_opex,)

#Electriciteitsvraag
electricity_df = pd.read_csv("data/electricity_profile.csv",sep="\t")
electricity_profile = electricity_df["Electriciteitsprofiel from ned.nl (standaard dag profiel)"] / electricity_df["Electriciteitsprofiel from ned.nl (standaard dag profiel)"].sum()

#Warmtevraag
heat_df = pd.read_csv("data/heat_profile.csv",sep="\t")
heat_profile = heat_df["MW"] / heat_df["MW"].sum()
cop = 0.45*((273+50)/(50-heat_df["°C"]))

#Electriciteitsvraag huishouden
household_electricity = calculate_household_electricity(annual_electricity_demand_kwh=2500,electricity_profile=electricity_profile,)

#Warmtevraag huishouden + warmtepomp elektriciteitsvraag
hourly_heat = calculate_hourly_heat_demand(annual_heat_demand_gj=31,heat_profile=heat_profile,)
heatpump_electricity = calculate_heatpump_electricity(hourly_heat_demand=hourly_heat,hourly_cop=cop,)

#Totale elektriciteitsvraag huishouden (electriciteit + warmtepomp)
total_electricity = calculate_total_electricity_demand(household_electricity=household_electricity,heatpump_electricity=heatpump_electricity,)

#Totale elektriciteitsvraag stad (82000 huizen)
city_electricity = calculate_city_electricity_demand(
    total_electricity_demand=total_electricity,
    houses=82000,
)

co2_df = pd.read_csv("data/co2_profiles.csv",
    sep="\t"
)

co2_profile = co2_df["2025"]

city_co2 = calculate_city_co2_emissions(
    city_electricity_demand=city_electricity,
    co2_profile=co2_profile,
)

price_df = pd.read_csv(
    "data/electricity_prices.csv",
    sep="\t"
)
price_profile = (
    price_df["2025"]
    .str.replace("€", "", regex=False)
    .str.strip()
    .replace("-", "0")
    .astype(float)
)

print(price_profile.head())
print(price_profile.dtype)


city_opex = calculate_city_opex(
    city_electricity_demand=city_electricity,
    electricity_price_profile=price_profile,
)

print(price_profile)

print(
    f"Annual OPEX = "
    f"€{city_opex.sum():,.0f}"
)
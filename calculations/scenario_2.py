import pandas as pd

from calculations.scenario_1 import *

def calculate_daily_average_heat_demand(hourly_heat_demand: pd.Series,) -> pd.Series:
    daily_average = (hourly_heat_demand.groupby(hourly_heat_demand.index // 24).transform("mean"))
    return daily_average

def calculate_buffer_volume(heatpump_electricity: pd.Series,daily_average_heat_demand: pd.Series,scop: float,delta_t: float = 20,):
    buffer_content = (daily_average_heat_demand - heatpump_electricity).cumsum()
    required_storage_energy = (buffer_content.max() - buffer_content.min())
    required_storage_energy *= scop
    volume = (required_storage_energy * 3600000 / 4180 / delta_t)
    return volume

def run_scenario_2(
    houses: int,
    annual_electricity_demand_kwh: float,
    annual_heat_demand_gj: float,
    analysis_year: str,
    capex_per_house: float,
    heatpump_lifetime_years: int,
    wacc: float,
    grid_expansion_cost_eur_per_kw: float,
    delta_t_buffer: float,
    ):

    # Electricity profile
    electricity_df = pd.read_csv("data/electricity_profile.csv",sep="\t")
    electricity_profile = (electricity_df["Electriciteitsprofiel from ned.nl (standaard dag profiel)"]
                           /electricity_df["Electriciteitsprofiel from ned.nl (standaard dag profiel)"].sum())

    # Heat profile
    heat_df = pd.read_csv("data/heat_profile.csv",sep="\t")
    heat_profile = (heat_df["MW"] / heat_df["MW"].sum())
    cop = (0.45 * ((273 + 50) / (50 - heat_df["°C"])))

    # CO₂ emission
    co2_df = pd.read_csv("data/co2_profiles.csv",sep="\t")
    co2_profile = co2_df[analysis_year]

     # Electricity prices
    price_df = pd.read_csv("data/electricity_prices.csv",sep="\t")
    price_profile = (price_df[analysis_year].str.replace("€", "", regex=False).str.strip().replace("-", "0").astype(float))

    # Calculations
    household_electricity = calculate_household_electricity(annual_electricity_demand_kwh=annual_electricity_demand_kwh,
                                                            electricity_profile=electricity_profile,)

    hourly_heat = calculate_hourly_heat_demand(annual_heat_demand_gj=annual_heat_demand_gj,heat_profile=heat_profile,)

    heatpump_electricity = calculate_heatpump_electricity(hourly_heat_demand=hourly_heat,hourly_cop=cop,)

    daily_average_heat = calculate_daily_average_heat_demand(hourly_heat_demand=heatpump_electricity)

    total_electricity = calculate_total_electricity_demand(household_electricity=household_electricity,
                                                           heatpump_electricity=daily_average_heat,)

    city_electricity = calculate_city_electricity_demand(total_electricity_demand=total_electricity,houses=houses,)

    annual_city_electricity_demand = (city_electricity.sum())

    peak_city_electricity_demand = (city_electricity.max())

    city_co2 = calculate_city_co2_emissions(city_electricity_demand=city_electricity,co2_profile=co2_profile,)

    annual_co2 = city_co2.sum()
   
    city_opex = calculate_city_opex(city_electricity_demand=city_electricity,electricity_price_profile=price_profile,)

    annual_city_opex = city_opex.sum()

    heat_opex = calculate_heat_opex(total_opex=city_opex,heatpump_electricity=daily_average_heat,
                                    total_electricity=total_electricity,)

    annual_heat_opex = heat_opex.sum()

    annuity_factor = calculate_annuity_factor(interest=wacc/100,lifetime_years=heatpump_lifetime_years,)

    heatpump_capex = calculate_heatpump_capex(capex_per_house=capex_per_house,houses=houses,annuity_factor=annuity_factor,)

    grid_capex = calculate_grid_capex(peak_heatpump_electricity_kw=daily_average_heat.max(),houses=houses,
                                      grid_expansion_cost_eur_per_kw=grid_expansion_cost_eur_per_kw,annuity_factor=annuity_factor,)

    total_costs = (heatpump_capex + grid_capex + annual_city_opex)

    lcoe_heat = calculate_lcoe_heat(city_capex=heatpump_capex,grid_capex=grid_capex,heat_opex=annual_heat_opex,
                                    houses=houses,heatpump_electricity=daily_average_heat,hourly_heat_demand=hourly_heat,)

    scop = calculate_scop(hourly_heat_demand=hourly_heat,heatpump_electricity=heatpump_electricity,) #(hourly_heat.sum() / heatpump_electricity.sum())

    buffer_volume = (calculate_buffer_volume(heatpump_electricity=heatpump_electricity,daily_average_heat_demand=daily_average_heat,scop=scop,delta_t=delta_t_buffer,))

    return {"annual_city_electricity_demand":annual_city_electricity_demand,
            "peak_city_electricity_demand":peak_city_electricity_demand,
            "annual_co2":annual_co2,
            "annual_city_opex":annual_city_opex,
            "annual_capex":heatpump_capex,
            "annual_grid_capex":grid_capex,
            "annual_total_costs":total_costs,
            "lcoe_heat":lcoe_heat,
            "buffer_volume":buffer_volume,}
import pandas as pd
import numpy as np
from calculations.common import *
from calculations.load_profiles import load_profiles

def calculate_heatpump_electricity(hourly_heat_demand: pd.Series,hourly_cop: pd.Series,) -> pd.Series:
    return hourly_heat_demand / hourly_cop

def calculate_scop(hourly_heat_demand: pd.Series,heatpump_electricity: pd.Series,) -> float:
    return (hourly_heat_demand.sum() / heatpump_electricity.sum())

def calculate_daily_average_heat_demand(hourly_heat_demand: pd.Series,datetime_series: pd.Series,) -> pd.Series:
    excel_serial = ((datetime_series - pd.Timestamp("1899-12-30")).dt.total_seconds() / 86400)
    daily_groups = np.floor(excel_serial - 1/24 + 1e-9)
    daily_groups[daily_groups == daily_groups.min()] += 1
    return (hourly_heat_demand.groupby(daily_groups).transform("mean"))

def calculate_buffer_volume(heatpump_electricity: pd.Series,daily_average_heat_demand: pd.Series,scop: float,delta_t: float = 20,):
    buffer_content = (daily_average_heat_demand - heatpump_electricity).cumsum()
    required_storage_energy = (buffer_content.max() - buffer_content.min())
    required_storage_energy *= scop
    volume = (required_storage_energy * 3600000 / 4180 / delta_t) / 1000
    return volume

def run_scenario_2(houses: int,annual_electricity_demand_kwh: float,annual_heat_demand_gj: float,
                   analysis_year: str,capex_per_house: float,heatpump_lifetime_years: int,
                   wacc: float,grid_expansion_cost_eur_per_kw: float,delta_t_buffer: float,):

    # Loading profiles
    (electricity_profile,heat_df,co2_profile,price_profile,) = load_profiles(analysis_year)
    heat_profile = (heat_df["MW"] / heat_df["MW"].sum())
    heat_df["datum"] = pd.to_datetime(heat_df["datum"],dayfirst=True,)

    cop = (0.45 * ((273 + 50) / (50 - heat_df["°C"])))

    # Calculations
    household_electricity = calculate_household_electricity(annual_electricity_demand_kwh=annual_electricity_demand_kwh,
                                                            electricity_profile=electricity_profile,)

    hourly_heat = calculate_hourly_heat_demand(annual_heat_demand_gj=annual_heat_demand_gj,heat_profile=heat_profile,)

    heatpump_electricity = calculate_heatpump_electricity(hourly_heat_demand=hourly_heat,hourly_cop=cop,)

    daily_average_heat = calculate_daily_average_heat_demand(hourly_heat_demand=heatpump_electricity,datetime_series=heat_df["datum"],)

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
import pandas as pd
import numpy as np
from calculations.common import *
from calculations.load_profiles import load_profiles

def calculate_collective_scop(carnot_efficiency: float,t_delivery: float,t_wko: float,) -> float:
    return (carnot_efficiency * ((273 + t_delivery) / (t_delivery - t_wko)))

def calculate_collective_heat_electricity(hourly_heat_demand: pd.Series,scop_collective: float,
                                          heat_loss_collective_heat_system: float,) -> pd.Series:
    return (hourly_heat_demand / scop_collective / (1 - heat_loss_collective_heat_system))

def run_scenario_3(houses: int,annual_electricity_demand_kwh: float,annual_heat_demand_gj: float,
                   analysis_year: str,capex_per_house: float,heatpump_lifetime_years: int,
                   wacc: float,grid_expansion_cost_eur_per_kw_centralized: float,
                   heat_loss_collective_heat_system: float = 0.10,):

    # Loading profiles
    (electricity_profile,heat_df,co2_profile,price_profile,) = load_profiles(analysis_year)
    heat_profile = (heat_df["MW"] / heat_df["MW"].sum())

    # Collective SCOP assumptions
    carnot_efficiency = 0.55
    t_delivery = 50
    t_wko = 17

    scop_collective = calculate_collective_scop(carnot_efficiency=carnot_efficiency,t_delivery=t_delivery,t_wko=t_wko,)

   # Calculations
    household_electricity = (calculate_household_electricity(annual_electricity_demand_kwh,electricity_profile,))
    hourly_heat = (calculate_hourly_heat_demand(annual_heat_demand_gj,heat_profile,))

    collective_heat_electricity = (calculate_collective_heat_electricity(hourly_heat_demand=hourly_heat,
                                                                         scop_collective=scop_collective,
                                                                         heat_loss_collective_heat_system=heat_loss_collective_heat_system,))

    print(hourly_heat.sum())
    print(collective_heat_electricity.sum() * scop_collective)


    total_electricity = (calculate_total_electricity_demand(household_electricity,collective_heat_electricity,))

    city_electricity = (calculate_city_electricity_demand(total_electricity,houses,))

    annual_city_electricity_demand = (city_electricity.sum())

    peak_city_electricity_demand = (city_electricity.max())

    city_co2 = calculate_city_co2_emissions(city_electricity,co2_profile,)

    annual_co2 = city_co2.sum()

    city_opex = calculate_city_opex(city_electricity,price_profile,)

    annual_city_opex = city_opex.sum()

    heat_opex = calculate_heat_opex(city_opex,collective_heat_electricity,total_electricity,)

    annual_heat_opex = heat_opex.sum()

    annuity_factor = calculate_annuity_factor(interest=wacc / 100,lifetime_years=heatpump_lifetime_years,)

    heatpump_capex = calculate_heatpump_capex(capex_per_house,houses,annuity_factor,)

    grid_capex = calculate_grid_capex(collective_heat_electricity.max(),houses,grid_expansion_cost_eur_per_kw_centralized,annuity_factor,)

    total_costs = (heatpump_capex + grid_capex + annual_city_opex)

    lcoe_heat = calculate_lcoe_heat_collective(city_capex=heatpump_capex,grid_capex=grid_capex,heat_opex=annual_heat_opex,
                                    houses=houses,collective_heat_electricity=collective_heat_electricity,scop_collective=scop_collective,)

    return {"annual_city_electricity_demand":annual_city_electricity_demand,
            "peak_city_electricity_demand":peak_city_electricity_demand,
            "annual_co2":annual_co2,
            "annual_city_opex":annual_city_opex,
            "annual_capex":heatpump_capex,
            "annual_grid_capex":grid_capex,
            "annual_total_costs":total_costs,
            "lcoe_heat":lcoe_heat,
            "scop_collective":scop_collective,}
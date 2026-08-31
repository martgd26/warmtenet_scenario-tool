import pandas as pd
import numpy as np
from calculations.common import *
from calculations.load_profiles import load_profiles

def calculate_buffer_volume(heatpump_electricity: pd.Series,daily_average_heat_demand: pd.Series,scop_collective: float,houses:int,delta_t_buffer_seasonal:float,):
    buffer_content = (daily_average_heat_demand - heatpump_electricity).cumsum()
    required_storage_energy = (buffer_content.max() - buffer_content.min())
    required_storage_energy *= houses
    required_storage_energy *= scop_collective
    volume = (required_storage_energy * 3600000 / 4180 / delta_t_buffer_seasonal /1000)
    return volume

def calculate_buffer_capex(buffer_volume: float,cost_per_m3: float, annuity_factor: float,) -> float:
    return (buffer_volume * cost_per_m3 * annuity_factor)
    
def run_scenario_4(houses: int,annual_electricity_demand_kwh: float,annual_heat_demand_gj: float,
                   analysis_year: str,capex_per_house: float,heatpump_lifetime_years: int,
                   wacc: float,grid_expansion_cost_eur_per_kw_centralized: float,
                   delta_t_buffer_seasonal: float,buffer_cost_per_m3: float,):

    # Loading profiles
    (electricity_profile,heat_df,co2_profile,price_profile,) = load_profiles(analysis_year)
    heat_profile = (heat_df["MW"] / heat_df["MW"].sum())

    carnot_efficiency = 0.55
    t_delivery = 50
    t_wko = 17

    scop_collective = (carnot_efficiency * ((273 + t_delivery) / (t_delivery - t_wko)))

    # Calculations
    household_electricity = calculate_household_electricity(annual_electricity_demand_kwh=annual_electricity_demand_kwh,
                                                            electricity_profile=electricity_profile,)

    hourly_heat = calculate_hourly_heat_demand(annual_heat_demand_gj=annual_heat_demand_gj,heat_profile=heat_profile,)

    heatpump_electricity = (hourly_heat / scop_collective / (1 - 0.10))

    year_average_heat = pd.Series(heatpump_electricity.mean(),index=heatpump_electricity.index,)

    total_electricity = calculate_total_electricity_demand(household_electricity=household_electricity,
                                                           heatpump_electricity=year_average_heat,)

    city_electricity = calculate_city_electricity_demand(total_electricity_demand=total_electricity,houses=houses,)

    annual_city_electricity_demand = (city_electricity.sum())

    peak_city_electricity_demand = (city_electricity.max())

    city_co2 = calculate_city_co2_emissions(city_electricity_demand=city_electricity,co2_profile=co2_profile,)

    annual_co2 = city_co2.sum()
   
    city_opex = calculate_city_opex(city_electricity_demand=city_electricity,electricity_price_profile=price_profile,)

    annual_city_opex = city_opex.sum()

    heat_opex = calculate_heat_opex(total_opex=city_opex,heatpump_electricity=year_average_heat,
                                    total_electricity=total_electricity,)

    annual_heat_opex = heat_opex.sum()

    annuity_factor = calculate_annuity_factor(interest=wacc/100,lifetime_years=heatpump_lifetime_years,)

    heatpump_capex = calculate_heatpump_capex(capex_per_house=capex_per_house,houses=houses,annuity_factor=annuity_factor,)

    grid_capex = calculate_grid_capex(peak_heatpump_electricity_kw=year_average_heat.max(),houses=houses,
                                      grid_expansion_cost_eur_per_kw=grid_expansion_cost_eur_per_kw_centralized,annuity_factor=annuity_factor,)


    #lcoe_heat = calculate_lcoe_heat(city_capex=heatpump_capex,grid_capex=grid_capex,heat_opex=annual_heat_opex,
    #                                houses=houses,heatpump_electricity=year_average_heat,hourly_heat_demand=hourly_heat,)


    

    #lcoe_heat = calculate_lcoe_heat_collective(city_capex=heatpump_capex,grid_capex=grid_capex,heat_opex=annual_heat_opex,
    #                                          
    #                                           houses=houses,collective_heat_electricity=year_average_heat,scop_collective=scop_collective,)

    buffer_volume = calculate_buffer_volume(heatpump_electricity=heatpump_electricity,daily_average_heat_demand=year_average_heat,scop_collective=scop_collective,houses=houses,delta_t_buffer_seasonal=delta_t_buffer_seasonal,)

    buffer_capex = calculate_buffer_capex(buffer_volume=buffer_volume,cost_per_m3=buffer_cost_per_m3,annuity_factor=annuity_factor,)

    total_costs = (heatpump_capex + grid_capex + annual_city_opex + buffer_capex)

    annual_heat_for_lcoe = (houses * year_average_heat.sum()* scop_collective)

    lcoe_heat = (heatpump_capex + grid_capex + buffer_capex + annual_heat_opex)/ annual_heat_for_lcoe
    
    return {"annual_city_electricity_demand":annual_city_electricity_demand,
            "peak_city_electricity_demand":peak_city_electricity_demand,
            "annual_co2":annual_co2,
            "annual_city_opex":annual_city_opex,
            "annual_capex":heatpump_capex,
            "annual_grid_capex":grid_capex,
            "annual_total_costs":total_costs,
            "lcoe_heat":lcoe_heat,
            "buffer_volume":buffer_volume,
            "buffer_capex": buffer_capex}
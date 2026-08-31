import pandas as pd

def calculate_household_electricity(annual_electricity_demand_kwh: float,electricity_profile: pd.Series,) -> pd.Series:
    return annual_electricity_demand_kwh * electricity_profile

def calculate_hourly_heat_demand(annual_heat_demand_gj: float,heat_profile: pd.Series,) -> pd.Series:
    annual_heat_demand_kwh = annual_heat_demand_gj / 0.0036
    return annual_heat_demand_kwh * heat_profile

def calculate_total_electricity_demand(household_electricity: pd.Series,heatpump_electricity: pd.Series,) -> pd.Series:
    return household_electricity + heatpump_electricity

def calculate_city_electricity_demand(total_electricity_demand: pd.Series,houses: int,) -> pd.Series:
    return total_electricity_demand * houses

def calculate_city_co2_emissions(city_electricity_demand: pd.Series,co2_profile: pd.Series,) -> pd.Series:
    return city_electricity_demand * co2_profile

def calculate_city_opex(city_electricity_demand: pd.Series,electricity_price_profile: pd.Series,) -> pd.Series:
    return city_electricity_demand * electricity_price_profile

def calculate_annuity_factor(interest: float,lifetime_years: int,) -> float:
    return interest / (1 - (1 / (1 + interest) ** lifetime_years))

def calculate_heatpump_capex(capex_per_house: float,houses: int,annuity_factor: float,) -> float:
    return capex_per_house * houses * annuity_factor

def calculate_grid_capex(peak_heatpump_electricity_kw: float,houses: int,grid_expansion_cost_eur_per_kw: float,
                         annuity_factor: float,) -> float:
    return (peak_heatpump_electricity_kw * houses * grid_expansion_cost_eur_per_kw * annuity_factor)

def calculate_heat_opex(total_opex: pd.Series,heatpump_electricity: pd.Series,total_electricity: pd.Series,) -> pd.Series:
    return total_opex * (heatpump_electricity / total_electricity)

def calculate_lcoe_heat(city_capex: float,grid_capex: float,heat_opex: float,houses: int,
                        heatpump_electricity: pd.Series,hourly_heat_demand: pd.Series,) -> float:
    annual_heat_delivered = houses * hourly_heat_demand.sum()
    return (city_capex + grid_capex + heat_opex) / annual_heat_delivered

def calculate_lcoe_heat_collective(city_capex: float,grid_capex: float,heat_opex: float,
                                   houses: int,collective_heat_electricity: pd.Series,
                                   scop_collective: float,) -> float:
    annual_heat_delivered = (houses * collective_heat_electricity.sum() * scop_collective)
    return (city_capex + grid_capex + heat_opex) / annual_heat_delivered
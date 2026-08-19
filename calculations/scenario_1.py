import pandas as pd


def calculate_household_electricity(
    annual_electricity_demand_kwh: float,
    electricity_profile: pd.Series,
) -> pd.Series:
    return annual_electricity_demand_kwh * electricity_profile


def calculate_hourly_heat_demand(
    annual_heat_demand_gj: float,
    heat_profile: pd.Series,
) -> pd.Series:
    annual_heat_demand_kwh = annual_heat_demand_gj / 0.0036

    return annual_heat_demand_kwh * heat_profile

def calculate_heatpump_electricity(
    hourly_heat_demand: pd.Series,
    hourly_cop: pd.Series,
) -> pd.Series:
    return hourly_heat_demand / hourly_cop

def calculate_total_electricity_demand(
    household_electricity: pd.Series,
    heatpump_electricity: pd.Series,
) -> pd.Series:
    return household_electricity + heatpump_electricity

def calculate_city_electricity_demand(
    total_electricity_demand: pd.Series,
    houses: int,
) -> pd.Series:
    return total_electricity_demand * houses

def calculate_city_co2_emissions(
    city_electricity_demand: pd.Series,
    co2_profile: pd.Series,
) -> pd.Series:
    return city_electricity_demand * co2_profile

def calculate_city_opex(
    city_electricity_demand: pd.Series,
    electricity_price_profile: pd.Series,
) -> pd.Series:
    return city_electricity_demand * electricity_price_profile

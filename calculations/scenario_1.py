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

def calculate_annuity_factor(
    interest: float,
    lifetime_years: int,
) -> float:
    return (
        interest
        /
        (
            1
            - (1 / (1 + interest) ** lifetime_years)
        )
    )

def calculate_heatpump_capex(
    capex_per_house: float,
    houses: int,
    annuity_factor: float,
) -> float:
    return (
        capex_per_house
        * houses
        * annuity_factor
    )

def calculate_grid_capex(
    peak_heatpump_electricity_kw: float,
    houses: int,
    grid_expansion_cost_eur_per_kw: float,
    annuity_factor: float,
) -> float:
    return (
        peak_heatpump_electricity_kw
        * houses
        * grid_expansion_cost_eur_per_kw
        * annuity_factor
    )

def calculate_heat_opex(
    total_opex: pd.Series,
    heatpump_electricity: pd.Series,
    total_electricity: pd.Series,
) -> pd.Series:
    return (
        total_opex
        * (
            heatpump_electricity
            / total_electricity
        )
    )

def calculate_scop(
    hourly_heat_demand: pd.Series,
    heatpump_electricity: pd.Series,
) -> float:
    return (
        hourly_heat_demand.sum()
        / heatpump_electricity.sum()
    )

def calculate_lcoe_heat(
    city_capex: float,
    grid_capex: float,
    heat_opex: float,
    houses: int,
    heatpump_electricity: pd.Series,
    hourly_heat_demand: pd.Series,
) -> float:

    annual_heat_delivered = (
        houses
        * hourly_heat_demand.sum()
    )

    return (
        city_capex
        + grid_capex
        + heat_opex
    ) / annual_heat_delivered

def run_scenario_1(
    houses: int,
    annual_electricity_demand_kwh: float,
    annual_heat_demand_gj: float,
    analysis_year: str,
    capex_per_house: float,
    heatpump_lifetime_years: int,
    wacc: float,
    grid_expansion_cost_eur_per_kw: float,
):

    # Electricity profile
    electricity_df = pd.read_csv(
        "data/electricity_profile.csv",
        sep="\t"
    )

    electricity_profile = (
        electricity_df[
            "Electriciteitsprofiel from ned.nl (standaard dag profiel)"
        ]
        /
        electricity_df[
            "Electriciteitsprofiel from ned.nl (standaard dag profiel)"
        ].sum()
    )

    # Heat profile
    heat_df = pd.read_csv(
        "data/heat_profile.csv",
        sep="\t"
    )

    heat_profile = (
        heat_df["MW"]
        / heat_df["MW"].sum()
    )

    cop = (
        0.45
        * ((273 + 50) / (50 - heat_df["°C"]))
    )


    co2_df = pd.read_csv(
    "data/co2_profiles.csv",
    sep="\t"
    )

    co2_profile = co2_df[analysis_year]

    # NEW CODE HERE

    household_electricity = calculate_household_electricity(
        annual_electricity_demand_kwh=
            annual_electricity_demand_kwh,
        electricity_profile=
            electricity_profile,
    )

    hourly_heat = calculate_hourly_heat_demand(
        annual_heat_demand_gj=
            annual_heat_demand_gj,
        heat_profile=
            heat_profile,
    )

    heatpump_electricity = calculate_heatpump_electricity(
        hourly_heat_demand=
            hourly_heat,
        hourly_cop=
            cop,
    )

    total_electricity = calculate_total_electricity_demand(
        household_electricity=
            household_electricity,
        heatpump_electricity=
            heatpump_electricity,
    )

    city_electricity = calculate_city_electricity_demand(
    total_electricity_demand=total_electricity,
    houses=houses,
    )

    annual_city_electricity_demand = (
    city_electricity.sum()
    )

    peak_city_electricity_demand = (
        city_electricity.max()
    )

    city_co2 = calculate_city_co2_emissions(
        city_electricity_demand=city_electricity,
        co2_profile=co2_profile,
    )

    annual_co2 = city_co2.sum()

    # Electricity prices

    price_df = pd.read_csv(
        "data/electricity_prices.csv",
        sep="\t"
    )

    price_profile = (
        price_df[analysis_year]
        .str.replace("€", "", regex=False)
        .str.strip()
        .replace("-", "0")
        .astype(float)
    )

    city_opex = calculate_city_opex(
    city_electricity_demand=city_electricity,
    electricity_price_profile=price_profile,
    )

    heat_opex = calculate_heat_opex(
    total_opex=city_opex,
    heatpump_electricity=heatpump_electricity,
    total_electricity=total_electricity,
    )

    annual_heat_opex = heat_opex.sum()

    annuity_factor = calculate_annuity_factor(
    interest=wacc/100,
    lifetime_years=heatpump_lifetime_years,
    )

    heatpump_capex = calculate_heatpump_capex(
    capex_per_house=capex_per_house,
    houses=houses,
    annuity_factor=annuity_factor,
    )

    grid_capex = calculate_grid_capex(
    peak_heatpump_electricity_kw=
        heatpump_electricity.max(),
    houses=houses,
    grid_expansion_cost_eur_per_kw=grid_expansion_cost_eur_per_kw,
    annuity_factor=annuity_factor,
    )

    total_costs = (
    heatpump_capex
    + grid_capex
    + annual_heat_opex
    )

    lcoe_heat = calculate_lcoe_heat(
    city_capex=heatpump_capex,
    grid_capex=grid_capex,
    heat_opex=annual_heat_opex,
    houses=houses,
    heatpump_electricity=heatpump_electricity,
    hourly_heat_demand=hourly_heat,
    )



    return {
    "annual_city_electricity_demand":
        annual_city_electricity_demand,

    "peak_city_electricity_demand":
        peak_city_electricity_demand,

    "annual_co2":
        annual_co2,

    "annual_heat_opex":
        annual_heat_opex,

    "annual_capex":
        heatpump_capex,

    "annual_grid_capex":
        grid_capex,

    "annual_total_costs":
        total_costs,

    "lcoe_heat":
        lcoe_heat,
        }
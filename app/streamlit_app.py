import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
import streamlit as st
from calculations.scenario_1 import run_scenario_1

st.title("Warmtenet Tool Scenario 1")

houses = st.number_input("Number of houses", value=82000,)
electricity_demand = st.number_input("Electricity demand per house (kWh/year)",value=2500,)
heat_demand = st.number_input("Heat demand per house (GJ/year)",value=31,)
heat_loss_heat_network = st.number_input("Heat loss in heat network (%)",value=10,)
analysis_year = st.selectbox("Analysis year",["2018","2019","2020","2021","2022","2023","2024","2025",],index=7,)
wacc = st.number_input("WACC (%)",value=3,)
grid_expansion_cost_eur_per_kw = st.number_input("Grid expansion cost decentralized (€ / kW)",value=1000,)
grid_expansion_cost_eur_per_kw_centralized = st.number_input("Grid expansion cost centralized (€ / kW)", value=650,)

with st.expander("Scenario specific settings"):
    capex_per_house = st.number_input("CAPEX (€ per house)",value=7000.0,)
    heatpump_lifetime_years = st.number_input("Heat pump lifetime (years)",value=15,) 

if st.button("Calculate"):
    results = run_scenario_1(
    houses=houses,
    annual_electricity_demand_kwh=electricity_demand,
    annual_heat_demand_gj=heat_demand,
    analysis_year=analysis_year,
    capex_per_house=capex_per_house,
    heatpump_lifetime_years=heatpump_lifetime_years,
    wacc=wacc,
    grid_expansion_cost_eur_per_kw=grid_expansion_cost_eur_per_kw,
    )
    
    st.header("Scenario Results")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Peak Demand City",f"{results['peak_city_electricity_demand']:.0f} kWh")
    with col2:
        st.metric("CO₂ Emissions City",f"{results['annual_co2']/1000:.0f} ton/year")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("CAPEX",f"€{results['annual_capex']:,.0f}")
    with col2:
        st.metric("Grid CAPEX",f"€{results['annual_grid_capex']:,.0f}")
    with col3:
        st.metric("Annual OPEX",f"€{results['annual_city_opex']:,.0f}")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Annual Costs",f"€{results['annual_total_costs']:,.0f}")
    with col2:
        st.metric("LCoE Heat",f"€{results['lcoe_heat']:.3f}/kWh")

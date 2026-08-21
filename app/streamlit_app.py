import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))
import streamlit as st
from calculations.scenario_1 import run_scenario_1
from calculations.scenario_2 import run_scenario_2

st.set_page_config(page_title="Warmtenet Tool",layout="wide",)

st.title("Warmtenet Tool")

with st.sidebar:
    mode = st.radio("Mode",["Single Scenario","Compare Scenarios",])

    if mode == "Single Scenario":
        scenario = st.selectbox("Scenario",["Individual Heat Pump","Individual Heat Pump + Day Buffer",])

        if scenario == "Individual Heat Pump":
            with st.expander("Scenario-specific settings"):
                capex_per_house_1 = st.number_input("CAPEX (€ per house)",value=7000.0,)
                heatpump_lifetime_years_1 = st.number_input("Heat pump lifetime (years)",value=15,key="single_s1_lifetime",)

        elif scenario == "Individual Heat Pump + Day Buffer":
            with st.expander("Scenario-specific settings"):
                capex_per_house_2 = st.number_input("CAPEX (€ per house)",value=8500.0,)
                heatpump_lifetime_years_2 = st.number_input("Heat pump lifetime (years)",value=15,key="single_s2_lifetime",)
                delta_t_buffer = st.number_input("Buffer ΔT (°C)", value=20.0,)

    if mode == "Compare Scenarios":
        st.subheader("Scenarios")

        selected_scenarios = []

        if st.checkbox("Individual Heat Pump",value=False,):
            selected_scenarios.append("Individual Heat Pump")

        if st.checkbox("Individual Heat Pump + Day Buffer",value=False,):
            selected_scenarios.append("Individual Heat Pump + Day Buffer")

        if "Individual Heat Pump" in selected_scenarios:
            with st.sidebar.expander("Scenario 1 Settings"):
                capex_per_house_1 = st.number_input("CAPEX (€ per house)",value=7000.0,)
                heatpump_lifetime_years_1 = st.number_input("Heat pump lifetime (years)",value=15,key="compare_s1_lifetime",)
            
        if "Individual Heat Pump + Day Buffer" in selected_scenarios:
            with st.sidebar.expander("Scenario 2 Settings"):
                capex_per_house_2 = st.number_input("CAPEX (€ per house)",value=8500.0,)
                heatpump_lifetime_years_2 = st.number_input("Heat pump lifetime (years)",value=15,key="compare_s2_lifetime",)
                delta_t_buffer = st.number_input("Buffer ΔT (°C)",value=20.0,)

    st.divider()
    if mode == "Single Scenario":
        calculate = st.button( "Calculate Scenario", use_container_width=True,)

    elif mode == "Compare Scenarios":
        calculate_comparison = st.button( "Calculate Comparison", use_container_width=True,)

    st.divider()

    st.header("General Inputs")
    analysis_year = st.selectbox("Analysis year",["2018","2019","2020","2021","2022","2023","2024","2025",],index=7,)
    houses = st.number_input("Number of houses", value=82000,)
    electricity_demand = st.number_input("Electricity demand per house (kWh/year)",value=2500,)
    heat_demand = st.number_input("Heat demand per house (GJ/year)",value=31,)

    st.divider()

    with st.expander("Advanced Inputs"):
        heat_loss_heat_network = st.number_input("Heat loss in heat network (%)",value=10,)
        wacc = st.number_input("WACC (%)",value=3,)
        grid_expansion_cost_eur_per_kw = st.number_input("Grid expansion cost decentralized (€ / kW)",value=1000,)
        grid_expansion_cost_eur_per_kw_centralized = st.number_input("Grid expansion cost centralized (€ / kW)", value=650,)


if mode == "Single Scenario":

    if calculate:
        if scenario == "Individual Heat Pump":

            results = run_scenario_1(
            houses=houses,
            annual_electricity_demand_kwh=electricity_demand,
            annual_heat_demand_gj=heat_demand,
            analysis_year=analysis_year,
            capex_per_house=capex_per_house_1,
            heatpump_lifetime_years=heatpump_lifetime_years_1,
            wacc=wacc,
            grid_expansion_cost_eur_per_kw=grid_expansion_cost_eur_per_kw,
            )
            
            st.header("Scenario Results")

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Peak Demand City",f"{results['peak_city_electricity_demand']:,.0f} kWh")
            with col2:
                st.metric("CO₂ Emissions City",f"{results['annual_co2']/1000:,.0f} ton/year")

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

        elif scenario == "Individual Heat Pump + Day Buffer":
            results = run_scenario_2(
            houses=houses,
            annual_electricity_demand_kwh=electricity_demand,
            annual_heat_demand_gj=heat_demand,
            analysis_year=analysis_year,
            capex_per_house=capex_per_house_2,
            heatpump_lifetime_years=heatpump_lifetime_years_2,
            wacc=wacc,
            grid_expansion_cost_eur_per_kw=grid_expansion_cost_eur_per_kw,
            delta_t_buffer = delta_t_buffer
            )

            st.header("Scenario Results")
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Peak Demand City",f"{results['peak_city_electricity_demand']:,.0f} kWh")
            with col2:
                st.metric("CO₂ Emissions City",f"{results['annual_co2']/1000:,.0f} ton/year")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("CAPEX",f"€{results['annual_capex']:,.0f}")
            with col2:
                st.metric("Grid CAPEX",f"€{results['annual_grid_capex']:,.0f}")
            with col3:
                st.metric("Annual OPEX",f"€{results['annual_city_opex']:,.0f}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Total Annual Costs",f"€{results['annual_total_costs']:,.0f}")
            with col2:
                st.metric("LCoE Heat",f"€{results['lcoe_heat']:.3f}/kWh")
            with col3:
                st.metric("Buffer Volume",f"{results['buffer_volume']:.1f} L")


if mode == "Compare Scenarios":

    if calculate_comparison:

        results = {}

        if "Individual Heat Pump" in selected_scenarios:
            results["Individual Heat Pump"] = run_scenario_1(
                houses=houses,
                annual_electricity_demand_kwh=electricity_demand,
                annual_heat_demand_gj=heat_demand,
                analysis_year=analysis_year,
                capex_per_house=capex_per_house_1,
                heatpump_lifetime_years=heatpump_lifetime_years_1,
                wacc=wacc,
                grid_expansion_cost_eur_per_kw=grid_expansion_cost_eur_per_kw,
                )

        if "Individual Heat Pump + Day Buffer" in selected_scenarios:
            results["Individual Heat Pump + Day Buffer"] = run_scenario_2(
                houses=houses,
                annual_electricity_demand_kwh=electricity_demand,
                annual_heat_demand_gj=heat_demand,
                analysis_year=analysis_year,
                capex_per_house=capex_per_house_2,
                heatpump_lifetime_years=heatpump_lifetime_years_2,
                wacc=wacc,
                grid_expansion_cost_eur_per_kw=grid_expansion_cost_eur_per_kw,
                delta_t_buffer=delta_t_buffer,
                )

        comparison_df = pd.DataFrame({scenario_name: {
            "Peak Demand (MW)": f"{scenario_results['peak_city_electricity_demand'] / 1000:,.1f}",
            "CO₂ (ton/year)": f"{scenario_results['annual_co2'] / 1000:,.0f}",
            "Annual Costs (€)": f"€{scenario_results['annual_total_costs']:,.0f}",
            "LCoE Heat (€/kWh)": f"€{scenario_results['lcoe_heat']:.3f}",}
            for scenario_name, scenario_results in results.items()})

        st.subheader("Scenario Comparison")
        st.dataframe(comparison_df,use_container_width=True,)
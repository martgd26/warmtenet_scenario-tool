import sys
from pathlib import Path
import pandas as pd

sys.path.append(str(Path(__file__).resolve().parent.parent))
import streamlit as st
from calculations.scenario_1 import run_scenario_1
from calculations.scenario_2 import run_scenario_2
from calculations.scenario_3 import run_scenario_3
from calculations.scenario_4 import run_scenario_4
from calculations.scenario_5 import run_scenario_5

st.set_page_config(page_title="Warmtenet Tool",layout="wide",)

st.title("Warmtenet Tool")

with st.sidebar:
    mode = st.radio("Mode",["Single Scenario","Compare Scenarios",])

    if mode == "Single Scenario":
        scenario = st.selectbox("Scenario",["Individual Heat Pump","Individual Heat Pump + Day Buffer","Collective Heat System","Collective Heat System + Seasonal Buffer","Collective Heat System + Two-Week Buffer"],index=0,)

        if scenario == "Individual Heat Pump":
            with st.expander("Scenario-specific settings"):
                capex_per_house_1 = st.number_input("CAPEX (€ per house)",value=7000.0,)
                heatpump_lifetime_years_1 = st.number_input("Heat pump lifetime (years)",value=15,key="single_s1_lifetime",)

        elif scenario == "Individual Heat Pump + Day Buffer":
            with st.expander("Scenario-specific settings"):
                capex_per_house_2 = st.number_input("CAPEX (€ per house)",value=8500.0,)
                heatpump_lifetime_years_2 = st.number_input("Heat pump lifetime (years)",value=15,key="single_s2_lifetime",)
                delta_t_buffer = st.number_input("Buffer ΔT (°C)", value=20.0,)

        elif scenario == "Collective Heat System":
            with st.expander("Scenario-specific settings"):
                capex_per_house_3 = st.number_input("CAPEX (€ per house)",value=15000.0,key="single_s3_capex",)
                heatpump_lifetime_years_3 = st.number_input("Heat system lifetime (years)",value=30,key="single_s3_lifetime",)

        elif scenario == "Collective Heat System + Seasonal Buffer":
            with st.expander("Scenario-specific settings"):
                capex_per_house_4 = st.number_input("CAPEX (€ per house)",value=15000.0,key="single_s4_capex",)
                heatpump_lifetime_years_4 = st.number_input("Heat system lifetime (years)",value=30,key="single_s4_lifetime",)
                delta_t_buffer_seasonal = st.number_input("Seasonal Buffer ΔT (°C)", value=50.0,)
                buffer_cost_per_m3_4 = st.number_input("Buffer CAPEX (€ / m³)",value=50.0, key="single_s4_buffer_cost")

        elif scenario == "Collective Heat System + Two-Week Buffer":
            with st.expander("Scenario-specific settings"):
                capex_per_house_5 = st.number_input("CAPEX (€ per house)",value=15000.0,key="single_s5_capex",)
                heatpump_lifetime_years_5 = st.number_input("Heat system lifetime (years)",value=30,key="single_s5_lifetime",)
                delta_t_buffer_two_week = st.number_input("Two-Week Buffer ΔT (°C)", value=50.0,)
                buffer_cost_per_m3_5 = st.number_input("Buffer CAPEX (€ / m³)",value=50.0, key="single_s5_buffer_cost")


    if mode == "Compare Scenarios":
        st.subheader("Scenarios")

        selected_scenarios = []

        if st.checkbox("Individual Heat Pump",value=False,):
            selected_scenarios.append("Individual Heat Pump")

        if st.checkbox("Individual Heat Pump + Day Buffer",value=False,):
            selected_scenarios.append("Individual Heat Pump + Day Buffer")

        if st.checkbox("Collective Heat System",value=False,):
            selected_scenarios.append("Collective Heat System")

        if st.checkbox("Collective Heat System + Seasonal Buffer",value=False,):
            selected_scenarios.append("Collective Heat System + Seasonal Buffer")

        if st.checkbox("Collective Heat System + Two-Week Buffer",value=False,):
            selected_scenarios.append("Collective Heat System + Two-Week Buffer")

        if "Individual Heat Pump" in selected_scenarios:
            with st.sidebar.expander("Settings 'Individual Heat Pump'"):
                capex_per_house_1 = st.number_input("CAPEX (€ per house)",value=7000.0,)
                heatpump_lifetime_years_1 = st.number_input("Heat pump lifetime (years)",value=15,key="compare_s1_lifetime",)
        
        if "Individual Heat Pump + Day Buffer" in selected_scenarios:
            with st.sidebar.expander("Settings 'Individual Heat Pump + Day Buffer'"):
                capex_per_house_2 = st.number_input("CAPEX (€ per house)",value=8500.0,)
                heatpump_lifetime_years_2 = st.number_input("Heat pump lifetime (years)",value=15,key="compare_s2_lifetime",)
                delta_t_buffer = st.number_input("Buffer ΔT (°C)",value=20.0,)

        if "Collective Heat System" in selected_scenarios:
                    with st.sidebar.expander("Settings 'Collective Heat System'"):
                        capex_per_house_3 = st.number_input("CAPEX (€ per house)",value=15000.0,key="compare_s3_capex",)
                        heatpump_lifetime_years_3 = st.number_input("Heat system lifetime (years)",value=30,key="compare_s3_lifetime",)

        if "Collective Heat System + Seasonal Buffer" in selected_scenarios:
                    with st.sidebar.expander("Settings 'Collective Heat System + Seasonal Buffer'"):
                        capex_per_house_4 = st.number_input("CAPEX (€ per house)",value=15000.0,key="compare_s4_capex",)
                        heatpump_lifetime_years_4 = st.number_input("Heat system lifetime (years)",value=30,key="compare_s4_lifetime",)
                        delta_t_buffer_seasonal = st.number_input("Seasonal Buffer ΔT (°C)",value=50.0,)
                        buffer_cost_per_m3_4 = st.number_input("Buffer CAPEX (€ / m³)",value=50.0, key="compare_s4_buffer_cost")

        if "Collective Heat System + Two-Week Buffer" in selected_scenarios:
                    with st.sidebar.expander("Settings 'Collective Heat System + Two-Week Buffer'"):
                        capex_per_house_5 = st.number_input("CAPEX (€ per house)",value=15000.0,key="compare_s5_capex",)
                        heatpump_lifetime_years_5 = st.number_input("Heat system lifetime (years)",value=30,key="compare_s5_lifetime",)
                        delta_t_buffer_two_week = st.number_input("Two-Week Buffer ΔT (°C)",value=50.0,)
                        buffer_cost_per_m3_5 = st.number_input("Buffer CAPEX (€ / m³)",value=50.0, key="compare_s5_buffer_cost")

    st.divider()
    if mode == "Single Scenario":
        calculate = st.button( "Calculate Scenario", use_container_width=True,)

    elif mode == "Compare Scenarios":
        calculate_comparison = st.button( "Calculate Comparison", use_container_width=True,)

    st.divider()

    st.header("General Inputs")
    analysis_year = st.selectbox("Analysis year",["2018","2019","2020","2021","2022","2023","2024","2025",],index=7,)
    houses = st.number_input("Number of houses", value=82000,)
    electricity_demand = st.number_input("Electricity demand per house (kWh/year) *ref. [1]*",value=2500,)
    heat_demand = st.number_input("Heat demand per house (GJ/year) *ref. [3]*",value=31,)

    st.divider()

    with st.expander("Advanced Inputs"):
        heat_loss_heat_network = st.number_input("Heat loss in heat network (%)",value=10,)
        wacc = st.number_input("WACC (%)",value=3,)
        grid_expansion_cost_eur_per_kw = st.number_input("Grid expansion cost decentralized (€ / kW) *ref. [2]*",value=1000,)
        grid_expansion_cost_eur_per_kw_centralized = st.number_input("Grid expansion cost centralized (€ / kW) *ref. [2]*", value=650,)


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

            results_df = pd.DataFrame({"Metric": ["Peak Demand","Annual CO₂ Emissions",
                                                  "Heat System CAPEX","Grid CAPEX",
                                                  "Annual OPEX","Total Annual Costs",
                                                  "LCoE Heat",],
                                        "Value": [f"{results['peak_city_electricity_demand']:,.0f} kW",
                                                  f"{results['annual_co2']/1000:,.0f} ton/year",
                                                  f"€{results['annual_capex']:,.0f}",
                                                  f"€{results['annual_grid_capex']:,.0f}",
                                                  f"€{results['annual_city_opex']:,.0f}",
                                                  f"€{results['annual_total_costs']:,.0f}",
                                                  f"€{results['lcoe_heat']:.3f}/kWh",],})
            st.dataframe(results_df,hide_index=True,use_container_width=True,)

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

            results_df = pd.DataFrame({"Metric": ["Peak Demand","Annual CO₂ Emissions",
                                                  "Heat System CAPEX","Grid CAPEX",
                                                  "Annual OPEX","Total Annual Costs",
                                                  "LCoE Heat","Buffer volume"],
                                        "Value": [f"{results['peak_city_electricity_demand']:,.0f} kW",
                                                  f"{results['annual_co2']/1000:,.0f} ton/year",
                                                  f"€{results['annual_capex']:,.0f}",
                                                  f"€{results['annual_grid_capex']:,.0f}",
                                                  f"€{results['annual_city_opex']:,.0f}",
                                                  f"€{results['annual_total_costs']:,.0f}",
                                                  f"€{results['lcoe_heat']:.3f}/kWh",
                                                  f"{results['buffer_volume']*1000:,.0f} L",],})
            st.dataframe(results_df,hide_index=True,use_container_width=True,)

        elif scenario == "Collective Heat System":
            results = run_scenario_3(
            houses=houses,
            annual_electricity_demand_kwh=electricity_demand,
            annual_heat_demand_gj=heat_demand,
            analysis_year=analysis_year,
            capex_per_house=capex_per_house_3,
            heatpump_lifetime_years=heatpump_lifetime_years_3,
            wacc=wacc,
            grid_expansion_cost_eur_per_kw_centralized=grid_expansion_cost_eur_per_kw_centralized,
            )
            
            st.header("Scenario Results")

            results_df = pd.DataFrame({"Metric": ["Peak Demand","Annual CO₂ Emissions",
                                                  "Heat System CAPEX","Grid CAPEX",
                                                  "Annual OPEX","Total Annual Costs",
                                                  "LCoE Heat",],
                                        "Value": [f"{results['peak_city_electricity_demand']:,.0f} kW",
                                                  f"{results['annual_co2']/1000:,.0f} ton/year",
                                                  f"€{results['annual_capex']:,.0f}",
                                                  f"€{results['annual_grid_capex']:,.0f}",
                                                  f"€{results['annual_city_opex']:,.0f}",
                                                  f"€{results['annual_total_costs']:,.0f}",
                                                  f"€{results['lcoe_heat']:.3f}/kWh",],})
            st.dataframe(results_df,hide_index=True,use_container_width=True,)

        elif scenario == "Collective Heat System + Seasonal Buffer":
            results = run_scenario_4(
            houses=houses,
            annual_electricity_demand_kwh=electricity_demand,
            annual_heat_demand_gj=heat_demand,
            analysis_year=analysis_year,
            capex_per_house=capex_per_house_4,
            heatpump_lifetime_years=heatpump_lifetime_years_4,
            wacc=wacc,
            grid_expansion_cost_eur_per_kw_centralized=grid_expansion_cost_eur_per_kw_centralized,
            delta_t_buffer_seasonal = delta_t_buffer_seasonal,
            buffer_cost_per_m3 = buffer_cost_per_m3_4,
            )
            
            st.header("Scenario Results")

            results_df = pd.DataFrame({"Metric": ["Peak Demand","Annual CO₂ Emissions",
                                                  "Heat System CAPEX","Grid CAPEX", "Buffer CAPEX",
                                                  "Annual OPEX","Total Annual Costs",
                                                  "LCoE Heat","Buffer volume"],
                                        "Value": [f"{results['peak_city_electricity_demand']:,.0f} kW",
                                                  f"{results['annual_co2']/1000:,.0f} ton/year",
                                                  f"€{results['annual_capex']:,.0f}",
                                                  f"€{results['annual_grid_capex']:,.0f}",
                                                  f"€{results['buffer_capex']:,.0f}",
                                                  f"€{results['annual_city_opex']:,.0f}",
                                                  f"€{results['annual_total_costs']:,.0f}",
                                                  f"€{results['lcoe_heat']:.3f}/kWh",
                                                  f"{results['buffer_volume']:,.0f} m³",],})
            st.dataframe(results_df,hide_index=True,use_container_width=True,)

        elif scenario == "Collective Heat System + Two-Week Buffer":
            results = run_scenario_5(
            houses=houses,
            annual_electricity_demand_kwh=electricity_demand,
            annual_heat_demand_gj=heat_demand,
            analysis_year=analysis_year,
            capex_per_house=capex_per_house_5,
            heatpump_lifetime_years=heatpump_lifetime_years_5,
            wacc=wacc,
            grid_expansion_cost_eur_per_kw_centralized=grid_expansion_cost_eur_per_kw_centralized,
            delta_t_buffer_two_week = delta_t_buffer_two_week,
            buffer_cost_per_m3 = buffer_cost_per_m3_5,
            )
            
            st.header("Scenario Results")

            results_df = pd.DataFrame({"Metric": ["Peak Demand","Annual CO₂ Emissions",
                                                  "Heat System CAPEX","Grid CAPEX", "Buffer CAPEX",
                                                  "Annual OPEX","Total Annual Costs",
                                                  "LCoE Heat","Buffer volume"],
                                        "Value": [f"{results['peak_city_electricity_demand']:,.0f} kW",
                                                  f"{results['annual_co2']/1000:,.0f} ton/year",
                                                  f"€{results['annual_capex']:,.0f}",
                                                  f"€{results['annual_grid_capex']:,.0f}",
                                                  f"€{results['buffer_capex']:,.0f}",
                                                  f"€{results['annual_city_opex']:,.0f}",
                                                  f"€{results['annual_total_costs']:,.0f}",
                                                  f"€{results['lcoe_heat']:.3f}/kWh",
                                                  f"{results['buffer_volume']:,.0f} m³",],})
            st.dataframe(results_df,hide_index=True,use_container_width=True,)

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

        if "Collective Heat System" in selected_scenarios:
            results["Collective Heat System"] = run_scenario_3(
                houses=houses,
                annual_electricity_demand_kwh=electricity_demand,
                annual_heat_demand_gj=heat_demand,
                analysis_year=analysis_year,
                capex_per_house=capex_per_house_3,
                heatpump_lifetime_years=heatpump_lifetime_years_3,
                wacc=wacc,
                grid_expansion_cost_eur_per_kw_centralized=grid_expansion_cost_eur_per_kw_centralized,
                )

        if "Collective Heat System + Seasonal Buffer" in selected_scenarios:
            results["Collective Heat System + Seasonal Buffer"] = run_scenario_4(
                houses=houses,
                annual_electricity_demand_kwh=electricity_demand,
                annual_heat_demand_gj=heat_demand,
                analysis_year=analysis_year,
                capex_per_house=capex_per_house_4,
                heatpump_lifetime_years=heatpump_lifetime_years_4,
                wacc=wacc,
                grid_expansion_cost_eur_per_kw_centralized=grid_expansion_cost_eur_per_kw_centralized,
                delta_t_buffer_seasonal=delta_t_buffer_seasonal,
                buffer_cost_per_m3=buffer_cost_per_m3_4
                )

        if "Collective Heat System + Two-Week Buffer" in selected_scenarios:
            results["Collective Heat System + Two-Week Buffer"] = run_scenario_5(
                houses=houses,
                annual_electricity_demand_kwh=electricity_demand,
                annual_heat_demand_gj=heat_demand,
                analysis_year=analysis_year,
                capex_per_house=capex_per_house_5,
                heatpump_lifetime_years=heatpump_lifetime_years_5,
                wacc=wacc,
                grid_expansion_cost_eur_per_kw_centralized=grid_expansion_cost_eur_per_kw_centralized,
                delta_t_buffer_two_week=delta_t_buffer_two_week,
                buffer_cost_per_m3=buffer_cost_per_m3_5
                )

        comparison_df = pd.DataFrame({scenario_name: {
            "Peak Demand (kW)": f"{scenario_results['peak_city_electricity_demand']:,.0f}",
            "CO₂ (ton/year)": f"{scenario_results['annual_co2'] / 1000:,.0f}",
            "Annual Costs (€)": f"€{scenario_results['annual_total_costs']:,.0f}",
            "LCoE Heat (€/kWh)": f"€{scenario_results['lcoe_heat']:.2f}",
            "Buffer volume (m³)": f"{scenario_results.get('buffer_volume', 0):,.1f}" if 'buffer_volume' in scenario_results else "N/A"
            } for scenario_name, scenario_results in results.items()})

        st.subheader("Scenario Comparison")
        st.dataframe(comparison_df,use_container_width=True,)


st.divider()

st.subheader("References")

st.markdown("""
**[1]** CBS, https://opendata.cbs.nl/#/CBS/nl/ 

**[2]** CE Delft (2024), *Het effect van het stagneren van de groei van warmtenetten - Wat als de ontwikkeling van warmtenetten niet op gang komt*, Publicatienummer: 24.240411.179.

https://ce.nl/publicaties/het-effect-van-het-stagneren-van-de-groei-van-warmtenetten/

**[3]** Mileucentraal, https://www.milieucentraal.nl/energie-besparen/inzicht-in-je-energierekening/gemiddeld-energieverbruik/ 

""")
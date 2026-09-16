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

st.title("Warmtenetten als onderdeel van het energiesysteem")

st.subheader("rekenmodel om vergelijk te maken tussen individuele en collectieve systemen met en zonder warmte buffers ")

st.markdown("""
#### Introductie

Dit rekenmodel is ontwikkeld als onderdeel van het programma Nieuwe Warmte Nu.
Met dit rekenmodel kan een vergelijking worden gemaakt tussen individuele
warmtesystemen en collectieve warmtesystemen voor een gehele stad. Daarnaast kan
inzichtelijk worden gemaakt wat de meerwaarde is van een warmtebuffer.

De resultaten worden vergeleken op basis van elektriciteitsvraag, piekvermogen,
CO₂-uitstoot en kosten. De gebruikte data en aannames die worden gebruikt in het
rekenmodel zijn beschreven in het rapport: *Warmtenetten als onderdeel van het energiesysteem - Een vergelijk tussen
individuele en collectieve systemen met en zonder warmtebuffers, Deltares
referentie: 11208818-029-USP-0001, datum 10-09-2026.*

#### Disclaimer

Het staat een ieder vrij de resultaten berekend met dit model te gebruiken voor
eigen intern, niet-commercieel gebruik, maar het model is niet geschikt om
(ontwerp)beslissingen op te baseren.

Deltares heeft dit rekenmodel opgezet om snel inzicht te kunnen geven in de
verschillen tussen individuele en collectieve systemen en in de kansen van
buffering binnen warmtesystemen. Dit rekenmodel wordt daarom aangeboden zonder
garantie van welke aard dan ook. Het gebruik ervan is voor eigen rekening en
risico.

Deltares / Nieuwe Warmte Nu is in geen geval aansprakelijk voor schade ontstaan
door gebruik van dit rekenmodel. Als de uitkomsten van het rekenmodel aanleiding
geven voor verder onderzoek, raden wij aan de verdere dimensionering uit te
laten voeren door een gespecialiseerd adviesbureau.

*Anton de Fockert, Ronald Roosjen*  
*Deltares, 10 september 2026*
""")

st.divider()


with st.sidebar:
    mode = st.radio("Methode",["Los scenario","Vergelijk scenario's",])

    if mode == "Los scenario":
        scenario = st.selectbox("Scenario",["Individuele warmtepomp","Individuele warmtepomp + dagbuffer","Collectief warmtesysteem","Collectief warmtesysteem + seizoenbuffer","Collectief warmtesysteem + twee weken buffer"],index=0,)

        if scenario == "Individuele warmtepomp":
            with st.expander("Scenario specifieke instellingen"):
                capex_per_house_1 = st.number_input("CAPEX (€ per huis)",value=7000.0,)
                heatpump_lifetime_years_1 = st.number_input("Levensduur warmtepomp (jaren)",value=15,key="single_s1_lifetime",)

        elif scenario == "Individuele warmtepomp + dagbuffer":
            with st.expander("Scenario specifieke instellingen"):
                capex_per_house_2 = st.number_input("CAPEX (€ per huis)",value=8500.0,)
                heatpump_lifetime_years_2 = st.number_input("Levensduur warmtepomp (jaren)",value=15,key="single_s2_lifetime",)
                delta_t_buffer = st.number_input("Buffer ΔT (°C)", value=20.0,)

        elif scenario == "Collectief warmtesysteem":
            with st.expander("Scenario specifieke instellingen"):
                capex_per_house_3 = st.number_input("CAPEX (€ per huis)",value=15000.0,key="single_s3_capex",)
                heatpump_lifetime_years_3 = st.number_input("Levensduur warmtesysteem (jaren)",value=30,key="single_s3_lifetime",)

        elif scenario == "Collectief warmtesysteem + seizoenbuffer":
            with st.expander("Scenario specifieke instellingen"):
                capex_per_house_4 = st.number_input("CAPEX (€ per huis)",value=15000.0,key="single_s4_capex",)
                heatpump_lifetime_years_4 = st.number_input("Levensduur warmtesysteem (jaren)",value=30,key="single_s4_lifetime",)
                delta_t_buffer_seasonal = st.number_input("Seizoensbuffer ΔT (°C)", value=50.0,)
                buffer_cost_per_m3_4 = st.number_input("Buffer CAPEX (€ / m³)",value=50.0, key="single_s4_buffer_cost")

        elif scenario == "Collectief warmtesysteem + twee weken buffer":
            with st.expander("Scenario specifieke instellingen"):
                capex_per_house_5 = st.number_input("CAPEX (€ per huis)",value=15000.0,key="single_s5_capex",)
                heatpump_lifetime_years_5 = st.number_input("Levensduur warmtesysteem (jaren)",value=30,key="single_s5_lifetime",)
                delta_t_buffer_two_week = st.number_input("Twee weken buffer ΔT (°C)", value=50.0,)
                buffer_cost_per_m3_5 = st.number_input("Buffer CAPEX (€ / m³)",value=50.0, key="single_s5_buffer_cost")


    if mode == "Vergelijk scenario's":
        st.subheader("Scenarios")

        selected_scenarios = []

        if st.checkbox("Individuele warmtepomp",value=False,):
            selected_scenarios.append("Individuele warmtepomp")

        if st.checkbox("Individuele warmtepomp + dagbuffer",value=False,):
            selected_scenarios.append("Individuele warmtepomp + dagbuffer")

        if st.checkbox("Collectief warmtesysteem",value=False,):
            selected_scenarios.append("Collectief warmtesysteem")

        if st.checkbox("Collectief warmtesysteem + seizoenbuffer",value=False,):
            selected_scenarios.append("Collectief warmtesysteem + seizoenbuffer")

        if st.checkbox("Collectief warmtesysteem + twee weken buffer",value=False,):
            selected_scenarios.append("Collectief warmtesysteem + twee weken buffer")

        if "Individuele warmtepomp" in selected_scenarios:
            with st.sidebar.expander("Instellingen 'Individuele warmtepomp'"):
                capex_per_house_1 = st.number_input("CAPEX (€ per huis)",value=7000.0,)
                heatpump_lifetime_years_1 = st.number_input("Levensduur warmtepomp (jaren)",value=15,key="compare_s1_lifetime",)
        
        if "Individuele warmtepomp + dagbuffer" in selected_scenarios:
            with st.sidebar.expander("Instellingen 'Individuele warmtepomp + dagbuffer'"):
                capex_per_house_2 = st.number_input("CAPEX (€ per huis)",value=8500.0,)
                heatpump_lifetime_years_2 = st.number_input("Levensduur warmtepomp (jaren)",value=15,key="compare_s2_lifetime",)
                delta_t_buffer = st.number_input("Buffer ΔT (°C)",value=20.0,)

        if "Collectief warmtesysteem" in selected_scenarios:
                    with st.sidebar.expander("Instellingen 'Collectief warmtesysteem'"):
                        capex_per_house_3 = st.number_input("CAPEX (€ per house)",value=15000.0,key="compare_s3_capex",)
                        heatpump_lifetime_years_3 = st.number_input("Heat system lifetime (years)",value=30,key="compare_s3_lifetime",)

        if "Collectief warmtesysteem + seizoenbuffer" in selected_scenarios:
                    with st.sidebar.expander("Instellingen 'Collectief warmtesysteem + seizoenbuffer'"):
                        capex_per_house_4 = st.number_input("CAPEX (€ per huis)",value=15000.0,key="compare_s4_capex",)
                        heatpump_lifetime_years_4 = st.number_input("Levensduur warmtepomp (jaren)",value=30,key="compare_s4_lifetime",)
                        delta_t_buffer_seasonal = st.number_input("Seizoensbuffer ΔT (°C)",value=50.0,)
                        buffer_cost_per_m3_4 = st.number_input("Buffer CAPEX (€ / m³)",value=50.0, key="compare_s4_buffer_cost")

        if "Collectief warmtesysteem + twee weken buffer" in selected_scenarios:
                    with st.sidebar.expander("Instellingen 'Collectief warmtesysteem + twee weken buffer'"):
                        capex_per_house_5 = st.number_input("CAPEX (€ per huis)",value=15000.0,key="compare_s5_capex",)
                        heatpump_lifetime_years_5 = st.number_input("Levensduur warmtepomp (jaren)",value=30,key="compare_s5_lifetime",)
                        delta_t_buffer_two_week = st.number_input("Twee weken buffer ΔT (°C)",value=50.0,)
                        buffer_cost_per_m3_5 = st.number_input("Buffer CAPEX (€ / m³)",value=50.0, key="compare_s5_buffer_cost")

    st.divider()
    if mode == "Los scenario":
        calculate = st.button( "Bereken scenario", use_container_width=True,)

    elif mode == "Vergelijk scenario's":
        calculate_comparison = st.button( "Vergelijk scenario's", use_container_width=True,)

    st.divider()

    st.header("Algemene instellingen")
    analysis_year = st.selectbox("Analysejaar",["2018","2019","2020","2021","2022","2023","2024","2025","2030","2035","2040","2050"],index=7,)
    houses = st.number_input("Aantal huizen", value=82000,)
    electricity_demand = st.number_input("Elektriciteitsvraag per huis (kWh/jaar)",value=2500,)
    heat_demand = st.number_input("Warmtevraag per huis (GJ/jaar)",value=31,)

    st.divider()

    with st.expander("Geavanceerde instellingen"):
        heat_loss_heat_network = st.number_input("Warmteverlies in het warmtenet (%)",value=10,)
        wacc = st.number_input("WACC (%)",value=3,)
        grid_expansion_cost_eur_per_kw = st.number_input("Netuitbreidingskosten gedecentraliseerd (€ / kW)",value=1000,)
        grid_expansion_cost_eur_per_kw_centralized = st.number_input("Netuitbreidingskosten gecentraliseerd (€ / kW)", value=650,)


if mode == "Los scenario":

    if calculate:
        if scenario == "Individuele warmtepomp":

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
            
            st.header("Resultaten")

            results_df = pd.DataFrame({"Indicator": ["Piekvraag","Jaarlijkse CO₂-uitstoot",
                                                  "Warmtesysteem CAPEX","Netwerk CAPEX",
                                                  "Jaarlijkse OPEX","Totale jaarlijkse kosten",
                                                  "LCoE Warmte",],
                                        "Waarde": [f"{results['peak_city_electricity_demand']:,.0f} kW",
                                                  f"{results['annual_co2']/1000:,.0f} ton/year",
                                                  f"€{results['annual_capex']:,.0f}",
                                                  f"€{results['annual_grid_capex']:,.0f}",
                                                  f"€{results['annual_city_opex']:,.0f}",
                                                  f"€{results['annual_total_costs']:,.0f}",
                                                  f"€{results['lcoe_heat']:.3f}/kWh",],})
            st.dataframe(results_df,hide_index=True,use_container_width=True,)

        elif scenario == "Individuele warmtepomp + Dagbuffer":
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
            
            
            st.header("Resultaten")

            results_df = pd.DataFrame({"Indicator": ["Piekvraag","Jaarlijkse CO₂-uitstoot",
                                                  "Warmtesysteem CAPEX","Netwerk CAPEX",
                                                  "Jaarlijkse OPEX","Totale jaarlijkse kosten",
                                                  "LCoE Warmte","Buffervolume"],
                                        "Waarde": [f"{results['peak_city_electricity_demand']:,.0f} kW",
                                                  f"{results['annual_co2']/1000:,.0f} ton/year",
                                                  f"€{results['annual_capex']:,.0f}",
                                                  f"€{results['annual_grid_capex']:,.0f}",
                                                  f"€{results['annual_city_opex']:,.0f}",
                                                  f"€{results['annual_total_costs']:,.0f}",
                                                  f"€{results['lcoe_heat']:.3f}/kWh",
                                                  f"{results['buffer_energy']:,.0f} kWh",
                                                  f"{results['buffer_volume']*1000:,.0f} L",],})
            st.dataframe(results_df,hide_index=True,use_container_width=True,)

        elif scenario == "Collectief warmtesysteem":
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
            
            st.header("Resultaten")

            results_df = pd.DataFrame({"Indicator": ["Piekvraag","Jaarlijkse CO₂-uitstoot",
                                                  "Warmtesysteem CAPEX","Netwerk CAPEX",
                                                  "Jaarlijkse OPEX","Totale jaarlijkse kosten",
                                                  "LCoE Warmte",],
                                        "Waarde": [f"{results['peak_city_electricity_demand']:,.0f} kW",
                                                  f"{results['annual_co2']/1000:,.0f} ton/year",
                                                  f"€{results['annual_capex']:,.0f}",
                                                  f"€{results['annual_grid_capex']:,.0f}",
                                                  f"€{results['annual_city_opex']:,.0f}",
                                                  f"€{results['annual_total_costs']:,.0f}",
                                                  f"€{results['lcoe_heat']:.3f}/kWh",],})
            st.dataframe(results_df,hide_index=True,use_container_width=True,)

        elif scenario == "Collectief warmtesysteem + seizoenbuffer":
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
            
            st.header("Resultaten")

            results_df = pd.DataFrame({"Indicator": ["Piekvraag","Jaarlijkse CO₂-uitstoot",
                                                  "Warmtesysteem CAPEX","Netwerk CAPEX", "Buffer CAPEX",
                                                  "Jaarlijkse OPEX","Totale jaarlijkse kosten",
                                                  "LCoE Warmte","Bufferenergie","Buffervolume"],
                                        "Waarde": [f"{results['peak_city_electricity_demand']:,.0f} kW",
                                                  f"{results['annual_co2']/1000:,.0f} ton/year",
                                                  f"€{results['annual_capex']:,.0f}",
                                                  f"€{results['annual_grid_capex']:,.0f}",
                                                  f"€{results['buffer_capex']:,.0f}",
                                                  f"€{results['annual_city_opex']:,.0f}",
                                                  f"€{results['annual_total_costs']:,.0f}",
                                                  f"€{results['lcoe_heat']:.3f}/kWh",
                                                  f"{results['buffer_energy']/1_000_000:,.1f} GWh",
                                                  f"{results['buffer_volume']:,.0f} m³ (20 x {(results['buffer_volume']/20)**0.5:,.0f} × {(results['buffer_volume']/20)**0.5:,.0f} m)",],})
            st.dataframe(results_df,hide_index=True,use_container_width=True,)

        elif scenario == "Collectief warmtesysteem + twee weken buffer":
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
            
            st.header("Resultaten")

            results_df = pd.DataFrame({"Indicator": ["Piekvraag","Jaarlijkse CO₂-uitstoot",
                                                  "Warmtesysteem CAPEX","Netwerk CAPEX", "Buffer CAPEX",
                                                  "Jaarlijkse OPEX","Totale jaarlijkse kosten",
                                                  "LCoE Warmte","Bufferenergie","Buffervolume"],
                                        "Waarde": [f"{results['peak_city_electricity_demand']:,.0f} kW",
                                                  f"{results['annual_co2']/1000:,.0f} ton/year",
                                                  f"€{results['annual_capex']:,.0f}",
                                                  f"€{results['annual_grid_capex']:,.0f}",
                                                  f"€{results['buffer_capex']:,.0f}",
                                                  f"€{results['annual_city_opex']:,.0f}",
                                                  f"€{results['annual_total_costs']:,.0f}",
                                                  f"€{results['lcoe_heat']:.3f}/kWh",
                                                  f"{results['buffer_energy']/1_000_000:,.1f} GWh",
                                                  f"{results['buffer_volume']:,.0f} m³ (20 x {(results['buffer_volume']/20)**0.5:,.0f} × {(results['buffer_volume']/20)**0.5:,.0f} m)",],})
            st.dataframe(results_df,hide_index=True,use_container_width=True,)

if mode == "Vergelijk scenario's":

    if calculate_comparison:

        results = {}

        if "Individuele warmtepomp" in selected_scenarios:
            results["Individuele warmtepomp"] = run_scenario_1(
                houses=houses,
                annual_electricity_demand_kwh=electricity_demand,
                annual_heat_demand_gj=heat_demand,
                analysis_year=analysis_year,
                capex_per_house=capex_per_house_1,
                heatpump_lifetime_years=heatpump_lifetime_years_1,
                wacc=wacc,
                grid_expansion_cost_eur_per_kw=grid_expansion_cost_eur_per_kw,
                )

        if "Individuele warmtepomp + dagbuffer" in selected_scenarios:
            results["Individuele warmtepomp + dagbuffer"] = run_scenario_2(
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

        if "Collectief warmtesysteem" in selected_scenarios:
            results["Collectief warmtesysteem"] = run_scenario_3(
                houses=houses,
                annual_electricity_demand_kwh=electricity_demand,
                annual_heat_demand_gj=heat_demand,
                analysis_year=analysis_year,
                capex_per_house=capex_per_house_3,
                heatpump_lifetime_years=heatpump_lifetime_years_3,
                wacc=wacc,
                grid_expansion_cost_eur_per_kw_centralized=grid_expansion_cost_eur_per_kw_centralized,
                )

        if "Collectief warmtesysteem + seizoenbuffer" in selected_scenarios:
            results["Collectief warmtesysteem + seizoenbuffer"] = run_scenario_4(
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

        if "Collectief warmtesysteem + twee weken buffer" in selected_scenarios:
            results["Collectief warmtesysteem + twee weken buffer"] = run_scenario_5(
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
            "Piekvraag (kW)": f"{scenario_results['peak_city_electricity_demand']:,.0f}",
            "Jaarlijkse CO₂-uitstoot (ton/jaar)": f"{scenario_results['annual_co2'] / 1000:,.0f}",
            "Totale jaarlijkse kosten (€)": f"€{scenario_results['annual_total_costs']:,.0f}",
            "LCoE Warmte (€/kWh)": f"€{scenario_results['lcoe_heat']:.2f}",
            "Bufferenergie (GWh)": (f"{scenario_results['buffer_energy']/1_000_000:,.1f}"
                                    if "buffer_energy" in scenario_results 
                                    else "N/A"),
            "Buffervolume (m³)": (f"{scenario_results['buffer_volume']:,.0f} m³ "
                                  f"(20 × {(scenario_results['buffer_volume']/20)**0.5:,.0f} × {(scenario_results['buffer_volume']/20)**0.5:,.0f} m)"
                                  if "buffer_volume" in scenario_results
                                  else "N/A"),} for scenario_name, scenario_results in results.items()})

        st.subheader("Scenario vergelijking")
        st.dataframe(comparison_df,use_container_width=True,)


#st.divider()

#st.subheader("References")

#st.markdown("""
#**[1]** CBS, https://opendata.cbs.nl/#/CBS/nl/ 

#**[2]** CE Delft (2024), *Het effect van het stagneren van de groei van warmtenetten - Wat als de ontwikkeling van warmtenetten niet op gang komt*, Publicatienummer: 24.240411.179.

#https://ce.nl/publicaties/het-effect-van-het-stagneren-van-de-groei-van-warmtenetten/

#**[3]** Mileucentraal, https://www.milieucentraal.nl/energie-besparen/inzicht-in-je-energierekening/gemiddeld-energieverbruik/ 

#""")
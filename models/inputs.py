from dataclasses import dataclass


@dataclass
class GeneralInputs:
    houses: int
    electricity_demand_kwh_per_house: float
    heat_demand_gj_per_house: float
    heat_loss_pct: float
    analysis_year: int
    wacc_pct: float
    decentral_grid_cost_eur_per_kw: float
    central_grid_cost_eur_per_kw: float
    grid_cost_eur_per_kwh: float
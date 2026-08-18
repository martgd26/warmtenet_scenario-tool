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


@dataclass
class IndividualHeatPumpInputs:
    capex_eur: float
    lifetime_years: int


@dataclass
class IndividualHeatPumpBufferInputs:
    capex_eur: float
    lifetime_years: int
    buffer_hours: float
    delta_t_buffer: float


@dataclass
class CollectiveHeatNetworkInputs:
    capex_eur: float
    lifetime_years: int


@dataclass
class CollectiveSeasonBufferInputs:
    network_capex_eur: float
    buffer_capex_eur: float
    network_lifetime_years: int
    buffer_lifetime_years: int
    delta_t_buffer: float


@dataclass
class CollectiveTwoWeekBufferInputs:
    network_capex_eur: float
    buffer_capex_eur: float
    network_lifetime_years: int
    buffer_lifetime_years: int
    delta_t_buffer: float
    buffer_days: float
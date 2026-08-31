import pandas as pd

def load_profiles(analysis_year):

    electricity_df = pd.read_csv("data/electricity_profile.csv",sep="\t",)
    electricity_profile = (electricity_df["Electriciteitsprofiel from ned.nl (standaard dag profiel)"]
        /electricity_df["Electriciteitsprofiel from ned.nl (standaard dag profiel)"].sum())
    
    heat_df = pd.read_csv("data/heat_profile.csv",sep="\t",)

    co2_df = pd.read_csv("data/co2_profiles.csv",sep="\t",)
    co2_profile = co2_df[analysis_year]

    price_df = pd.read_csv("data/electricity_prices.csv",sep="\t",)

    price_profile = (price_df[analysis_year].str.replace("€", "", regex=False)
                     .str.strip().replace("-", "0").astype(float))

    return (electricity_profile,heat_df,co2_profile,price_profile,)
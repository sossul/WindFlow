import pandas as pd

def get_data():
    url = "../raw_data/2022_viento_dmc.csv"
    df = pd.read_csv(url)
    df[df['nombreEstacion'] == 'El Loa, Calama Ad.']
    df["time"] = pd.to_datetime(df["time"])
    df.set_index('time', inplace=True)
    return df

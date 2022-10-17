import numpy as np
import datetime
import pandas as pd

def wind_transform(df):

    df['wd_x'] = np.cos(df['WDIR']*np.pi/180)*df['WSPD']
    df['wd_y'] = np.sin(df['WDIR']*np.pi/180)*df['WSPD']


    date_time = pd.to_datetime(df.pop('fecha'))
    timestamp_s = date_time.map(pd.Timestamp.timestamp)
    day = 24*12*60
    year = (365.2425)*day

    df['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
    df['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
    df['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
    df['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))


    return df[['TEMP','wd_x','wd_y','Day sin','Day cos', 'Year sin', 'Year cos']]

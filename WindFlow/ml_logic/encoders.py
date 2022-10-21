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

def wind_transform2(df):
    df['wd_x'] = np.cos(df['WDIR']*np.pi/180)*df['WSPD']
    df['wd_y'] = np.sin(df['WDIR']*np.pi/180)*df['WSPD']
    #date_time = pd.to_datetime(df.pop('fecha'))
    #timestamp_s = date_time.map(pd.Timestamp.timestamp)
    df.drop(columns=['WDIR', 'WSPD'], inplace=True)
    timestamp_s = df.index.map(pd.Timestamp.timestamp)
    day = 24*60*60
    year = (365.2425)*day

    df['Day sin'] = np.sin(timestamp_s * (2 * np.pi / day))
    df['Day cos'] = np.cos(timestamp_s * (2 * np.pi / day))
    df['Year sin'] = np.sin(timestamp_s * (2 * np.pi / year))
    df['Year cos'] = np.cos(timestamp_s * (2 * np.pi / year))
    return df


def pred_df(df):
    standarization_values = pd.read_csv('WindFlow/data/standarization_values.csv', index_col = 0)

    train_mean = standarization_values['mean']
    train_std = standarization_values['std']


    df["fecha"] = pd.to_datetime(df["fecha"], format = "%Y/%m/%d %H:%M:%S")
    df.set_index('fecha', inplace=True)
    df = df[['WDIR010', 'WSPD010', 'STWD010', 'SWSP010', 'TEMP010', 'PRES002', 'RHUM000']].copy()

    df.columns = ['WDIR', 'WSPD', 'STWD', 'SWSP', 'TEMP', 'PRES', 'RHUM']
    outliers = df['PRES'] < 700
    median = df.median()
    df['PRES'] = df['PRES'].mask(outliers, other=median)
    df = wind_transform2(df).copy()
    df = df.fillna(df.mean())

    x_pred = (df - train_mean) / train_std

    x_pred = x_pred.to_numpy()
    x_pred = np.expand_dims(x_pred, axis=0)
    return x_pred


def inverse_std():
    standarization_values = pd.read_csv('WindFlow/data/standarization_values.csv', index_col = 0)

    norm_x = standarization_values.loc['wd_x']
    norm_y = standarization_values.loc['wd_y']

    mean_x = norm_x['mean']
    mean_y = norm_y['mean']

    std_x =  norm_x['std']
    std_y =  norm_y['std']

    return mean_x, mean_y, std_x, std_y

import time
import datetime
import pandas as pd
import requests
import numpy as np

def dateToTimestamp(fecha, hora):
    '''
    Recibe '%Y-%m-%d' , '%H:%M:%S' y retorna timestamp
    '''
    timestamp = int((time.mktime(time.strptime((f"{fecha} {hora}"), '%Y-%m-%d %H:%M:%S'))))
    timestamp = timestamp - 14400 + 3600
    return (timestamp)

def timestampToDate(timestamp):
    '''
    Recibe un int de timestamp y retorna un string asi '%Y-%m-%d %H:%M:%S'
    '''
    dt_obj = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
    print (type(dt_obj))
    return dt_obj

def get_data(fechaInicio, horaInicio, fechaFin, horaFin, variable, estacion, frecuencia):
    '''
    Recibe fecha inicio como string'%Y-%m-%d', hora inicio como string '%H:%M:%S', fecha final como string'%Y-%m-%d',
    hora final como string '%H:%M:%S', variable a evaluar, estacion y frecuencia de la data (horaria + | diaria * | minutal , | 15min q )
    '''
    tsi = dateToTimestamp(fechaInicio, horaInicio)
    tsf = dateToTimestamp(fechaFin, horaFin)
    tsi_s = str(tsi)
    tsf_s = str(tsf)

    url = f"https://airviro.r9.cl/api/v1/domain/CODELCO/timeserie/{estacion}{frecuencia}M{variable}010/{tsi_s}/{tsf_s}/"

    print('fecha inicio de la solicitud',datetime.datetime.utcfromtimestamp(tsi).strftime('%Y-%m-%d %H:%M:%S'))
    print('fecha final',datetime.datetime.utcfromtimestamp(tsf).strftime('%Y-%m-%d %H:%M:%S'))

    headers = {
        'Authenticator': 'K1ykGBjKDDWzAnVfYa2Lahs24_4_uyptAeaq83I98gIa73-e5rxw0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Cookie': 'SESSID=OFYZH_xi5nyXFYtgDxWn9XUXDZO7bHqF7aXLFDOo3UVROa2LDuqV0',
    }

    params = {'username':'apicodelco',
            'password':'codelco.,2022'}

    response = requests.get(url, headers=headers, params=params).json()
    df = pd.DataFrame(response['data']['timeserie'])
    df_list = []
    df_list.append(df)
    try:
        next_url = response['links']['next']
        print('next url')
        while next_url is not None:
            print('entr?? while')
            response = requests.get(next_url, headers=headers).json()
            df_list.append(pd.DataFrame(response['data']['timeserie']))
            try:
                print('en while next url')
                next_url = response['links']['next']
            except:
                print('en while fin')
                next_url = None
    except:
        print('no hay next url, primer except')

    df = pd.concat(df_list)
    df['fecha'] = df['timestamp'].apply(lambda x : datetime.datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
    df[variable] = df['value']
    df = df.drop(columns= ['value'])
    return df

def get_data_multiparam(fechaInicio, horaInicio, fechaFin, horaFin, list_param, estacion, frecuencia):
    '''
    Recibe fecha inicio como string'%Y-%m-%d', hora inicio como string '%H:%M:%S', fecha final como string'%Y-%m-%d',
    hora final como string '%H:%M:%S', variable a evaluar, estacion y frecuencia de la data (horaria + | diaria * | minutal , | 15min q )
    '''
    df_list =  [get_data(fechaInicio, horaInicio, fechaFin, horaFin, param, estacion, frecuencia) for param in list_param]
    df = df_list[0]
    for i in range(len(list_param)):
        df[list_param[i]] = df_list[i][list_param[i]]
    return df

def get_data_ts(fechaInicio, fechaFin, variable, estacion, frecuencia):
    #url = f"https://airviro.r9.cl/api/v1/domain/CODELCO/timeserie/{estacion}{frecuencia}M{variable}010/{fechaInicio}/{fechaFin}/"
    url = f"https://airviro.r9.cl/api/v1/domain/CODELCO/timeserie/{estacion}{frecuencia}M{variable}/{fechaInicio}/{fechaFin}/"

    tsi = int(fechaInicio)
    tsf = int(fechaFin)
    print('fecha inicio de la solicitud',datetime.datetime.utcfromtimestamp(tsi).strftime('%Y-%m-%d %H:%M:%S'))
    print('fecha final',datetime.datetime.utcfromtimestamp(tsf).strftime('%Y-%m-%d %H:%M:%S'))
    headers = {
        'Authenticator': 'K1ykGBjKDDWzAnVfYa2Lahs24_4_uyptAeaq83I98gIa73-e5rxw0',
        'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        'Cookie': 'SESSID=OFYZH_xi5nyXFYtgDxWn9XUXDZO7bHqF7aXLFDOo3UVROa2LDuqV0',
    }
    params = {'username':'apicodelco',
            'password':'codelco.,2022'}
    response = requests.get(url, headers=headers, params=params).json()
    df = pd.DataFrame(response['data']['timeserie'])
    df_list = []
    df_list.append(df)
    try:
        next_url = response['links']['next']
        print('next url')
        while next_url is not None:
            print('entr?? while')
            response = requests.get(next_url, headers=headers).json()
            df_list.append(pd.DataFrame(response['data']['timeserie']))
            try:
                print('en while next url')
                next_url = response['links']['next']
            except:
                print('en while fin')
                next_url = None
    except:
        print('no hay next url, primer except')
    df = pd.concat(df_list)
    df['fecha'] = df['timestamp'].apply(lambda x : datetime.datetime.utcfromtimestamp(x).strftime('%Y-%m-%d %H:%M:%S'))
    df[variable] = df['value']
    df = df.drop(columns= ['value'])
    return df


def get_data_multiparam_ts(fechaInicio, fechaFin, list_param, estacion, frecuencia):
    df_list =  [get_data_ts(fechaInicio, fechaFin, param, estacion, frecuencia) for param in list_param]
    df = df_list[0]
    for i in range(len(list_param)):
        df[list_param[i]] = df_list[i][list_param[i]]
    return df

def get_data_to_predict(fechaInicio, horaInicio ,estacion, frecuencia, window, list_param):
    timestamp_f = dateToTimestamp(fechaInicio, horaInicio)
    timestamp_i = timestamp_f- window*60 - 60
    df = get_data_multiparam_ts(timestamp_i,timestamp_f, list_param, estacion, frecuencia)
    df = df[5::5]
    return df

def get_data_to_evaluate(fechaInicio, horaInicio ,estacion, frecuencia, window, list_param):
    timestamp_i = dateToTimestamp(fechaInicio, horaInicio) - 60
    timestamp_f = timestamp_i+ window*60 + 60
    df = get_data_multiparam_ts(timestamp_i,timestamp_f, list_param, estacion, frecuencia)
    df = df[5::5]
    return df

def get_csv(fechaInicio, horaInicio, fechaFin, horaFin, list_param, estacion, frecuencia):
    '''
    Recibe fecha inicio como string'%Y-%m-%d', hora inicio como string '%H:%M:%S', fecha final como string'%Y-%m-%d',
    hora final como string '%H:%M:%S', variable a evaluar, estacion y frecuencia de la data (horaria + | diaria * | minutal , | 15min q )
    '''
    df= get_data_multiparam(fechaInicio, horaInicio, fechaFin, horaFin, list_param, estacion, frecuencia)
    df.to_csv('newdata.csv')

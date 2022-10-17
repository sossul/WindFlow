import numpy as np
import math

def toCircular(df, wd):

    df['sin']=np.sin(df[wd]/360*2*math.pi)

    df['cos']=np.cos(df[wd]/360*2*math.pi)

    print("toCircular columns created")

def convertToDegrees(Wd_x,Wd_y):
	'''
	Converting sine and cosine back to its circular angle depends on finding which of the the 4 circular quadrants the
	prediction will fall into. If sin and cos are both GT 0, degrees will fall in 0-90.  If sin>0 cos<0, degrees will fall into 90-180, etc.
	'''
	#quadrant1
	if Wd_x > 0 and Wd_y > 0:
		return  np.arctan(Wd_y/Wd_x)*180/np.pi
	#quadrant2
	if Wd_x < 0 and Wd_y > 0:
		return  np.arctan(Wd_y/Wd_x)*180/np.pi + 180
	#quadrant3
	if Wd_x < 0 and Wd_y < 0:
		return  np.arctan(Wd_y/Wd_x)*180/np.pi + 180
	#quadrant4
	if Wd_x > 0 and Wd_y < 0:
		return  np.arctan(Wd_y/Wd_x)*180/np.pi + 360

def v_total(wd_x,wd_y):
  return np.sqrt(wd_x**2 + wd_y**2)



import time
import datetime
import pandas as pd
import requests

def get_data(fechaInicio, fechaFin, variable, estacion, frecuencia):
    url = f"https://airviro.r9.cl/api/v1/domain/CODELCO/timeserie/{estacion}{frecuencia}M{variable}010/{fechaInicio}/{fechaFin}/"
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
            print('entró while')
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


def get_data_multiparam(fechaInicio, fechaFin, list_param, estacion, frecuencia):
    df_list =  [get_data(fechaInicio, fechaFin, param, estacion, frecuencia) for param in list_param]
    df = df_list[0]
    for i in range(len(list_param)):
        df[list_param[i]] = df_list[i][list_param[i]]
    return df

def dateToTimestamp(fecha, hora):
    '''
    Recibe '%d-%m-%Y' , '%H:%M' y retorna timestamp
    '''

    timestamp = int((time.mktime(time.strptime((f"{fecha} {hora}"), '%Y-%m-%d %H:%M'))))
    timestamp = timestamp - 14400
    return (timestamp)

def timestampToDate(timestamp):
    '''
    Recibe un int de timestamp y retorna un string asi '%d-%m-%y %H:%M'
    '''
    dt_obj = datetime.fromtimestamp(timestamp).strftime('%y-%m-%d %H:%M')
    print (type(dt_obj))
    return dt_obj

def get_data_to_predict(fecha, hora,estacion, frecuencia, window, list_param):
    timestamp_f = dateToTimestamp(fecha, hora)
    timestamp_i = timestamp_f- window*60
    df = get_data_multiparam(timestamp_i,timestamp_f, list_param, estacion, frecuencia)
    df = df.set_index('fecha')
    return df[list_param]

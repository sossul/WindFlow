import streamlit as st

import numpy as np
import pandas as pd
import datetime
import requests
from visions import Time



st.markdown("""# WindFlow
## It is an app that predicts wind speed and direction for a given location.
Due to the fact that certain cities are located near mining centers,
these places are exposed to microparticle contamination from dynamite blasting activities, which makes it extremely urgent to predict wind speed and direction in order to properly program these activities and thus reduce the propagation radius of these microparticles.""")

st.sidebar.markdown("# Main page 🎈")


st.caption('On the map below you can see (in the blue dots) the locations of the copper mine works. Near and to the south of these is the city of Calama, which has a population of 180,283. Currently it presents many pollution problems linked to the work of the mine, with the following work we seek to reduce the environmental impact by knowing the best moments of operation.')

###############################################################
#######################    MAPA    ############################
###############################################################

from streamlit_folium import st_folium
import folium
from numpy import mean

coordinatesSI4 = [-22.3049, -68.8986] # estacion SI4
coordinatesSIO = [-22.4053, -68.9108] # estacion SIO
coordinatesGAA = [-22.3588, -68.8899] # estacion GAA

testmap = folium.Map(location=[-22.37, -68.90], zoom_start=11.65)
folium.Marker(coordinatesSI4, tooltip='SI4').add_to(testmap)
folium.Circle(coordinatesSI4, radius=300 ).add_to(testmap)
folium.Marker(coordinatesSIO, tooltip='SIO').add_to(testmap)
folium.Circle(coordinatesSIO, radius=300 ).add_to(testmap)
folium.Marker(coordinatesGAA, tooltip='RT1').add_to(testmap)
folium.Circle(coordinatesGAA, radius=300 ).add_to(testmap)

st_folium(testmap)

option = st.selectbox(
    'Choose the station to predict the wind direction and speed',
    ('RT1', 'SI0', 'SI4'))
st.write('You selected:', option)

d = st.date_input(
    "Fecha:",
    datetime.date(2022, 1, 4))
st.write('Fecha:', d)

t = st.time_input('Hora', datetime.time(8, 45))
st.write('Hora:', t)


#URL = "https://windflow-uiovyej6ca-ew.a.run.app/predict"

URL = "http://127.0.0.1:8000/predict"

PARAMS = {'fecha':d,
        'hora':t}
r = requests.get(url = URL, params = PARAMS)
data = r.json()
# st.write('predict:', data)

URL = "http://127.0.0.1:8000/evaluate"
PARAMS = {'fecha':d,
        'hora':t}
r = requests.get(url = URL, params = PARAMS)
data_true = r.json()

df = pd.concat([pd.DataFrame(data_true), pd.DataFrame(data)], axis=1)
# st.dataframe(df)

import numpy as np
import math

col_wspd = df.true_SPD.values.tolist()
col_wspd_np = np.array(col_wspd)

col_wdir = df.true_DIR.values.tolist()
col_wdir_np = np.array(col_wdir)

col_time = df.date_hour.values.tolist()

col_wspd_pred = df.pred_SPD.values.tolist()
col_wspd_pred_np = np.array(col_wspd_pred)

col_wdir_pred = df.pred_DIR.values.tolist()
col_wdir_pred_np = np.array(col_wdir_pred)

col_time = df.date_hour.values.tolist()

import matplotlib.pyplot as plt

n = 10
wind_speed = col_wspd_np[-10:]
wind_dir = col_wdir_np[-10:]
time = col_time[-10:]
time =[x[10:16] for x in time]
Y = [0] * n

U = np.cos(wind_dir/180. * math.pi) * wind_speed
V = np.sin(wind_dir/180. * math.pi) * wind_speed

wind_speed_pred = col_wspd_pred_np[-10:]
wind_dir_pred = col_wdir_pred_np[-10:]
time = col_time[-10:]
time =[x[10:16] for x in time]
Y_PRED = [0] * n


U_PRED = np.cos(wind_dir/180. * math.pi) * wind_speed_pred
V_PRED = np.sin(wind_dir/180. * math.pi) * wind_speed_pred


plt.style.use('dark_background')
fig, ax = plt.subplots()
quiver1 =ax.quiver(time, Y, U, V, color='b')
quiver2 =ax.quiver(time, Y_PRED, U_PRED, V_PRED, color='r', alpha=0.6)
ax.legend([quiver1, quiver2], ['TRUE', 'PREDICTION'])
title = df.iloc[0]['date_hour'][:10]
ax.title.set_text(title)
st.pyplot(fig)

import seaborn as sns
import matplotlib.pyplot as plt

plt.style.use('dark_background')
fig = plt.figure(figsize=(20, 8))

df['hour'] = df['date_hour'].str[-8:].str[:5]
df_2 = df[0::2]

sns.lineplot(data= df_2, x=df_2['hour'] ,y= df_2['pred_SPD'], label='PREDICTION')
sns.lineplot(data= df_2, x=df_2['hour'],y= df_2['true_SPD'],label='TRUE')
plt.xticks(rotation=45)

font1 = {'family':'serif','color':'blue','size':20}
font2 = {'family':'serif','color':'darkred','size':15}

plt.title("SPEED PREDICTION 6 HOURS", fontdict = font1)
plt.xlabel("TIME", fontdict = font2)
plt.ylabel("SPEED IN M/S", fontdict = font2)
st.pyplot(fig)

fig = plt.figure(figsize=(20, 8))
sns.lineplot(data= df_2, x=df_2['hour'] ,y= df_2['pred_DIR'],label='PREDICTION')
sns.lineplot(data= df_2, x=df_2['hour'],y= df_2['true_DIR'],label='TRUE')
plt.xticks(rotation=45)

plt.title("DIRECTION PREDICTION 6 HOURS", fontdict = font1)
plt.xlabel("TIME", fontdict = font2)
plt.ylabel("DIRECTION IN DEGREES", fontdict = font2)
st.pyplot(fig)

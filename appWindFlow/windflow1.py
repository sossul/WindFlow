import streamlit as st

import numpy as np
import pandas as pd
import datetime
import requests



st.markdown("""# WindFlow
## It is an app that predicts wind speed and direction for a given location.
Due to the fact that certain cities are located near mining centers,
these places are exposed to microparticle contamination from dynamite blasting activities, which makes it extremely urgent to predict wind speed and direction in order to properly program these activities and thus reduce the propagation radius of these microparticles.""")

st.sidebar.markdown("# Main page 🎈")

# df= pd.read_csv("data.csv")
# this slider allows the user to select a number of lines
# to display in the dataframe
# the selected value is returned by st.slider

#line_count = st.slider('Select a line count', 1, 10, 3)

st.caption('On the map below you can see (in the blue dots) the locations of the copper mine works. Near and to the south of these is the city of Calama, which has a population of 180,283. Currently it presents many pollution problems linked to the work of the mine, with the following work we seek to reduce the environmental impact by knowing the best moments of operation.')

###############################################################
#######################    MAPA    ############################
###############################################################

from streamlit_folium import st_folium
import folium
from numpy import mean

coordinatesSI4 = [-22.3049, -68.8986] # estacion SI4
coordinatesSIO = [-22.4053, -68.9108] # estacion SIO
coordinatesGAA = [-23.4188, -68.7853] # estacion GAA

testmap = folium.Map(location=[-22.82, -68.86489999999999], zoom_start=9)
folium.Marker(coordinatesSI4, tooltip='SI4').add_to(testmap)
folium.Circle(coordinatesSI4, radius=300 ).add_to(testmap)
folium.Marker(coordinatesSIO, tooltip='SIO').add_to(testmap)
folium.Circle(coordinatesSIO, radius=300 ).add_to(testmap)
folium.Marker(coordinatesGAA, tooltip='GAA').add_to(testmap)
folium.Circle(coordinatesGAA, radius=300 ).add_to(testmap)

st_folium(testmap)



d = st.date_input(
    "Fecha:",
    datetime.date(2022, 1, 4))
st.write('Fecha:', d)

t = st.time_input('Hora', datetime.time(8, 45))
st.write('Hora:', t)

URL = "http://127.0.0.1:8000/predict"
PARAMS = {'fecha':d,
          'hora':t}
r = requests.get(url = URL, params = PARAMS)
data = r.json()
st.write('predict:', data)
###############################################################
####################    1ER GRÁFICO    ########################
###############################################################

import matplotlib.pyplot as plt
col_wspd = df.WSPD.values.tolist()
col_wspd_np = np.array(col_wspd)

col_wdir = df.WDIR.values.tolist()
col_wdir_np = np.array(col_wdir)

col_time = df.fecha.values.tolist()

n = 10
wind_speed = col_wspd_np[-10:]
wind_dir = col_wdir_np[-10:]
time = col_time[-10:]
time =[x[10:16] for x in time]
Y = [0] * n

U = np.cos(wind_dir) * wind_speed
V = np.sin(wind_dir) * wind_speed

plt.figure()
plt.quiver(time, Y, U, V)


fig, ax = plt.subplots()
ax.quiver(time, Y, U, V)



st.pyplot(fig)


###############################################################
######################    PREDICCIÓN    #######################
###############################################################




from PIL import Image
image = Image.open('unknown.png')

st.image(image, caption='Current prediction versus historical information')



# and used to select the displayed lines

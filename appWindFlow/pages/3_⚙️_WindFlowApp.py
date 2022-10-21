import streamlit as st
import os
import numpy as np
import pandas as pd
import datetime
import requests
#from visions import Time
import seaborn as sns
import matplotlib.pyplot as plt
import math
from PIL import Image
import streamlit as st



# def add_bg_from_url():
#     st.markdown(
#          f"""
#          <style>
#          .stApp {{
#              background-image: url("https://s3-us-west-2.amazonaws.com/enterreno-production/moments/photos/000/006/735/original/mina-de-chuquicamata-en-1950.jpg");
#              background-attachment: fixed;
#              background-size: cover
#          }}
#          </style>
#          """,
#          unsafe_allow_html=True
#      )

# add_bg_from_url()

# st.set_page_config(layout="wide")
# video_html = """
# 		<style>

# 		#myVideo {
# 		  position: fixed;
# 		  right: 0;
# 		  bottom: 0;
# 		  min-width: 100%;
# 		  min-height: 100%;
# 		}

# 		.content {
# 		  position: fixed;
# 		  bottom: 0;
# 		  background: rgba(0, 0, 0, 0.5);
# 		  color: #f1f1f1;
# 		  width: 100%;
# 		  padding: 20px;
# 		}

# 		</style>
# 		<video autoplay muted loop id="myVideo">
# 		  <source src="https://www.youtube.com/watch?v=wAEi9s9bEpY")>
# 		  Your browser does not support HTML5 video.
# 		</video>
#         """

# st.markdown(video_html, unsafe_allow_html=True)
# st.title('Video page')


###########
def add_logo():
    st.markdown(
        """
        <style>
            [data-testid="stSidebarNav"] {
                background-image: url(https://i.ibb.co/sHy0KCY/Foto-Jet-9.png);
                background-repeat: no-repeat;
                padding-top: 150px;
                background-position: 0px 15px;
            }
            [data-testid="stSidebarNav"]::before {
                content: "WindFlow 1.0.2";
                margin-left: 20px;
                margin-top: 20px;
                font-size: 15px;
                position: relative;
                top: 100px;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
#####
add_logo()



# from PIL import Image
# import streamlit as st

# You can always call this function where ever you want

# def add_logo(logo_path, width, height):
#     """Read and return a resized logo"""
#     logo = Image.open(logo_path)
#     modified_logo = logo.resize((width, height))
#     return modified_logo

# #my_logo = add_logo(logo_path="jaz_icono2.png", width=50, height=50)
# #st.sidebar.image(my_logo)

# # OR

# st.sidebar.image(add_logo(logo_path="jaz_icono2.png", width=50, height=50))

####




###




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
    datetime.date(2021, 12, 15))
st.write('Fecha:', d)

t = st.time_input('Hora', datetime.time(19, 00))
st.write('Hora:', t)


URL_pred = "https://windflow-uiovyej6ca-ew.a.run.app/predict"
URL_true = "https://windflow-uiovyej6ca-ew.a.run.app/evaluate"

PARAMS = {'fecha':d, 'hora':t}


def click():
    r_pred = requests.get(url = URL_pred, params = PARAMS)
    r_true = requests.get(url = URL_true, params = PARAMS)

    st.session_state.data_pred = r_pred.json()
    st.session_state.data_true = r_true.json()

button = st.button("Predict", on_click = click)

# if 'data_pred' not in st.session_state:
#     print('DATA NULL')




# r_pred = requests.get(url = URL_pred, params = PARAMS)
# r_true = requests.get(url = URL_true, params = PARAMS)

# st.session_state.data_pred = r_pred.json()
# st.session_state.data_true = r_true.json()

if 'data_pred' in st.session_state:
    print('ENTRO AL IF ENTRO AL IF')
    data_pred = st.session_state.data_pred
    data_true = st.session_state.data_true
    df = pd.concat([pd.DataFrame(data_true), pd.DataFrame(data_pred)], axis=1)



    #Grafico1
    df_7 = df[0::10]

    col_wspd = df_7.true_SPD.values.tolist()
    col_wspd_np = np.array(col_wspd)

    col_wdir = df_7.true_DIR.values.tolist()
    col_wdir_np = np.array(col_wdir)

    col_time = df_7.date_hour.values.tolist()

    col_wspd_pred = df_7.pred_SPD.values.tolist()
    col_wspd_pred_np = np.array(col_wspd_pred)

    col_wdir_pred = df_7.pred_DIR.values.tolist()
    col_wdir_pred_np = np.array(col_wdir_pred)

    col_time = df_7.date_hour.values.tolist()


    n = 8
    wind_speed = col_wspd_np
    wind_dir = col_wdir_np
    time = col_time
    time =[x[10:16] for x in time]
    Y = [0] * n

    U = np.cos(wind_dir/180. * math.pi) * wind_speed
    V = np.sin(wind_dir/180. * math.pi) * wind_speed

    wind_speed_pred = col_wspd_pred_np
    wind_dir_pred = col_wdir_pred_np
    time = col_time
    time =[x[10:16] for x in time]
    Y_PRED = [0] * n


    U_PRED = np.cos(wind_dir_pred/180. * math.pi) * wind_speed_pred
    V_PRED = np.sin(wind_dir_pred/180. * math.pi) * wind_speed_pred


    plt.style.use('dark_background')
    fig1, ax = plt.subplots()
    quiver1 =ax.quiver(time, Y, U, V, color='b')
    quiver2 =ax.quiver(time, Y_PRED, U_PRED, V_PRED, color='r', alpha=0.6)
    ax.legend([quiver1, quiver2], ['TRUE', 'PREDICTION'])
    ax.get_yaxis().set_ticks([])
    title = df.iloc[0]['date_hour'][:10]
    ax.title.set_text(title)
    st.pyplot(fig1)



    ### Grafico 2

    plt.style.use('dark_background')
    fig2 = plt.figure(figsize=(10, 4))

    df['hour'] = df['date_hour'].str[-8:].str[:5]
    df_2 = df[0::1]

    sns.lineplot(data= df_2, x=df_2['hour'] ,y= df_2['pred_SPD'], label='PREDICTION', color='red', linewidth=2.5)
    sns.lineplot(data= df_2, x=df_2['hour'],y= df_2['true_SPD'],label='TRUE', color='blue', linewidth=2.5)
    plt.xticks(rotation=45)
    plt.xticks(df_2['hour'][::4])

    font1 = {'family':'serif','color':'blue','size':20}
    font2 = {'family':'serif','color':'darkred','size':15}

    plt.title("SPEED PREDICTION 6 HOURS", fontdict = font1)
    plt.xlabel("TIME", fontdict = font2)
    plt.ylabel("SPEED IN M/S", fontdict = font2)
    st.pyplot(fig2)


    ###Grafico3
    fig3 = plt.figure(figsize=(10, 4))
    sns.lineplot(data= df_2, x=df_2['hour'] ,y= df_2['pred_DIR'],label='PREDICTION', color='red', linewidth=2.5)
    sns.lineplot(data= df_2, x=df_2['hour'],y= df_2['true_DIR'],label='TRUE', color='blue', linewidth=2.5)
    plt.xticks(rotation=45)
    plt.xticks(df_2['hour'][::4])

    plt.title("DIRECTION PREDICTION 6 HOURS", fontdict = font1)
    plt.xlabel("TIME", fontdict = font2)
    plt.ylabel("DIRECTION IN DEGREES", fontdict = font2)
    st.pyplot(fig3)




    # def show_graphs():
    #     st.pyplot(fig1)
    #     st.pyplot(fig2)
    #     st.pyplot(fig3)

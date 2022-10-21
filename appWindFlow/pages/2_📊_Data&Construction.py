import streamlit as st
import os
import numpy as np
import pandas as pd
import datetime
import requests
#from visions import Time
import seaborn as sns
import matplotlib.pyplot as plt
from PIL import Image
import streamlit as st

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

st.markdown("""## Data: ✍🏼
Real Data that we obtained is from a meteorological company in Chile, it is historical information of 05 years.
For each date and minute we have measurements of wind speed and direction as well as temperature and humidity. The data was delivered in an API, a dictionary with Json format that was converted into a Dataframe.""")

image = Image.open('appWindFlow/grafico.png')
st.image(image, caption='Historical data of the direction and force of the wind')

st.markdown("""## The model 🧑🏼‍🔬
Three models were tested and metrics were evaluated to find the best model (Bidirectional LSTM, Profet, Multivariate LSTM). The model that showed the best performance was the following, Bidirectional LSTM, which was the one used in the app.
## Application functionality 📱
It predicts the speed in (m/s) and the direction in (degrees°) for the next 06 hours according to the station, date and time indicated
""")


"""### Wind"""

file_ = open("/Users/francepoma/code/sebasdq/WindFlow/appWindFlow/tree wind.gif", "rb")
contents = file_.read()
data_url = base64.b64encode(contents).decode("utf-8")
file_.close()

st.markdown(
    f'<img src="data:image/gif;base64,{data_url}" alt="cat gif">',
    unsafe_allow_html=True,
)

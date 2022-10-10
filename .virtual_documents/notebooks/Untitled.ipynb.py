import pandas as pd
import matplotlib.pyplot as plt


url = "../raw_data/2022_viento_dmc.csv"
df = pd.read_csv(url)
df


df[['nombreEstacion']].value_counts()


df[df['nombreEstacion'] == 'El Loa, Calama Ad.']


#Transformamos la variable date a timestamp
df["time"] = pd.to_datetime(df["time"]) 
df.set_index('time', inplace=True) # Dejamos la fecha como index 


df.info()


df[['dd_Valor', 'ff_Valor']].plot(kind='line', figsize = (18,18), cmap='coolwarm', subplots = True, fontsize = 10)
plt.show()


df.head()


import plotly.express as px
fig = px.line(df.head(1000), x=df.head(1000).index, y="dd_Valor")
fig.show()


fig = px.line(df.head(1000), x=df.head(1000).index, y="ff_Valor")
fig.show()




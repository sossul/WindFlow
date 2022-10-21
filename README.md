#
![Alt text](WindFlow.png?raw=true "Title")

&nbsp;

# Windflow APP

It predicts the speed in (m/s) and the direction in (degrees°) for the next 06 hours according to the station, date and time indicated.

It is an application that helps mining companies to schedule the best time to operate dynamite blasting activities. This reduces the environmental impact generated by the propagation of particulate matter (dust)




## Demo

You can view the Demo in the following link:

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)]([https://windflow.herokuapp.com/](https://windflow.herokuapp.com/WindFlowApp))
- [Youtube Demo Day](https://www.youtube.com/watch?v=HZyLS1le0jQ)
- [Slides]((https://www.canva.com/design/DAFPpteOAt4/fcP2YAVPXLMD-vLufgjpDA/view?    utm_content=DAFPpteOAt4&utm_campaign=designshare&utm_medium=link&utm_source=publishsharelink))



## Authors

- [@sebasdq](https://github.com/sebasdq)
- [@John2671](https://github.com/John2671)
- [@sossul](https://github.com/sossul)
- [@FelipeUlloan](https://github.com/FelipeUlloan)
- [@FranceJazmine](https://github.com/FranceJazmine)


## Data Provenance:

- Real Data that we obtained is from a meteorological company in the city of Calama in Chile. It is historical information of 05 years.
- For each date and minute we have measurements of wind speed and direction as well as temperature and humidity. The data was delivered in an API, a dictionary with Json format that was converted into a Dataframe.


## The model:

- Three models were tested and metrics were evaluated to find the best model (Bidirectional LSTM, Profet, Multivariate LSTM). The model that showed the best performance was the following, Bidirectional LSTM, which was the one used in the app.


##

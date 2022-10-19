from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from data import get_data_to_predict, get_data_to_evaluate
from ml_logic.encoders import wind_transform
from keras.models import load_model
import numpy as np
import tensorflow as tf
from predict import pred
from utils import convertToDegrees, v_total

# from taxifare.ml_logic.preprocessor import preprocess_features

# from taxifare.ml_logic.registry import load_model

app = FastAPI()
app.state.model = load_model('model_saved.h5')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# http://127.0.0.1:8000/predict?pickup_datetime=2012-10-06 12:10:20&pickup_longitude=40.7614327&pickup_latitude=-73.9798156&dropoff_longitude=40.6513111&dropoff_latitude=-73.8803331&passenger_count=2
@app.get("/predict")

def predict(fecha, hora):

    df = get_data_to_predict(fecha, hora, 'RT1', ',', 60, ['WSPD','WDIR','TEMP'])
    x_pred = wind_transform(df)
    x_pred = x_pred.to_numpy()
    x_pred = np.expand_dims(x_pred, axis=0)
    y_pred = app.state.model.predict(x_pred)
    list_pred = y_pred[0].tolist()
    y_test_pred = [[[v_total(x[0],x[1]), convertToDegrees(x[0],x[1])] for x in y ] for y in y_pred]
    SPD_pred = [item[0] for item in y_test_pred[0]]
    DIR_pred = [item[1] for item in y_test_pred[0]]
    # return(y_test_pred)
    return {'pred_SPD':SPD_pred,
            'pred_DIR':DIR_pred
            }

@app.get("/evaluate")

def evaluate(fecha, hora):

    df = get_data_to_evaluate(fecha, hora, 'RT1', ',', 60, ['WSPD','WDIR','TEMP'])

    return {'true_SPD':list(df['WSPD']),
            'true_DIR':list(df['WDIR'])
            }

# def predict(pickup_datetime: datetime,  # 2013-07-06 17:18:00
#             pickup_longitude: float,    # -73.950655
#             pickup_latitude: float,     # 40.783282
#             dropoff_longitude: float,   # -73.984365
#             dropoff_latitude: float,    # 40.769802
#             passenger_count: int):      # 1
#     """
#     we use type hinting to indicate the data types expected
#     for the parameters of the function
#     FastAPI uses this information in order to hand errors
#     to the developpers providing incompatible parameters
#     FastAPI also provides variables of the expected data type to use
#     without type hinting we need to manually convert
#     the parameters of the functions which are all received as strings
#     """

#     X_pred =pd.DataFrame(dict(
#             key=["2013-07-06 17:18:00"],  # useless but the pipeline requires it
#             pickup_datetime=pickup_datetime,
#             pickup_longitude=pickup_longitude,
#             pickup_latitude=pickup_latitude,
#             dropoff_longitude=dropoff_longitude,
#             dropoff_latitude=dropoff_latitude,
#             passenger_count=passenger_count))

#     X_processed = preprocess_features(X_pred)

#     y_pred = app.state.model.predict(X_processed)

#     return {'fare':float(y_pred)}


@app.get("/")
def root():
    return {'greeting': 'Hello'}

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


@app.get("/")
def root():
    return {'greeting': 'Hello'}

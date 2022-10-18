from matplotlib.pyplot import get
from data import get_data_to_predict
from WindFlow.ml_logic.encoders import wind_transform
from keras.models import load_model
import numpy as np
import tensorflow as tf

def pred(fecha, hora):

    df = get_data_to_predict(fecha, hora, 'RT1', ',', 60, ['WSPD','WDIR','TEMP'])
    x_pred = wind_transform(df)
    x_pred = x_pred.to_numpy()
    x_pred = np.expand_dims(x_pred, axis=0)
    pred_prueba_model = load_model('model_saved.h5')
    y_pred = pred_prueba_model.predict(x_pred)
    return y_pred

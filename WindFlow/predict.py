from turtle import shape
from matplotlib.pyplot import get
from data import get_data_to_predict
from ml_logic.encoders import wind_transform
from keras.models import load_model
import numpy as np
import tensorflow as tf
from utils import convertToDegrees, v_total

def pred(fecha, hora):

    df = get_data_to_predict(fecha, hora, 'RT1', ',', 60, ['WSPD','WDIR','TEMP'])
    x_pred = wind_transform(df)
    x_pred = x_pred.to_numpy()
    x_pred = np.expand_dims(x_pred, axis=0)
    pred_prueba_model = load_model('model_saved.h5')
    y_pred = pred_prueba_model.predict(x_pred)
    list_pred = y_pred[0].tolist()
    y_test_pred = [[[v_total(x[0],x[1]), convertToDegrees(x[0],x[1])] for x in y ] for y in y_pred]
    SPD_pred = [item[0] for item in y_test_pred[0]]
    DIR_pred = [item[1] for item in y_test_pred[0]]
    # return(y_test_pred)
    return {'pred_SPD':SPD_pred,
            'pred_DIR':DIR_pred
            }

fecha = '2022-01-04'
hora = '16:00:00'
print(pred(fecha,hora))

from matplotlib.pyplot import get
from data import get_data_to_predict
from ml_logic.encoders import wind_transform
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
    list_pred = y_pred[0].tolist()
    wx = [item[0] for item in list_pred]
    wy = [item[1] for item in list_pred]
    return {'pred_wx':wx,
            'pred_wy':wy
            }

fecha = '2022-01-04'
hora = '16:00:00'
print(pred(fecha,hora))

from turtle import shape
from matplotlib.pyplot import get
from data import get_data_to_evaluate
from ml_logic.encoders import wind_transform
from keras.models import load_model
import numpy as np
import tensorflow as tf
from utils import convertToDegrees, v_total

fecha = '2022-01-04'
hora = '16:00:00'

def evaluate(fecha, hora):

    df = get_data_to_evaluate(fecha, hora, 'RT1', ',', 60, ['WSPD','WDIR','TEMP'])
    print (df)
    # return (df['WDIR'].tolist)
    return {'true_SPD':list(df['WSPD']),
            'true_DIR':list(df['WDIR'])
            }

print(evaluate(fecha, hora))

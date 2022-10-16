from WindFlow.utils import get_data_to_predict
from WindFlow.ml_logic.model import model_pred

import pandas as pd
import numpy as np

def pred(fecha, hora):

    x_pred = get_data_to_predict(fecha, hora, 'RT1', ',', 180, ['WDIR'])
    x_pred = np.squeeze([x_pred])
    x_pred = np.array([[x_pred]])

    df = pd.read_csv('WindFlow/data/data.csv')
    y = model_pred(df, x_pred)

    return y

# ax = pred('2022-10-10', '16:00')
# print(ax)

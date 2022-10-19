
from datetime import datetime
from sqlite3 import SQLITE_DROP_INDEX
import pandas as pd
from WindFlow.data import get_data_to_predict, get_data_to_evaluate
from WindFlow.ml_logic.encoders import pred_df, inverse_std
from keras.models import load_model
# import numpy as np
# import tensorflow as tf
# from predict import pred
from WindFlow.utils import convertToDegrees, v_total
import numpy as np



# model = load_model('new_model.h5')

# fecha = '2022-01-01'
# hora = '15:00:00'

# list_param = ['WDIR010', 'WSPD010','STWD010','SWSP010', 'TEMP010','EVAP000','PRES002','RHUM000']
# df = get_data_to_predict(fecha, hora, 'RT1', ',', 60*24,  list_param)

# x_pred = pred_df(df)
# y_pred = model.predict(x_pred)

# mean_x, mean_y, std_x, std_y = inverse_std()

# y_test_pred = [[[v_total((x[0]*std_x)+mean_x, (x[1]*std_y)+mean_y),
#                  convertToDegrees((x[0]*std_x)+mean_x,(x[1]*std_y)+mean_y)] for x in y ] for y in y_pred]


# SPD_pred = [round(item[0],1) for item in y_test_pred[0]]
# DIR_pred = [round(item[1],0) for item in y_test_pred[0]]

# print({'pred_SPD':SPD_pred,
#             'pred_DIR':DIR_pred
#             })


fecha = '2022-01-01'
hora = '15:00:00'

df = get_data_to_evaluate(fecha, hora, 'RT1', ',', 60*6, ['WSPD010','WDIR010'])

print(df)

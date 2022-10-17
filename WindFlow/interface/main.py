from curses import window
from statistics import mode
from WindFlow.ml_logic.multi_ltsm import init_model, evaluate_model, compile_and_fit_model
import pandas as pd
from WindFlow.ml_logic.encoders import wind_transform
from WindFlow.ml_logic.windowclass import WindowGenerator
from keras.models import load_model
import matplotlib.pyplot as plt
import numpy as np

from WindFlow.ml_logic.preprocessor import preprocess_features


def train_test_split(df):

    column_indices = {name: i for i, name in enumerate(df.columns)}
    n = len(df)
    train_df = df[0:int(n*0.7)]
    val_df = df[int(n*0.7):int(n*0.9)]
    test_df = df[int(n*0.9):]

    num_features = df.shape[1]
    return train_df, val_df, test_df, num_features, column_indices


def train():
    df = pd.read_csv('WindFlow/data/data.csv')

    df=df[['fecha','WDIR','WSPD','TEMP']]
    df = df[1::5]


    train_df, val_df, test_df, num_features, column_indices = train_test_split(df)

    train_df = preprocess_features(train_df)
    print(train_df)
    val_df = preprocess_features(val_df)
    test_df = preprocess_features(test_df)

    OUT_STEPS = 12
    input_width=12
    label_columns= ['wd_x', 'wd_y']
    window = WindowGenerator(input_width=input_width, label_width=OUT_STEPS,shift=OUT_STEPS,label_columns=label_columns,
        train_df = train_df, val_df = val_df, test_df = test_df)

    print(type(df))
    print(window)
    model = init_model(OUT_STEPS=OUT_STEPS, NUM_FEATURES= 2)
    model, history = compile_and_fit_model(model, window=window, patience=1)

    model.save('model_saved.h5')
    print('trained')
    return window

def evaluate(window):
    model = load_model('model_saved.h5')
    eval = evaluate_model(model,window=window)
    print(eval)


window = train()
evaluate(window)

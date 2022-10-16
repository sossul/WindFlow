# LTSM univariate

from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np
import pandas as pd

from keras.models import Sequential
from keras.layers import Dense, LSTM
from tensorflow.keras.callbacks import EarlyStopping


def create_dataset(dataset, look_back=1):
    X, Y = [], []
    for i in range(look_back, len(dataset)):
        a = dataset[i-look_back:i, 0]
        X.append(a)
        Y.append(dataset[i, 0])
    return np.array(X), np.array(Y)


def model_pred(df, X_pred):

    data =  df[['WDIR']]
    #Convert the dataframe to a numpy array
    dataset = data.values

    scaler = MinMaxScaler(feature_range=(-1, 0))
    #scaler = StandardScaler()

    scaled_data = scaler.fit_transform(dataset)


    # Defines the rolling window
    look_back = 180
    train_size = int(0.85 * len(df))
    test_size = len(df) - train_size

    # Split into train and test sets
    train, test = scaled_data[:train_size-look_back,:], scaled_data[train_size-look_back:,:]


    x_train, y_train = create_dataset(train, look_back)
    x_test, y_test = create_dataset(test, look_back)

    # reshape input to be [samples, time steps, features]
    x_train = np.reshape(x_train, (x_train.shape[0], 1, x_train.shape[1]))
    x_test = np.reshape(x_test, (x_test.shape[0], 1, x_test.shape[1]))

    print(len(x_train), len(x_test))

    #Build the LSTM model

    es = EarlyStopping(patience= 15, restore_best_weights=True)

    model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape=(x_train.shape[1], x_train.shape[2])))
    model.add(LSTM(64, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    # Compile the model
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=["mae"])

    #Train the model
    model.fit(x_train, y_train, batch_size=16, epochs=1, validation_data=(x_test, y_test), callbacks = [es])

    # Lets predict with the model
    pred = model.predict(X_pred)

    # invert predictions

    pred = scaler.inverse_transform(pred)

    return pred

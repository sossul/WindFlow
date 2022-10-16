from colorama import Fore, Style

import numpy as np

from keras.models import Sequential
from keras.layers import Model, Dense, LSTM
from tensorflow.keras.callbacks import EarlyStopping

from typing import Tuple

def initialize_model(X: np.ndarray) -> Model:
    """
    Initialize the Neural Network with random weights
    """
    print(Fore.BLUE + "\nInitialize model..." + Style.RESET_ALL)

    model = Sequential()
    model.add(LSTM(128, return_sequences=True, input_shape=(X.shape[1], X.shape[2])))
    model.add(LSTM(64, return_sequences=False))
    model.add(Dense(25))
    model.add(Dense(1))

    print("\n✅ model initialized")

    return model

def compile_model(model: Model) -> Model:
    """
    Compile the Neural Network
    """
    model.compile(optimizer='adam', loss='mean_squared_error', metrics=["mae"])

    print("\n✅ model compiled")
    return model


def train_model(model: Model,
                x_train: np.ndarray,
                y_train: np.ndarray,
                x_test,
                y_test,
                batch_size=64,
                patience=2) -> Tuple[Model, dict]:
    """
    Fit model and return a the tuple (fitted_model, history)
    """

    print(Fore.BLUE + "\nTrain model..." + Style.RESET_ALL)

    es = EarlyStopping(monitor="val_loss",
                       patience=patience,
                       restore_best_weights=True,
                       verbose=0)


    history = model.fit(x_train,
                        y_train,
                        batch_size=batch_size,
                        epochs=20,
                        validation_data=(x_test, y_test),
                        callbacks = [es])


    print(f"\n✅ model trained ({len(X)} rows)")

    return model, history

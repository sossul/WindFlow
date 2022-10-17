from colorama import Fore, Style
import tensorflow as tf
# from tensorflow.keras.layers import Normalization
# norm_layer = Normalization()
# norm_layer.adapt(train_df)
def init_model(OUT_STEPS, NUM_FEATURES):
    print(Fore.BLUE + "\nInitialize model..." + Style.RESET_ALL)
    multi_lstm_model = tf.keras.Sequential([
        # Shape [batch, time, features] => [batch, lstm_units].
        # Adding more `lstm_units` just overfits more quickly.


        # norm_layer,
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(256, return_sequences=True)),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(128, return_sequences=True)),
        tf.keras.layers.Bidirectional(tf.keras.layers.LSTM(64, return_sequences=False)),
        #tf.keras.layers.LSTM(128, return_sequences=False),
        # Shape => [batch, out_steps*features].
        tf.keras.layers.Dense(OUT_STEPS*NUM_FEATURES,
                            kernel_initializer=tf.initializers.zeros()),
        # Shape => [batch, out_steps, features].
        tf.keras.layers.Reshape([OUT_STEPS, NUM_FEATURES])
    ])
    print("\n✅ model initialized")
    return multi_lstm_model

def compile_and_fit_model(model, window, patience=2, MAX_EPOCHS=30):
    """
    Compile the Neural Network
    """
    early_stopping = tf.keras.callbacks.EarlyStopping(monitor='val_loss',
                                                    patience=patience,
                                                    mode='min')

    model.compile(loss=tf.keras.losses.MeanSquaredError(),
                    optimizer=tf.keras.optimizers.Adam(),
                    metrics=[tf.keras.metrics.MeanAbsoluteError()])
    print(Fore.RED + "compiled")

    history = model.fit(window.train, epochs=MAX_EPOCHS,
                        validation_data=window.val,
                        callbacks=[early_stopping])
    print(Fore.BLUE + "fitted")
    return model, history

def evaluate_model(model, window):
    """
    Evaluate trained model performance on dataset
    """

    print(Fore.BLUE + f"\nEvaluate model..." + Style.RESET_ALL)

    if model is None:
        print(f"\n❌ no model to evaluate")
        return None

    metrics = model.evaluate(window.test,
        verbose=1,
        # callbacks=None,
        return_dict=True)

    loss = metrics["loss"]
    mae = metrics["mean_absolute_error"]

    print(f"\n✅ model evaluated: loss {round(loss, 2)} mae {round(mae, 2)}")

    return metrics

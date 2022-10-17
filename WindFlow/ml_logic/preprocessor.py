from sklearn.pipeline import make_pipeline
from sklearn.compose import ColumnTransformer, make_column_transformer
from sklearn.preprocessing import OneHotEncoder, FunctionTransformer, StandardScaler


from WindFlow.ml_logic.encoders import wind_transform

import numpy as np
import pandas as pd

from colorama import Fore, Style


def preprocess_features(X: pd.DataFrame) -> np.ndarray:

    def create_sklearn_preprocessor() -> ColumnTransformer:
        """
        Create a scikit-learn preprocessor
        that transforms a cleaned dataset of shape (_, 7)
        into a preprocessed one of different fixed shape (_, 65)
        """


        X_train_min = X.min()
        X_train_max = X.max()
        pipe = make_pipeline(
            FunctionTransformer(wind_transform),
            StandardScaler()
        )

        return pipe

    columns = X.columns

    print(Fore.BLUE + "\nPreprocess features..." + Style.RESET_ALL)

    preprocessor = create_sklearn_preprocessor()

    X_processed = preprocessor.fit_transform(X)

    print("\n✅ X_processed, with shape", X_processed.shape)

    return pd.DataFrame(X_processed, columns = ['TEMP','wd_x','wd_y','Day sin','Day cos', 'Year sin', 'Year cos'])

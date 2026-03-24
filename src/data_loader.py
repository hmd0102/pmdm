import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


def load_data(path: str = "data/dataset.csv"):
    df = pd.read_csv(path)

    df = df.drop(["name", "header"], axis=1)

    df["contains_text"] = df["contains_text"].map({
        "Yes": 1,
        "No": 0
    })

    X = df.drop("class", axis=1)
    y = df["class"]

    return X, y


def prepare_data(
    path: str = "data/dataset.csv",
    test_size: float = 0.2,
    random_state: int = 42,
    scale: bool = False,
):

    X, y = load_data(path=path)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state, stratify=y
    )

    scaler = None
    if scale:
        scaler = StandardScaler()
        numeric_cols = X_train.select_dtypes(include="number").columns
        X_train[numeric_cols] = scaler.fit_transform(X_train[numeric_cols])
        X_test[numeric_cols] = scaler.transform(X_test[numeric_cols])

    return X_train, X_test, y_train, y_test, scaler

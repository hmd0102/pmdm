import pandas as pd

def load_data(path="data/dataset.csv"):
    df = pd.read_csv(path)
    df = df.drop(["name", "header"], axis=1)

    df["contains_text"] = df["contains_text"].map({
        "Yes": 1,
        "No": 0
    })

    X = df.drop("class", axis=1)
    y = df["class"]

    return X, y
import pandas as pd


def run(path: str = "data/dataset.csv"):
    df = pd.read_csv(path)

    print("=== Dataset shape ===")
    print(df.shape)
    print()

    print("=== Column dtypes ===")
    print(df.dtypes)
    print()

    print("=== Head (first 5 rows) ===")
    print(df.head())
    print()

    print("=== Summary statistics ===")
    print(df.describe(include="all"))
    print()

    print("=== Missing values per column ===")
    print(df.isna().sum())
    print()

    if "class" in df.columns:
        print("=== Target distribution (class) ===")
        print(df["class"].value_counts(dropna=False))
        print(df["class"].value_counts(normalize=True, dropna=False))
        print()

    if "contains_text" in df.columns:
        print("=== contains_text distribution ===")
        print(df["contains_text"].value_counts(dropna=False))
        print()


if __name__ == "__main__":
    run()

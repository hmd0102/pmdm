import argparse

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


def run(path: str = "data/dataset.csv", show_plots: bool = False, max_rows: int = 20):
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 240)

    df = pd.read_csv(path)

    print("=== Dataset shape ===")
    print(df.shape)
    print()

    print("=== Column dtypes ===")
    print(df.dtypes)
    print()

    print("=== Head (first rows) ===")
    print(df.head(max_rows))
    print()

    print("=== Unique values per column ===")
    print(df.nunique())
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

    if show_plots:
        # Plot distributions for numeric columns
        numeric_cols = df.select_dtypes(include="number").columns.tolist()
        if numeric_cols:
            df[numeric_cols].hist(bins=20, figsize=(12, 8), layout=(len(numeric_cols) // 4 + 1, 4))
            plt.suptitle("Numeric feature distributions")
            plt.tight_layout(rect=[0, 0.03, 1, 0.95])
            plt.show()

        # Correlation matrix for numeric features
        if len(numeric_cols) > 1:
            corr = df[numeric_cols].corr()
            plt.figure(figsize=(10, 8))
            sns.heatmap(corr, annot=False, cmap="coolwarm", center=0)
            plt.title("Correlation matrix")
            plt.show()


def _parse_args():
    parser = argparse.ArgumentParser(description="Simple EDA for dataset")
    parser.add_argument("--path", default="data/dataset.csv", help="Path to dataset CSV")
    parser.add_argument("--show-plots", action="store_true", help="Show histogram/correlation plots")
    parser.add_argument("--max-rows", type=int, default=20, help="Number of rows to show in head() output")
    return parser.parse_args()


if __name__ == "__main__":
    args = _parse_args()
    run(path=args.path, show_plots=args.show_plots, max_rows=args.max_rows)

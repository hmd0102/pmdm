import argparse
import os

import joblib

from src.data_loader import prepare_data
from src.eda import run as run_eda
from src.train import train_model
from src.evaluate import evaluate


def _parse_args():
    parser = argparse.ArgumentParser(description="Train/evaluate pipeline")
    parser.add_argument(
        "--mode",
        choices=["eda", "train", "evaluate", "all"],
        default="all",
        help="Pipeline mode: eda, train, evaluate, or all",
    )
    parser.add_argument("--data", default="data/dataset.csv", help="Path to dataset CSV")
    parser.add_argument("--model-path", default="model.joblib", help="Path to save/load the model")
    parser.add_argument("--test-size", type=float, default=0.2, help="Test set fraction")
    parser.add_argument("--random-state", type=int, default=42, help="Random seed")
    parser.add_argument(
        "--scale",
        action="store_true",
        help="Standardize numeric features before training",
    )
    parser.add_argument(
        "--show-plots",
        action="store_true",
        help="Show evaluation plots (confusion matrix + ROC) and EDA plots",
    )
    return parser.parse_args()


def main():
    args = _parse_args()

    if args.mode == "eda":
        run_eda(path=args.data, show_plots=args.show_plots)
        return

    X_train, X_test, y_train, y_test, _ = prepare_data(
        path=args.data,
        test_size=args.test_size,
        random_state=args.random_state,
        scale=args.scale,
    )

    model = None

    if args.mode in ("train", "all"):
        model = train_model(X_train, y_train, random_state=args.random_state)
        joblib.dump(model, args.model_path)
        print(f"Saved trained model to {args.model_path}")

    if args.mode in ("evaluate", "all"):
        if model is None:
            if os.path.exists(args.model_path):
                model = joblib.load(args.model_path)
                print(f"Loaded model from {args.model_path}")
            else:
                raise FileNotFoundError(
                    f"Model not found at {args.model_path}. Run with --mode train first."
                )

        evaluate(
            model,
            X_test,
            y_test,
            show_plots=args.show_plots,
            save_plots=True,
            plot_prefix="evaluation",
        )


if __name__ == "__main__":
    main()
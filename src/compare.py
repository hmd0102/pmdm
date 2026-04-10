from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from src.evaluate import evaluate
from src.data_loader import prepare_data
import joblib
import os


def get_candidate_models(random_state: int = 42) -> dict:
    return {
        "Random Forest":       RandomForestClassifier(n_estimators=100, random_state=random_state),
        "Decision Tree":       DecisionTreeClassifier(random_state=random_state),
        "Logistic Regression": LogisticRegression(max_iter=1000, random_state=random_state),
        "Gradient Boosting":   GradientBoostingClassifier(random_state=random_state),
        "SVM":                 SVC(probability=True, random_state=random_state),
    }


def compare_models(X_train, y_train, X_test, y_test, random_state: int = 42):
    candidates = get_candidate_models(random_state)
    best_model = None
    best_acc = -1

    for name, model in candidates.items():
        print(f"\n{'='*40}")
        print(f"Mô hình: {name}")
        print(f"{'='*40}")
        model.fit(X_train, y_train)
        evaluate(
            model, X_test, y_test,
            show_plots=False,
            save_plots=True,
            plot_prefix=f"results/{name.lower().replace(' ', '_')}",
        )
        acc = model.score(X_test, y_test)
        if acc > best_acc:
            best_acc = acc
            best_model = (name, model)

    print(f"\nMô hình tốt nhất: {best_model[0]} (accuracy={best_acc:.4f})")
    return best_model[1]


if __name__ == "__main__":
    X_train, X_test, y_train, y_test, _ = prepare_data(
        path="data/dataset.csv",
        test_size=0.2,
        random_state=42,
        scale=False,
    )

    best_model = compare_models(X_train, y_train, X_test, y_test)

    os.makedirs("models", exist_ok=True)
    joblib.dump(best_model, "models/best_model.joblib")
    print("Đã lưu: models/best_model.joblib")
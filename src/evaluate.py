from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    classification_report,
    roc_auc_score,
    roc_curve,
)
import seaborn as sns
import matplotlib.pyplot as plt


def evaluate(
    model,
    X_test,
    y_test,
    show_plots: bool = True,
    save_plots: bool = False,
    plot_prefix: str = "evaluation",
):
    y_pred = model.predict(X_test)

    print("Accuracy:", accuracy_score(y_test, y_pred))

    cm = confusion_matrix(y_test, y_pred)
    print("Confusion Matrix:")
    print(cm)

    print(classification_report(y_test, y_pred))

    fig, ax = plt.subplots(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", ax=ax)
    ax.set_xlabel("Predicted")
    ax.set_ylabel("Actual")
    ax.set_title("Confusion Matrix")

    if save_plots:
        fig.savefig(f"{plot_prefix}_confusion_matrix.png", bbox_inches="tight")
    if show_plots:
        plt.show()
    plt.close(fig)

    try:
        y_prob = model.predict_proba(X_test)
        if y_prob.shape[1] == 2:
            y_scores = y_prob[:, 1]
        else:
            y_scores = y_prob[:, 1]

        auc = roc_auc_score(y_test, y_scores)
        print("ROC AUC:", auc)

        fpr, tpr, _ = roc_curve(y_test, y_scores)
        fig, ax = plt.subplots(figsize=(5, 4))
        ax.plot(fpr, tpr, label=f"AUC = {auc:.3f}")
        ax.plot([0, 1], [0, 1], linestyle="--", color="gray")
        ax.set_xlabel("False Positive Rate")
        ax.set_ylabel("True Positive Rate")
        ax.set_title("ROC Curve")
        ax.legend(loc="lower right")

        if save_plots:
            fig.savefig(f"{plot_prefix}_roc_curve.png", bbox_inches="tight")
        if show_plots:
            plt.show()
        plt.close(fig)
    except Exception:
        pass

    if hasattr(model, "feature_importances_") and hasattr(X_test, "columns"):
        importances = model.feature_importances_
        features = X_test.columns
        fi = sorted(zip(features, importances), key=lambda x: x[1], reverse=True)
        print("\nTop 10 feature importances:")
        for name, score in fi[:10]:
            print(f"  {name}: {score:.4f}")

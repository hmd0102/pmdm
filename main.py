from sklearn.model_selection import train_test_split
from src.data_loader import load_data
from src.train import train_model
from src.evaluate import evaluate

# load data
X, y = load_data()

# split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# train
model = train_model(X_train, y_train)

# evaluate
evaluate(model, X_test, y_test)
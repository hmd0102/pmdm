from sklearn.ensemble import RandomForestClassifier


def train_model(X_train, y_train, random_state: int = 42, **rf_kwargs):
    model = RandomForestClassifier(random_state=random_state, **rf_kwargs)
    model.fit(X_train, y_train)
    return model
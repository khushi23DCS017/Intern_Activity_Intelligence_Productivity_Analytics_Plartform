# pyre-ignore-all-errors
import pickle
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def train_productivity_model(intern_summary, models_dir):
    """
    Trains Linear Regression to predict productivity_score
    from behavioral features only (not the formula inputs directly).

    Features: active_days, number_of_activities, tech_count
    Target  : productivity_score

    Saves → models/productivity_model.pkl
    """
    print("--> Training productivity regression model...")

    features = ['active_days', 'number_of_activities', 'tech_count']
    X = intern_summary[features]
    y = intern_summary['productivity_score']

    # 80/20 split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate on test set (unseen data)
    y_pred_test = model.predict(X_test)
    r2           = r2_score(y_test, y_pred_test)
    accuracy_pct = round(max(r2, 0) * 100, 2)

    # Predict on full dataset to store in summary
    intern_summary['predicted_productivity'] = model.predict(X)

    metrics = {
        "Train_Size"          : int(len(X_train)),
        "Test_Size"           : int(len(X_test)),
        "MAE"                 : round(float(mean_absolute_error(y_test, y_pred_test)), 4),
        "MSE"                 : round(float(mean_squared_error(y_test,  y_pred_test)), 4),
        "R2_Score"            : round(float(r2), 4),
        "Accuracy_Percentage" : f"{accuracy_pct}%"
    }
    print(f"  Regression metrics (test set): {metrics}")

    # Save to models/ directory
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, "productivity_model.pkl")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    print(f"  Saved → {model_path}")

    return intern_summary, model_path, metrics

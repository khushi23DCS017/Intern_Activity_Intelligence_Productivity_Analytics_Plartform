import pickle
import os
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

def train_productivity_model(intern_summary, ml_dir):
    print("--> Training the productivity regression model...")
    
    # using only behavioral/activity features to predict productivity
    # not using hours/score directly since they are part of the formula
    # this makes the model actually learn something meaningful
    features = ['active_days', 'number_of_activities', 'tech_count']
    X = intern_summary[features]
    y = intern_summary['productivity_score']
    
    # 80/20 train test split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # train only on training data
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # predict on test set (unseen data)
    y_pred_test = model.predict(X_test)
    
    # predict on full set to store in summary
    intern_summary['predicted_productivity'] = model.predict(X)
    
    # eval on test set only (this gives real accuracy)
    r2 = r2_score(y_test, y_pred_test)
    accuracy_pct = round(max(r2, 0) * 100, 2)  # clamp to 0 just in case
    
    metrics = {
        "Train_Size": len(X_train),
        "Test_Size": len(X_test),
        "MAE": round(mean_absolute_error(y_test, y_pred_test), 4),
        "MSE": round(mean_squared_error(y_test, y_pred_test), 4),
        "R2_Score": round(r2, 4),
        "Accuracy_Percentage": f"{accuracy_pct}%"
    }
    print(f"Regression metrics (on test set): {metrics}")
    
    # save model
    os.makedirs(ml_dir, exist_ok=True)
    model_path = os.path.join(ml_dir, "productivity_model.pkl")
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
        
    return intern_summary, model_path, metrics

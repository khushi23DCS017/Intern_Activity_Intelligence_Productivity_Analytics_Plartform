# pyre-ignore-all-errors
import pickle
import os
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score

def train_clustering_model(intern_summary, models_dir):
    """
    Trains KMeans (3 clusters) to segment interns into:
        High Performer / Consistent Contributor / Learning Phase

    Features: productivity_score, hours_spent, avg_score

    Saves → models/clustering_model.pkl
    """
    print("--> Training KMeans clustering model...")

    features = ['productivity_score', 'hours_spent', 'avg_score']
    X = intern_summary[features]

    # Scale before clustering
    scaler   = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    kmeans         = KMeans(n_clusters=3, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    intern_summary['cluster'] = cluster_labels

    # Evaluate
    metrics = {
        "Silhouette_Score"    : round(float(silhouette_score(X_scaled, cluster_labels)), 4),
        "Davies_Bouldin_Index": round(float(davies_bouldin_score(X_scaled, cluster_labels)), 4)
    }
    print(f"  KMeans metrics: {metrics}")

    # Map cluster numbers to readable labels
    # Sort by avg productivity: lowest → Learning Phase, highest → High Performer
    cluster_means = intern_summary.groupby('cluster')['productivity_score'].mean().sort_values()
    label_map = {
        cluster_means.index[0]: 'Learning Phase',
        cluster_means.index[1]: 'Consistent Contributor',
        cluster_means.index[2]: 'High Performer'
    }
    intern_summary['category'] = intern_summary['cluster'].map(label_map)
    print(f"  Cluster label map: {label_map}")

    # Save to models/ directory
    os.makedirs(models_dir, exist_ok=True)
    model_path = os.path.join(models_dir, "clustering_model.pkl")
    with open(model_path, 'wb') as f:
        pickle.dump({
            'scaler'   : scaler,
            'kmeans'   : kmeans,
            'label_map': label_map
        }, f)
    print(f"  Saved → {model_path}")

    return intern_summary, model_path, metrics

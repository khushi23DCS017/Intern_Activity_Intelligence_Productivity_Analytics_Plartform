import pickle
import os
import json
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, davies_bouldin_score

def train_clustering_model(intern_summary, ml_dir):
    print("--> Training KMeans to find intern groups...")
    
    # using these features for clustering
    features = ['productivity_score', 'hours_spent', 'avg_score']
    X = intern_summary[features]
    
    # scale the data first! (standard scaler)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_scaled)
    intern_summary['cluster'] = cluster_labels
    
    # scores to see if clustering is good
    metrics = {
        "Silhouette_Score": round(float(silhouette_score(X_scaled, cluster_labels)), 4),
        "Davies_Bouldin_Index": round(float(davies_bouldin_score(X_scaled, cluster_labels)), 4)
    }
    print(f"KMeans scores: {metrics}")
    
    # mapping labels based on avg productivity
    cluster_means = intern_summary.groupby('cluster')['productivity_score'].mean().sort_values()
    
    # 0 -> low, 1 -> mid, 2 -> high basically
    label_map = {
        cluster_means.index[0]: 'Learning Phase',
        cluster_means.index[1]: 'Consistent Contributor',
        cluster_means.index[2]: 'High Performer'
    }
    intern_summary['category'] = intern_summary['cluster'].map(label_map)
    
    # dump everything in pkl
    os.makedirs(ml_dir, exist_ok=True)
    model_path = os.path.join(ml_dir, "clustering_model.pkl")
    with open(model_path, 'wb') as f:
        pickle.dump({'scaler': scaler, 'kmeans': kmeans, 'label_map': label_map}, f)
        
    return intern_summary, model_path, metrics

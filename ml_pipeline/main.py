import os
import json
from load_data import load_data
from preprocessing import preprocess_data
from feature_engineering import compute_metrics
from train_model import train_productivity_model
from clustering_model import train_clustering_model
from generate_outputs import generate_outputs

# main execution logic for ml pipeline
def run_pipeline():
    # this is my local path, make sure to change if running somewhere else
    base_dir = r"e:\Intern Analysys"
    ml_dir = os.path.join(base_dir, "ml")
    viz_dir = os.path.join(base_dir, "visualizations")
    
    print(f"Starting pipeline in {base_dir} ...")
    
    # step 1 & 2: load and clean data
    activity_df, assignments_df = load_data(base_dir)
    activity_df, assignments_df = preprocess_data(activity_df, assignments_df)
    
    # step 3: build features
    intern_summary = compute_metrics(activity_df, assignments_df)
    
    # step 4: train both models
    intern_summary, prod_model_path, reg_metrics = train_productivity_model(intern_summary, ml_dir)
    intern_summary, clust_model_path, clust_metrics = train_clustering_model(intern_summary, ml_dir)
    
    # save metrics so frontend can use it
    evaluation_metrics = {
        "Productivity_Regression": reg_metrics,
        "Intern_Segmentation_KMeans": clust_metrics
    }
    with open(os.path.join(ml_dir, "model_evaluation.json"), "w") as f:
        json.dump(evaluation_metrics, f, indent=4)
        
    print(f"Saved evaluation metrics to json")
    
    # step 5: generate final csv and png
    generate_outputs(intern_summary, assignments_df, ml_dir, viz_dir)
    
    print("Pipeline finished successfully!!!")

if __name__ == "__main__":
    run_pipeline()

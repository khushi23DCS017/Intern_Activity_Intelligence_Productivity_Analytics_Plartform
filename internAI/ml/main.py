# pyre-ignore-all-errors
import os
import sys
import json

# Add parent dir so config.py is importable
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from load_data         import load_data
from preprocessing     import preprocess_data
from feature_engineering import compute_metrics
from train_model       import train_productivity_model
from clustering_model  import train_clustering_model
from generate_outputs  import generate_outputs
from train_classification import train_classification_model

def run_pipeline():
    # -------------------------------------------------------
    # PATHS — relative to project root, no hardcoding
    # -------------------------------------------------------
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    ml_dir       = os.path.join(project_root, "ml")
    models_dir   = os.path.join(project_root, "models")
    viz_dir      = os.path.join(project_root, "visualizations")

    os.makedirs(ml_dir,     exist_ok=True)
    os.makedirs(models_dir, exist_ok=True)
    os.makedirs(viz_dir,    exist_ok=True)

    print(f"Project root : {project_root}")
    print(f"ML outputs   : {ml_dir}")
    print(f"Models       : {models_dir}")
    print(f"Starting pipeline...\n")

    # -------------------------------------------------------
    # STEP 1 — Load from PostgreSQL
    # -------------------------------------------------------
    activity_df, assignments_df = load_data()

    # -------------------------------------------------------
    # STEP 2 — Preprocess
    # -------------------------------------------------------
    activity_df, assignments_df = preprocess_data(activity_df, assignments_df)

    # -------------------------------------------------------
    # STEP 3 — Feature Engineering
    # -------------------------------------------------------
    intern_summary = compute_metrics(activity_df, assignments_df)

    # -------------------------------------------------------
    # STEP 4 — Train Regression Model (productivity prediction)
    # Saves → models/productivity_model.pkl
    # -------------------------------------------------------
    intern_summary, prod_model_path, reg_metrics = train_productivity_model(
        intern_summary, models_dir
    )

    # -------------------------------------------------------
    # STEP 5 — Train Clustering Model (intern segmentation)
    # Saves → models/clustering_model.pkl
    # -------------------------------------------------------
    intern_summary, clust_model_path, clust_metrics = train_clustering_model(
        intern_summary, models_dir
    )

    # -------------------------------------------------------
    # STEP 6 — Save model_evaluation.json (regression + clustering)
    # -------------------------------------------------------
    evaluation_metrics = {
        "Productivity_Regression"   : reg_metrics,
        "Intern_Segmentation_KMeans": clust_metrics
    }
    eval_path = os.path.join(models_dir, "model_evaluation.json")
    with open(eval_path, "w") as f:
        json.dump(evaluation_metrics, f, indent=4)
    print(f"Saved evaluation metrics → {eval_path}")

    # -------------------------------------------------------
    # STEP 7 — Generate CSV outputs + visualizations
    # Saves CSVs → ml/  |  PNGs → visualizations/
    # -------------------------------------------------------
    generate_outputs(intern_summary, assignments_df, ml_dir, viz_dir)

    # -------------------------------------------------------
    # STEP 8 — Train Classification Model (at-risk prediction)
    # Reads CSVs from ml_dir, saves → models/classification_model.pkl
    # Appends metrics to model_evaluation.json
    # -------------------------------------------------------
    train_classification_model(ml_dir, models_dir)

    print("\n✅ Pipeline finished successfully!")
    print(f"   Models saved in  : {models_dir}")
    print(f"   CSV outputs in   : {ml_dir}")
    print(f"   Charts saved in  : {viz_dir}")


if __name__ == "__main__":
    run_pipeline()

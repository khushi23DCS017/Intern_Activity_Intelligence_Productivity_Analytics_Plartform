import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore') # ignore seaborn plotting warnings

def generate_outputs(intern_summary, assignments_df, ml_dir, viz_dir):
    print("--> Exporting csvs and charts for dashboard...")
    os.makedirs(ml_dir, exist_ok=True)
    os.makedirs(viz_dir, exist_ok=True)
    
    # 1. intern summary main file
    summary_cols = ['intern_id', 'hours_spent', 'assignments_completed', 'avg_score', 'tech_count', 'productivity_score']
    intern_summary[summary_cols].to_csv(os.path.join(ml_dir, "intern_summary.csv"), index=False)
    
    # 2. productivity preds
    intern_summary[['intern_id', 'predicted_productivity', 'productivity_score']].to_csv(os.path.join(ml_dir, "intern_productivity.csv"), index=False)
    
    # 3. clusters
    intern_summary[['intern_id', 'cluster', 'category']].to_csv(os.path.join(ml_dir, "intern_clusters.csv"), index=False)
    
    # 4. tech breakdown
    tech_df = assignments_df.groupby('technology').agg(
        avg_score=('average_assignment_score', 'mean'),
        total_completed=('assignments_completed', 'sum'),
        total_interns=('intern_id', 'nunique')
    ).reset_index()
    tech_df.to_csv(os.path.join(ml_dir, "technology_analysis.csv"), index=False)
    
    # 5. engagement
    engagement_cols = ['intern_id', 'number_of_activities', 'active_days', 'hours_spent']
    intern_summary[engagement_cols].to_csv(os.path.join(ml_dir, "engagement_scores.csv"), index=False)
    
    # 6. leaderboard
    top_interns = intern_summary.sort_values(by='productivity_score', ascending=False).head(10)
    top_interns[['intern_id', 'productivity_score', 'category']].to_csv(os.path.join(ml_dir, "top_interns.csv"), index=False)
    
    # PLOTS
    # prod distribution
    plt.figure(figsize=(10, 6))
    sns.histplot(intern_summary['productivity_score'], bins=20, kde=True, color='#3498db')
    plt.title("Productivity Score Dist")
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, "productivity_distribution.png"))
    plt.close()
    
    # tech skills
    plt.figure(figsize=(10, 6))
    sns.barplot(data=tech_df, x='technology', y='avg_score', hue='technology', palette='viridis', legend=False)
    plt.title("Tech Skills Comparison")
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, "technology_analysis.png"))
    plt.close()
    
    # clusters scatter
    plt.figure(figsize=(10, 6))
    palette_map = {'High Performer': '#2ecc71', 'Consistent Contributor': '#3498db', 'Learning Phase': '#f39c12'}
    sns.scatterplot(
        data=intern_summary, 
        x='hours_spent', 
        y='productivity_score', 
        hue='category', 
        palette=palette_map,
        s=100, alpha=0.8
    )
    plt.title("Clusters based on Hours & Score")
    plt.legend(title='')
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, "cluster_visualization.png"))
    plt.close()
    
    # top 10
    plt.figure(figsize=(12, 6))
    sns.barplot(data=top_interns, x='productivity_score', y='intern_id', hue='intern_id', palette='magma', legend=False)
    plt.title("Top 10 Leaderboard")
    plt.tight_layout()
    plt.savefig(os.path.join(viz_dir, "top_interns_leaderboard.png"))
    plt.close()
    
    print("Done exporting everything!")

# pyre-ignore-all-errors
import pandas as pd
import numpy as np

def preprocess_data(activity_df, assignments_df):
    print("--> Running preprocessing steps...")

    # intern_id comes from DB as intern_name — just strip whitespace
    activity_df['intern_id']    = activity_df['intern_id'].astype(str).str.strip()
    assignments_df['intern_id'] = assignments_df['intern_id'].astype(str).str.strip()

    # Drop any bad rows
    activity_df = activity_df[~activity_df['intern_id'].str.lower().eq('nan')]

    # Ensure date is datetime (Postgres gives date already, safety re-parse)
    activity_df['Date'] = pd.to_datetime(activity_df['Date'], errors='coerce')

    # Average knowledge + test score for overall assignment score
    # If both are 0 it means not attempted — keep as 0
    assignments_df['average_assignment_score'] = (
        assignments_df[['score_knowledge', 'score_test']]
        .replace(0, np.nan)
        .mean(axis=1)
        .fillna(0)
    )

    # assignments_completed already a number from DB
    assignments_df['assignments_completed'] = pd.to_numeric(
        assignments_df['assignments_completed'], errors='coerce'
    ).fillna(0)

    # Clean hours
    activity_df['Hours'] = pd.to_numeric(
        activity_df['Hours'], errors='coerce'
    ).fillna(0)

    print(f"  Activity rows    : {len(activity_df)}")
    print(f"  Assignment rows  : {len(assignments_df)}")

    return activity_df, assignments_df

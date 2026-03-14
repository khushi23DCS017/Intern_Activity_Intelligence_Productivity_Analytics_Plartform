# pyre-ignore-all-errors
import pandas as pd

def compute_metrics(activity_df, assignments_df):
    print("--> Engineering features...")

    # Engagement stats per intern
    engagement_df = activity_df.groupby('intern_id').agg(
        total_hours_logged   = ('Hours',    'sum'),
        number_of_activities = ('Activity', 'count'),
        active_days          = ('Date',     'nunique')
    ).reset_index()

    # Assignment stats per intern
    assignment_metrics_df = assignments_df.groupby('intern_id').agg(
        assignments_completed    = ('assignments_completed',    'sum'),
        average_assignment_score = ('average_assignment_score', 'mean'),
        technology_count         = ('technology',               'nunique')
    ).reset_index()

    # Merge (outer join — don't lose any intern)
    intern_summary = pd.merge(
        engagement_df, assignment_metrics_df,
        on='intern_id', how='outer'
    ).fillna(0)

    # Productivity score formula
    # productivity = 0.4*assignments_completed + 0.3*avg_score + 0.3*hours
    intern_summary['productivity_score'] = (
        0.4 * intern_summary['assignments_completed'] +
        0.3 * intern_summary['average_assignment_score'] +
        0.3 * intern_summary['total_hours_logged']
    )

    # Rename for clarity
    intern_summary = intern_summary.rename(columns={
        'total_hours_logged'     : 'hours_spent',
        'average_assignment_score': 'avg_score',
        'technology_count'       : 'tech_count'
    })

    print(f"  Interns in summary: {len(intern_summary)}")
    return intern_summary

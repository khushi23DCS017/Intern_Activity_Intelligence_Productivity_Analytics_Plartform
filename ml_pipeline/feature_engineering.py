import pandas as pd

def compute_metrics(activity_df, assignments_df):
    print("--> Engineering features...")
    
    # group by intern to get engagement stats
    engagement_df = activity_df.groupby('intern_id').agg(
        total_hours_logged=('Hours', 'sum'),
        number_of_activities=('Activity', 'count'),
        active_days=('Date', 'nunique') # count unique days
    ).reset_index()
    
    # assignment stats
    assignment_metrics_df = assignments_df.groupby('intern_id').agg(
        assignments_completed=('assignments_completed', 'sum'),
        average_assignment_score=('average_assignment_score', 'mean'),
        technology_count=('technology', 'nunique')
    ).reset_index()
    
    # merge them (outer join to not lose anyone)
    intern_summary = pd.merge(engagement_df, assignment_metrics_df, on='intern_id', how='outer').fillna(0)
    
    # formula from problem statement
    # productivity_score = 0.4*completed + 0.3*score + 0.3*hours
    intern_summary['productivity_score'] = (
        0.4 * intern_summary['assignments_completed'] +
        0.3 * intern_summary['average_assignment_score'] +
        0.3 * intern_summary['total_hours_logged']
    )
    
    # renaming columns so they are easier to use in dashboard
    intern_summary = intern_summary.rename(columns={
        'total_hours_logged': 'hours_spent',
        'average_assignment_score': 'avg_score',
        'technology_count': 'tech_count'
    })
    
    # print(intern_summary.head())
    return intern_summary

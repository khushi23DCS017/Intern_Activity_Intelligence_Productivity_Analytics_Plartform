# pyre-ignore-all-errors
import os
import sys
import pandas as pd
import psycopg2

# Import DB config from parent config.py
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DB_CONFIG

def get_connection():
    """Returns a psycopg2 connection using config.py settings."""
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        return psycopg2.connect(database_url)
    return psycopg2.connect(**DB_CONFIG)

def load_data(data_dir=None):
    """
    Loads activity and assignment data from PostgreSQL.
    data_dir param kept for backwards compatibility but not used.
    """
    print("--> Connecting to PostgreSQL and loading data...")

    conn = get_connection()

    # Pull activity logs
    activity_query = """
        SELECT
            di.intern_name   AS intern_id,
            da.activity_name AS "Activity",
            fa.activity_date AS "Date",
            fa.hours         AS "Hours"
        FROM fact_activity fa
        JOIN dim_intern   di ON fa.intern_id   = di.intern_id
        JOIN dim_activity da ON fa.activity_id = da.activity_id
    """
    activity_df = pd.read_sql(activity_query, conn)

    # Pull assignment progress with short tech labels
    assignment_query = """
        SELECT
            di.intern_name AS intern_id,
            CASE dc.course_name
                WHEN 'Basic Python Programming'             THEN 'Python'
                WHEN 'Basic SQL'                            THEN 'SQL'
                WHEN 'Data Processing using NumPy & Pandas' THEN 'NumPy'
                WHEN 'Data Processing using Pyspark'        THEN 'PySpark'
                ELSE dc.course_name
            END                                          AS technology,
            flp.completed_assignment_scored              AS assignments_completed,
            flp.completed_assignment_total               AS total_assignments,
            COALESCE(flp.knowledge_check_pct, 0)         AS score_knowledge,
            COALESCE(flp.overall_test_pct,    0)         AS score_test,
            flp.completion_status                        AS overall_status,
            flp.progress_percent
        FROM fact_learning_progress flp
        JOIN dim_intern di ON flp.intern_id = di.intern_id
        JOIN dim_course dc ON flp.course_id = dc.course_id
    """
    assignments_df = pd.read_sql(assignment_query, conn)

    conn.close()
    print(f"Loaded {len(activity_df)} activity rows "
          f"and {len(assignments_df)} assignment rows from DB.")

    return activity_df, assignments_df

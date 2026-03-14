import pandas as pd
from sqlalchemy import create_engine

# ---------------------------
# DATABASE CONNECTION
# ---------------------------

engine = create_engine(
    "postgresql://postgres:password@localhost:5432/intern_analytics"
)

# ---------------------------
# LOAD EOD DATA
# ---------------------------

eod = pd.read_csv("intern_activity_full_dataset.csv")

eod["Date"] = pd.to_datetime(eod["Date"])
eod["Hours"] = eod["Hours"].astype(float)

# ---------------------------
# LOAD LMS FILES
# ---------------------------

python_lms = pd.read_excel("assignment_submissions_progress_Basic Python Programming.xlsx")
sql_lms = pd.read_excel("assignment_submissions_progress_Basic SQL.xlsx")
numpy_lms = pd.read_excel("assignment_submissions_progress_Data Processing using NumPy  Pa.xlsx")
pyspark_lms = pd.read_excel("assignment_submissions_progress_Data Processing using Pyspark.xlsx")

lms = pd.concat([python_lms, sql_lms, numpy_lms, pyspark_lms])

# ---------------------------
# CLEAN LMS DATA
# ---------------------------

lms["Progress (%)"] = (
    lms["Progress (%)"]
    .astype(str)
    .str.replace("%","")
    .astype(float)
)

lms["Knowledge Check Score"] = lms["Knowledge Check Score"].astype(float)
lms["Test Score"] = lms["Test Score"].astype(float)

lms["Start Date"] = pd.to_datetime(lms["Start Date"])

# ---------------------------
# LOAD DIM_INTERN
# ---------------------------

interns = pd.DataFrame()

interns["intern_name"] = pd.concat([
    eod["User Name"],
    lms["User Name"]
]).drop_duplicates()

interns["mentor_name"] = None

interns.to_sql("dim_intern", engine, if_exists="append", index=False)

# ---------------------------
# LOAD DIM_COURSE
# ---------------------------

courses = pd.DataFrame()

courses["course_name"] = lms["Course Name"].drop_duplicates()

courses.to_sql("dim_course", engine, if_exists="append", index=False)

# ---------------------------
# LOAD DIM_ACTIVITY
# ---------------------------

activities = pd.DataFrame()

activities["activity_name"] = eod["Activity"].drop_duplicates()

activities.to_sql("dim_activity", engine, if_exists="append", index=False)

# ---------------------------
# LOAD DIM_DATE
# ---------------------------

dates = pd.DataFrame()

dates["date"] = pd.concat([
    eod["Date"],
    lms["Start Date"]
]).drop_duplicates()

dates["day"] = dates["date"].dt.day
dates["week"] = dates["date"].dt.isocalendar().week
dates["month"] = dates["date"].dt.month
dates["quarter"] = dates["date"].dt.quarter
dates["year"] = dates["date"].dt.year

dates.to_sql("dim_date", engine, if_exists="append", index=False)

# ---------------------------
# LOAD LOOKUP TABLES
# ---------------------------

intern_lookup = pd.read_sql("SELECT * FROM dim_intern", engine)
course_lookup = pd.read_sql("SELECT * FROM dim_course", engine)
date_lookup = pd.read_sql("SELECT * FROM dim_date", engine)

# ---------------------------
# LOAD FACT_LEARNING_PROGRESS
# ---------------------------

fact = lms.merge(
    intern_lookup,
    left_on="User Name",
    right_on="intern_name"
)

fact = fact.merge(
    course_lookup,
    left_on="Course Name",
    right_on="course_name"
)

fact = fact.merge(
    date_lookup,
    left_on="Start Date",
    right_on="date"
)

fact_final = fact[
    [
        "intern_id",
        "course_id",
        "date_id",
        "Progress (%)",
        "Knowledge Check Score",
        "Test Score",
        "Overall Status"
    ]
]

fact_final.columns = [
    "intern_id",
    "course_id",
    "date_id",
    "progress_percent",
    "knowledge_score",
    "test_score",
    "completion_status"
]

fact_final.to_sql(
    "fact_learning_progress",
    engine,
    if_exists="append",
    index=False
)

print("ETL pipeline executed successfully")

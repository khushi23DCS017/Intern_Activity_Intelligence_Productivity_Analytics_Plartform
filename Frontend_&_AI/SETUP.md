# Intern Analytics Platform – Setup Guide

## Prerequisites

- **Python 3.9+**
- **PostgreSQL** installed and running with database `intern_analytics`
- **Groq API key** (free at https://console.groq.com/keys)

---

## 1. Database Setup

Create the PostgreSQL database and tables. The app expects this star schema:

### Tables

- **dim_intern** – `intern_id`, `intern_name`, `mentor_name`
- **dim_mentor** – `mentor_id`, `mentor_name`
- **dim_course** – `course_id`, `course_name`
- **dim_activity** – `activity_id`, `activity_name`
- **dim_date** – `date_id`, `date`, `day`, `week`, `month`, `quarter`, `year`
- **fact_activity** – `activity_event_id`, `intern_id`, `activity_id`, `date_id`, `hours`
- **fact_learning_progress** – `progress_id`, `intern_id`, `course_id`, `mentor_id`, `date_id`, `progress_percent`, `knowledge_score`, `test_score`, `completion_status`

If your schema is different, update the SQL queries in `utils/data_loader.py`.

---

## 2. Environment Configuration

1. Copy `.env.example` to `.env` (or create `.env`):

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and set your connection string:

   ```env
   # Groq API Key
   GROQ_API_KEY=your_actual_groq_key

   # PostgreSQL - paste your connection string directly
   DATABASE_URL=postgresql://postgres:1234@localhost:5432/intern_analytics
   ```

   No need to set host, user, password separately—just use your full connection string.

---

## 3. Install Dependencies

```bash
cd C:\Intern_AI
pip install -r requirements.txt
```

---

## 4. Run the Application

```bash
streamlit run app.py
```

---

## 5. Login Credentials

Auth is still mock-based. Users in `utils/auth.py`:

| Username | Password | Role        | Display Name   |
|----------|----------|-------------|----------------|
| hr1      | password | HR_Manager  | Alice HR       |
| mgr1     | password | Team_Manager| Bob Manager    |
| mentor1  | password | Mentor      | Charlie Mentor |
| intern1  | password | Intern      | Intern_1       |
| intern2  | password | Intern      | Intern_2       |

**Important:** `user_display_name` must match values in the database:

- **Interns:** `Intern_1`, `Intern_2`, etc. should match `dim_intern.intern_name`
- **Mentors:** `Charlie Mentor` should match `dim_intern.mentor_name` for filtering

Update `utils/auth.py` (USERS) and your database so these names align.

---

## 6. Troubleshooting

| Issue | Action |
|-------|--------|
| `Database error: connection refused` | Check PostgreSQL is running and `DATABASE_URL` in `.env` is correct |
| `relation "dim_intern" does not exist` | Create the expected tables in your DB |
| `Insufficient data` or empty dashboards | Ensure `fact_activity` and `fact_learning_progress` have rows |
| Groq API errors | Confirm `GROQ_API_KEY` is valid in `.env` |

---

## 7. Optional: Schema Migration

To recreate the schema used by this app, run SQL similar to:

```sql
CREATE TABLE dim_mentor (mentor_id SERIAL PRIMARY KEY, mentor_name VARCHAR(100) UNIQUE NOT NULL);
CREATE TABLE dim_intern (intern_id SERIAL PRIMARY KEY, intern_name VARCHAR(100) UNIQUE NOT NULL, mentor_name VARCHAR(100));
CREATE TABLE dim_course (course_id SERIAL PRIMARY KEY, course_name VARCHAR(100) UNIQUE NOT NULL);
CREATE TABLE dim_activity (activity_id SERIAL PRIMARY KEY, activity_name VARCHAR(100) UNIQUE NOT NULL);
CREATE TABLE dim_date (date_id SERIAL PRIMARY KEY, date DATE UNIQUE NOT NULL, day INT, week INT, month INT, quarter INT, year INT);
CREATE TABLE fact_learning_progress (progress_id SERIAL PRIMARY KEY, intern_id INT REFERENCES dim_intern(intern_id), course_id INT REFERENCES dim_course(course_id), mentor_id INT REFERENCES dim_mentor(mentor_id), date_id INT REFERENCES dim_date(date_id), progress_percent DECIMAL(5,2), knowledge_score DECIMAL(5,2), test_score DECIMAL(5,2), completion_status VARCHAR(50));
CREATE TABLE fact_activity (activity_event_id SERIAL PRIMARY KEY, intern_id INT REFERENCES dim_intern(intern_id), activity_id INT REFERENCES dim_activity(activity_id), date_id INT REFERENCES dim_date(date_id), hours DECIMAL(4,2));
```

Then populate the tables with your data.

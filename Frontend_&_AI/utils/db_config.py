"""
PostgreSQL database configuration.
Use DATABASE_URL in .env for a single connection string - no separate setup needed.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

# Load .env from project root
load_dotenv(Path(__file__).resolve().parent.parent / ".env")


def get_db_uri():
    """
    Return SQLAlchemy-compatible PostgreSQL URI.
    Use DATABASE_URL for a direct connection string, e.g.:
      postgresql://user:password@host:port/database
    Or use individual DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT.
    """
    url = os.getenv("DATABASE_URL") or os.getenv("DB_CONNECTION_STRING")
    if url:
        # Ensure psycopg2 driver for SQLAlchemy
        if url.startswith("postgresql://") and "psycopg2" not in url:
            url = url.replace("postgresql://", "postgresql+psycopg2://", 1)
        return url

    # Fallback: build from individual vars
    return (
        f"postgresql+psycopg2://{os.getenv('DB_USER', 'postgres')}:{os.getenv('DB_PASSWORD', '')}"
        f"@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}/{os.getenv('DB_NAME', 'intern_analytics')}"
    )

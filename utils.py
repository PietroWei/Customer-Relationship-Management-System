# util.py
import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables from .env file
def load_environment_variables():
    load_dotenv()

# Database connection function
def get_db_connection():
    load_environment_variables()  # Ensure .env is loaded
    conn = psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT")
    )
    return conn
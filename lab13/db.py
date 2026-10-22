
import streamlit as st
import psycopg2
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager

@contextmanager
def get_connection():
    conn = None
    try:
        if "url" in st.secrets.get("postgres", {}):
            conn = psycopg2.connect(
                st.secrets["postgres"]["url"],
                cursor_factory=RealDictCursor
            )
        else:
            conn = psycopg2.connect(
                host=st.secrets["postgres"]["host"],
                port=st.secrets["postgres"]["port"],
                database=st.secrets["postgres"]["database"],
                user=st.secrets["postgres"]["user"],
                password=st.secrets["postgres"]["password"],
                cursor_factory=RealDictCursor
            )

        yield conn
        conn.commit()

    finally:
        if conn is not None:
            conn.close()

def init_db():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)

            cur.execute("""
                ALTER TABLE users
                ADD COLUMN IF NOT EXISTS role VARCHAR(20)
                DEFAULT 'user';
            """)

def create_user(username, email, password_hash):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """INSERT INTO users
                    (username, email, password_hash)
                    VALUES (%s, %s, %s)""",
                    (username, email, password_hash)
                )
        return True

    except psycopg2.errors.UniqueViolation:
        return False

def get_user_by_username(username):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM users WHERE username = %s",
                (username,)
            )
            return cur.fetchone()

def get_all_users():
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """SELECT id, username, email, created_at
                FROM users ORDER BY id"""
            )
            return cur.fetchall()

def user_exists(username=None, email=None):
    with get_connection() as conn:
        with conn.cursor() as cur:
            if username:
                cur.execute(
                    "SELECT 1 FROM users WHERE username = %s",
                    (username,)
                )
            elif email:
                cur.execute(
                    "SELECT 1 FROM users WHERE email = %s",
                    (email,)
                )
            else:
                return False

            return cur.fetchone() is not None

def update_password(username, new_hash):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "UPDATE users SET password_hash = %s WHERE username = %s",
                (new_hash, username)
            )

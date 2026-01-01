import psycopg2
from db import get_connection
import hashlib

# ------------------ PASSWORD HASHING ------------------
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


# ------------------ CREATE USERS TABLE ------------------
def create_users_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    conn.commit()
    cur.close()
    conn.close()


# ------------------ SIGNUP FUNCTION ------------------
def signup(username, password):
    create_users_table()  # 🔥 FIX: ensures table exists

    conn = get_connection()
    cur = conn.cursor()

    hashed_password = hash_password(password)

    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, hashed_password)
        )
        conn.commit()
        return True

    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        return False

    finally:
        cur.close()
        conn.close()


# ------------------ LOGIN FUNCTION ------------------
def login(username, password):
    create_users_table()  # safety

    conn = get_connection()
    cur = conn.cursor()

    hashed_password = hash_password(password)

    cur.execute(
        "SELECT id FROM users WHERE username=%s AND password=%s",
        (username, hashed_password)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        return user[0]  # return user_id
    else:
        return None





















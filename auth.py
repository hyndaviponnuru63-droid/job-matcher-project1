import psycopg2
import hashlib
from db import get_connection


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def create_users_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


def signup(username, password):
    create_users_table()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username.strip(), hash_password(password))
        )
        conn.commit()
        return True

    except psycopg2.IntegrityError:
        conn.rollback()
        return False

    finally:
        cur.close()
        conn.close()


def login(username, password):
    create_users_table()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "SELECT id FROM users WHERE username=%s AND password=%s",
        (username.strip(), hash_password(password))
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        return user[0]
    return None

























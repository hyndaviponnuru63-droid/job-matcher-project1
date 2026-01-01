import psycopg2
from db import get_connection
import hashlib


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

    hashed_password = hash_password(password)

    try:
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username.strip(), hashed_password)
        )
        conn.commit()
        print("✅ Signup successful")
        return True

    except psycopg2.IntegrityError as e:
        conn.rollback()
        print("❌ Integrity Error:", e)
        return False

    except Exception as e:
        conn.rollback()
        print("❌ Signup Exception:", e)
        return False

    finally:
        cur.close()
        conn.close()


def login(username, password):
    create_users_table()

    conn = get_connection()
    cur = conn.cursor()

    hashed_password = hash_password(password)

    cur.execute(
        "SELECT id FROM users WHERE username=%s AND password=%s",
        (username.strip(), hashed_password)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        return user[0]
    return None























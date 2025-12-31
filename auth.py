# auth.py
from db import get_connection

def signup(username, password):
    if not username or not password:
        return False
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print("Signup error:", e)
        return False

def login(username, password):
    if not username or not password:
        return None
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT id, username FROM users WHERE username=%s AND password=%s",
            (username, password)
        )
        user = cur.fetchone()
        cur.close()
        conn.close()
        return user
    except Exception as e:
        print("Login error:", e)
        return None















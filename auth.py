import hashlib
from db import get_connection

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def signup(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, hash_password(password))
    )
    conn.commit()
    conn.close()

def login(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM users WHERE username=%s AND password=%s",
        (username, hash_password(password))
    )
    user = cur.fetchone()
    conn.close()
    return user

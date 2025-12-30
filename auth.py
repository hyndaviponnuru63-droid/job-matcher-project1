from db import get_connection

def signup(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users (username, password) VALUES (%s, %s)",
        (username, password)
    )
    conn.commit()
    conn.close()

def login(username, password):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT id FROM users WHERE username=%s AND password=%s",
        (username, password)
    )
    user = cur.fetchone()
    conn.close()
    return user





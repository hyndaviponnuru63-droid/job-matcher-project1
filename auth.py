from db import get_connection

def login(username, password):
    """
    Checks if username and password exist in the database.
    Returns user row if valid, else None.
    """
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













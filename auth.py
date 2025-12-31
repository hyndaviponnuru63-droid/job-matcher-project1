from db import get_connection

def signup(username, password):
    """
    Registers a new user in the database safely.
    Returns True if successful, False otherwise.
    """
    if not username or not password:
        print("Signup error: Username or password is empty")
        return False

    try:
        conn = get_connection()
        cur = conn.cursor()
        # Use parameterized query to avoid SQL injection
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











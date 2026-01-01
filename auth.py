# auth.py
import streamlit as st
from db import get_connection

def signup(username, password):
    if not username or not password:
        st.error("Username and password cannot be empty")
        return False

    try:
        conn = get_connection()
        cur = conn.cursor()

        # check if username already exists
        cur.execute(
            "SELECT id FROM users WHERE username = %s",
            (username,)
        )
        if cur.fetchone():
            st.error("Username already exists")
            cur.close()
            conn.close()
            return False

        # insert new user
        cur.execute(
            "INSERT INTO users (username, password) VALUES (%s, %s)",
            (username, password)
        )
        conn.commit()

        cur.close()
        conn.close()
        return True

    except Exception as e:
        st.error(f"Signup error: {e}")   # THIS shows real error
        return False


def login(username, password):
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
        st.error(f"Login error: {e}")
        return None



















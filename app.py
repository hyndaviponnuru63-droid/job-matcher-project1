import streamlit as st
from auth import signup, login
from db import get_connection
from saved_jobs import init_db, save_job, remove_job, get_saved_jobs

# ---------- INIT DB ----------
init_db()

# ---------- SEARCH JOBS ----------
search = st.text_input("Search jobs (format: job_title, company, skills)", key="search_box")
conn = get_connection()
cur = conn.cursor()

if search:
    # Split input by commas
    parts = [p.strip() for p in search.split(",")]
    
    # Assign each part to its column or empty string
    job_title = parts[0] if len(parts) > 0 else ""
    company   = parts[1] if len(parts) > 1 else ""
    skills    = parts[2] if len(parts) > 2 else ""

    # SQL query with ILIKE (case-insensitive) and optional filters
    cur.execute("""
        SELECT id, job_title, company, skills
        FROM jobs
        WHERE job_title ILIKE %s
          AND company ILIKE %s
          AND skills ILIKE %s
    """, (f"%{job_title}%", f"%{company}%", f"%{skills}%"))
else:
    # If nothing typed, show all jobs
    cur.execute("SELECT id, job_title, company, skills FROM jobs")

jobs = cur.fetchall()
cur.close()
conn.close()



# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None

st.title("Job Matcher Project")

# ---------- LOGOUT ----------
if st.session_state.logged_in:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.success("Logged out successfully")

# ---------- SIGNUP ----------
if not st.session_state.logged_in:
    st.subheader("Sign Up")
    new_username = st.text_input("Username", key="signup_user")
    new_password = st.text_input("Password", type="password", key="signup_pass")
    if st.button("Sign Up"):
        if signup(new_username, new_password):
            st.success("Signup successful! Please login.")
        else:
            st.error("Username already exists")

# ---------- LOGIN ----------
if not st.session_state.logged_in:
    st.subheader("Login")
    username = st.text_input("Login Username", key="login_user")
    password = st.text_input("Login Password", type="password", key="login_pass")
    if st.button("Login"):
        user_id = login(username, password)
        if user_id:
            st.session_state.logged_in = True
            st.session_state.user_id = user_id
            st.session_state.username = username
            st.success(f"Login successful! Welcome {username}")
        else:
            st.error("Invalid credentials")

# ---------- JOB LIST & SEARCH ----------
if st.session_state.logged_in:
    st.subheader("Available Jobs")

    search = st.text_input("Search jobs by title, company, or skills", key="search_box")

    conn = get_connection()
    cur = conn.cursor()

    if search:
        cur.execute("""
            SELECT id, job_title, company, skills
            FROM jobs
            WHERE job_title ILIKE %s
               OR company ILIKE %s
               OR skills ILIKE %s
        """, (f"%{search}%", f"%{search}%", f"%{search}%"))
    else:
        cur.execute("SELECT id, job_title, company, skills FROM jobs")

    jobs = cur.fetchall()
    cur.close()
    conn.close()

    if jobs:
        for job in jobs:
            st.write(f"**{job[1]}** at {job[2]}")
            st.write(f"Skills: {job[3]}")
            if st.button(f"Save Job {job[0]}", key=f"save_{job[0]}"):
                save_job(st.session_state.user_id, job[0])
                st.success("Job saved")
    else:
        st.info("No jobs available")

    # ---------- SAVED JOBS ----------
    st.subheader("Saved Jobs")
    saved = get_saved_jobs(st.session_state.user_id)
    if saved:
        for job in saved:
            st.write(f"{job[1]} - {job[2]} | Skills: {job[3]}")
            if st.button(f"Remove {job[0]}", key=f"remove_{job[0]}"):
                remove_job(st.session_state.user_id, job[0])
                st.success("Removed")
    else:
        st.info("You haven't saved any jobs yet.")







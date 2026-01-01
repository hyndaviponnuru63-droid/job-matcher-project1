import streamlit as st
from auth import signup, login
from db import get_connection
from saved_jobs import save_job, remove_job, get_saved_jobs, create_tables


# ---------- INITIAL SETUP ----------
create_tables()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user_id" not in st.session_state:
    st.session_state.user_id = None


st.title("Job Matcher Project")

# ---------- SIGNUP ----------
st.subheader("Sign Up")
new_username = st.text_input("Username")
new_password = st.text_input("Password", type="password")

if st.button("Sign Up"):
    if signup(new_username, new_password):
        st.success("Signup successful. Please login.")
    else:
        st.error("Username already exists")


# ---------- LOGIN ----------
st.subheader("Login")
username = st.text_input("Login Username")
password = st.text_input("Login Password", type="password")

if st.button("Login"):
    user_id = login(username, password)
    if user_id:
        st.session_state.logged_in = True
        st.session_state.user_id = user_id
        st.success("Login successful")
    else:
        st.error("Invalid credentials")


# ---------- JOB LIST ----------
if st.session_state.logged_in:
    st.subheader("Available Jobs")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, job_title, company, skills FROM jobs")
    jobs = cur.fetchall()
    cur.close()
    conn.close()

    if jobs:
        for job in jobs:
            st.write(f"**{job[1]}** at {job[2]}")
            st.write(f"Skills: {job[3]}")

            if st.button(f"Save Job {job[0]}"):
                save_job(st.session_state.user_id, job[0])
                st.success("Job saved")
    else:
        st.info("No jobs available")


    # ---------- SAVED JOBS ----------
    st.subheader("Saved Jobs")
    saved = get_saved_jobs(st.session_state.user_id)

    if saved:
        for job in saved:
            st.write(f"{job[1]} - {job[2]}")
            if st.button(f"Remove {job[0]}"):
                remove_job(st.session_state.user_id, job[0])
                st.success("Removed")
    else:
        st.info("You haven't saved any jobs yet.")

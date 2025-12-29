import streamlit as st
from auth import login, signup
from db import get_connection
from saved_jobs import save_job, remove_job

# ------------------ Initialize session state ------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None

st.title("Job Matcher Project")

# ================= SIGNUP =================
st.subheader("Sign Up")
new_username = st.text_input("New Username", key="signup_username")
new_password = st.text_input("New Password", type="password", key="signup_password")

if st.button("Sign Up"):
    if new_username.strip() != "" and new_password.strip() != "":
        signup(new_username, new_password)
        st.success("User created! You can now log in.")
    else:
        st.error("Please enter username and password.")

# ================= LOGIN =================
st.subheader("Login")
username = st.text_input("Username", key="login_username")
password = st.text_input("Password", type="password", key="login_password")

if st.button("Login"):
    user = login(username, password)
    if user:
        st.session_state.logged_in = True
        st.session_state.user_id = user[0]
        st.success("Login successful")
    else:
        st.error("Invalid credentials")

# ================= LOGOUT =================
if st.session_state.logged_in:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.success("Logged out successfully")

# ================= SEARCH / FILTER =================
search_skill = st.text_input("Search jobs by skill:")

# ================= SHOW JOBS + SAVE =================
if st.session_state.logged_in:
    st.subheader("Available Jobs")

    conn = get_connection()
    cur = conn.cursor()
    
    if search_skill.strip() == "":
        cur.execute("""
            SELECT id, job_title, skills, company, 
                   COALESCE(description,'') AS description, 
                   COALESCE(location,'') AS location, 
                   COALESCE(salary,'') AS salary
            FROM jobs
        """)
    else:
        cur.execute("""
            SELECT id, job_title, skills, company, 
                   COALESCE(description,'') AS description, 
                   COALESCE(location,'') AS location, 
                   COALESCE(salary,'') AS salary
            FROM jobs
            WHERE skills ILIKE %s
        """, (f"%{search_skill}%",))
    
    jobs = cur.fetchall()
    conn.close()

    if len(jobs) == 0:
        st.info("No jobs available in database.")
    else:
        for idx, job in enumerate(jobs):
            job_id, job_title, skills, company, description, location, salary = job
            st.write(f"**{job_title}** - {skills} - {company}")
            st.write(f"Description: {description}")
            st.write(f"Location: {location} | Salary: {salary}")
            if st.button("Save Job", key=f"save_{job_id}_{idx}"):
                save_job(st.session_state.user_id, job_id)
                st.success(f"Job '{job_title}' saved!")

    # ------------------ Show saved jobs ------------------
    st.subheader("Saved Jobs")

    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT j.id, j.job_title, j.company, j.skills
        FROM saved_jobs sj
        JOIN jobs j ON sj.job_id = j.id
        WHERE sj.user_id = %s
    """, (st.session_state.user_id,))
    saved_jobs = cur.fetchall()
    conn.close()

    if len(saved_jobs) == 0:
        st.info("You haven't saved any jobs yet.")
    else:
        for idx, job in enumerate(saved_jobs):
            job_id, job_title, company, skills = job
            st.write(f"**{job_title}** - {skills} - {company}")
            if st.button("Remove Saved Job", key=f"remove_{job_id}_{idx}"):
                remove_job(st.session_state.user_id, job_id)
                st.success(f"Job '{job_title}' removed!")

    st.info(f"Logged in as User ID: {st.session_state.user_id}")


        




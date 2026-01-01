import streamlit as st #old
from auth import signup, login
from db import get_connection
from saved_jobs import init_db, save_job, remove_job, get_saved_jobs
import pdfplumber

# ---------- INIT DB ----------
init_db()

# ---------- SESSION STATE ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "username" not in st.session_state:
    st.session_state.username = None
if "user_skills" not in st.session_state:
    st.session_state.user_skills = []

st.title("Job Matcher Project")

# ---------- LOGOUT ----------
if st.session_state.logged_in:
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.user_id = None
        st.session_state.username = None
        st.session_state.user_skills = []
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

# ---------- LOGGED-IN FEATURES ----------
if st.session_state.logged_in:

    st.subheader(f"Welcome, {st.session_state.username}!")

    # ---------- SKILLS INPUT ----------
    st.subheader("Your Skills")
    skills_input = st.text_input("Enter your skills (comma-separated)", key="user_skills_input")
    if st.button("Save Skills"):
        st.session_state.user_skills = [s.strip().lower() for s in skills_input.split(",")]
        st.success(f"Skills saved: {', '.join(st.session_state.user_skills)}")

    # ---------- RESUME UPLOAD ----------
    st.subheader("Upload Resume (Optional)")
    uploaded_file = st.file_uploader("Upload your resume (PDF)", type=["pdf"])
    if uploaded_file:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + " "
        st.text_area("Resume Text Extracted", text, height=150)

        # Simple skill extraction
        all_skills = ["python", "java", "sql", "html", "css", "javascript",
                      "react", "django", "flask", "c++"]
        extracted_skills = [skill for skill in all_skills if skill.lower() in text.lower()]
        if extracted_skills:
            st.session_state.user_skills = extracted_skills
            st.success(f"Skills extracted from resume: {', '.join(extracted_skills)}")

    # ---------- AVAILABLE JOBS & SEARCH ----------
    st.subheader("Available Jobs")
    search = st.text_input("Search jobs (format: job_title, company, skills)", key="search_box")

    conn = get_connection()
    cur = conn.cursor()

    if search:
        # Split input by commas
        parts = [p.strip() for p in search.split(",")]
        job_title = parts[0] if len(parts) > 0 else ""
        company   = parts[1] if len(parts) > 1 else ""
        skills    = parts[2] if len(parts) > 2 else ""
        cur.execute("""
            SELECT id, job_title, company, skills
            FROM jobs
            WHERE job_title ILIKE %s
              AND company ILIKE %s
              AND skills ILIKE %s
        """, (f"%{job_title}%", f"%{company}%", f"%{skills}%"))
    else:
        cur.execute("SELECT id, job_title, company, skills FROM jobs")

    jobs = cur.fetchall()
    cur.close()
    conn.close()

    # ---------- JOB FIT CALCULATION ----------
    def calculate_job_fit(job_skills, user_skills):
        job_set = set([s.strip().lower() for s in job_skills.split(",")])
        user_set = set(user_skills)
        if not user_set:
            return 0
        fit = len(job_set & user_set) / len(job_set) * 100
        return int(fit)

    # Sort jobs by Job Fit descending
    jobs.sort(key=lambda j: calculate_job_fit(j[3], st.session_state.user_skills), reverse=True)

    # Display jobs
    if jobs:
        for job in jobs:
            fit_percentage = calculate_job_fit(job[3], st.session_state.user_skills)
            st.write(f"**{job[1]}** at {job[2]}")
            st.write(f"Skills: {job[3]}")
            st.write(f"**Job Fit: {fit_percentage}%**")
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




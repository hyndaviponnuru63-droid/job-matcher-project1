from db import get_connection

# ------------------ CREATE TABLES ------------------
def create_job_tables():
    conn = get_connection()
    cur = conn.cursor()

    # Jobs table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id SERIAL PRIMARY KEY,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            location TEXT,
            description TEXT
        );
    """)

    # Saved jobs table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS saved_jobs (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
            job_id INTEGER REFERENCES jobs(id) ON DELETE CASCADE,
            UNIQUE(user_id, job_id)
        );
    """)

    conn.commit()
    cur.close()
    conn.close()


# ------------------ SAVE JOB ------------------
def save_job(user_id, job_id):
    create_job_tables()

    conn = get_connection()
    cur = conn.cursor()

    try:
        cur.execute(
            "INSERT INTO saved_jobs (user_id, job_id) VALUES (%s, %s)",
            (user_id, job_id)
        )
        conn.commit()
    except:
        conn.rollback()
    finally:
        cur.close()
        conn.close()


# ------------------ REMOVE JOB ------------------
def remove_job(user_id, job_id):
    create_job_tables()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM saved_jobs WHERE user_id=%s AND job_id=%s",
        (user_id, job_id)
    )

    conn.commit()
    cur.close()
    conn.close()


# ------------------ GET SAVED JOBS ------------------
def get_saved_jobs(user_id):
    create_job_tables()

    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT j.id, j.title, j.company, j.location
        FROM saved_jobs sj
        JOIN jobs j ON sj.job_id = j.id
        WHERE sj.user_id = %s
    """, (user_id,))

    jobs = cur.fetchall()

    cur.close()
    conn.close()
    return jobs






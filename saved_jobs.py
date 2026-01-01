from db import get_connection


def init_db():
    conn = get_connection()
    cur = conn.cursor()

    # USERS table (needed for foreign key)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)

    # JOBS table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS jobs (
            id SERIAL PRIMARY KEY,
            job_title TEXT NOT NULL,
            company TEXT NOT NULL,
            skills TEXT
        );
    """)

    # SAVED JOBS table
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


def save_job(user_id, job_id):
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


def remove_job(user_id, job_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM saved_jobs WHERE user_id=%s AND job_id=%s",
        (user_id, job_id)
    )

    conn.commit()
    cur.close()
    conn.close()


def get_saved_jobs(user_id):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT j.id, j.job_title, j.company, j.skills
        FROM saved_jobs sj
        JOIN jobs j ON sj.job_id = j.id
        WHERE sj.user_id = %s
    """, (user_id,))

    jobs = cur.fetchall()
    cur.close()
    conn.close()
    return jobs










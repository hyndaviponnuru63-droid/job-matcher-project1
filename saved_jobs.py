from db import get_connection

def save_job(user_id, job_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO saved_jobs (user_id, job_id) VALUES (%s, %s)", (user_id, job_id))
    conn.commit()
    conn.close()

def remove_job(user_id, job_id):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM saved_jobs WHERE user_id=%s AND job_id=%s", (user_id, job_id))
    conn.commit()
    conn.close()




from db import get_connection

def save_job(user_id, job_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "INSERT INTO saved_jobs (user_id, job_id) VALUES (%s, %s) ON CONFLICT DO NOTHING",
            (user_id, job_id)
        )
        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()

def remove_job(user_id, job_id):
    conn = get_connection()
    cur = conn.cursor()
    try:
        cur.execute(
            "DELETE FROM saved_jobs WHERE user_id=%s AND job_id=%s",
            (user_id, job_id)
        )
        conn.commit()
    except:
        conn.rollback()
    finally:
        conn.close()


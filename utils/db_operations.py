import psycopg2
from config import DB_CONFIG
from utils.common import generate_uuid

def get_db_connection():
    conn = psycopg2.connect(**DB_CONFIG)
    return conn

def update_percentage(id_proses, percentage):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE jobs SET progress = %s WHERE id = %s", (percentage, id_proses))
    conn.commit()
    cur.close()
    conn.close()

def update_status(id_proses, status):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("UPDATE jobs SET status = %s WHERE id = %s", (status, id_proses))
    conn.commit()
    cur.close()
    conn.close()

def insert_result(id_proses, workspace, layer):
    result_id = generate_uuid()  
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO results (id, jobid, workspace, layer) VALUES (%s, %s, %s, %s)", (result_id, id_proses, workspace, layer))
    conn.commit()
    cur.close()
    conn.close()

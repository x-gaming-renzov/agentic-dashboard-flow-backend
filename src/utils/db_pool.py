# src/utils/pgpool.py

import os
import dotenv
from psycopg2 import pool

dotenv.load_dotenv()

connection_pool = None

def init_pg_pool(minconn=1, maxconn=5):
    """
    Initialize the PostgreSQL connection pool once at startup.
    """
    global connection_pool
    if connection_pool is None:
        connection_pool = pool.SimpleConnectionPool(
            minconn,
            maxconn,
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            database=os.getenv("DB_NAME"),
            # Optionally set more parameters here
        )
        print("[pgpool] Connection pool created")
    else:
        print("[pgpool] Connection pool already initialized")

def get_connection():
    """
    Retrieve a connection from the pool.
    """
    global connection_pool
    if connection_pool is None:
        # In case someone calls this before init_pg_pool() is invoked
        init_pg_pool()

    return connection_pool.getconn()

def put_connection(conn):
    """
    Return a connection to the pool.
    """
    global connection_pool
    if connection_pool:
        connection_pool.putconn(conn)

def close_pg_pool():
    """
    Close all connections in the pool (e.g. on shutdown).
    """
    global connection_pool
    if connection_pool:
        connection_pool.closeall()
        connection_pool = None
        print("[pgpool] Connection pool closed")

def execute_sql_query(query: str):
    conn = get_connection()    # Now from the pool
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        data = cursor.fetchall()
        conn.commit()
        return data
    finally:
        cursor.close()
        # Important: release the connection back to the pool!
        put_connection(conn)

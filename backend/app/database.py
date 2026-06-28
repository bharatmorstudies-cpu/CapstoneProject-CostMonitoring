import os
import pg8000.dbapi
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

def get_db_connection():
    """Establishes a connection link via the pure-Python pg8000 driver."""
    # Parse the standard database connection string into parts required by pg8000
    url = urlparse(DATABASE_URL)
    username = url.username
    password = url.password
    database = url.path.lstrip('/')
    hostname = url.hostname
    port = url.port or 5432

    conn = pg8000.dbapi.connect(
        user=username,
        password=password,
        host=hostname,
        database=database,
        port=port
    )
    return conn

def init_db():
    """Creates the structural tables required to host resource cost points."""
    command = """
    CREATE TABLE IF NOT EXISTS cloud_costs (
        id SERIAL PRIMARY KEY,
        provider VARCHAR(50) NOT NULL,
        date DATE NOT NULL,
        resource_type VARCHAR(100) NOT NULL,
        cost NUMERIC(12, 2) NOT NULL,
        environment VARCHAR(50) NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        CONSTRAINT unique_provider_date_resource UNIQUE (provider, date, resource_type, environment)
    )
    """
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        conn.commit()
        print("Database initialization successful: Tables verified via pure-Python driver.")
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
    finally:
        if conn is not None:
            conn.close()

def save_cost_records(records):
    """Inserts standardized billing records using an upsert methodology to avoid duplication."""
    # Note: pg8000 uses standard '%s' or param style mapping parameters
    query = """
        INSERT INTO cloud_costs (provider, date, resource_type, cost, environment)
        VALUES (%s, %s, %s, %s, %s)
        ON CONFLICT (provider, date, resource_type, environment)
        DO UPDATE SET cost = EXCLUDED.cost;
    """
    conn = None
    inserted_count = 0
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        for record in records:
            cur.execute(query, (
                record['provider'],
                str(record['date']), # Standardize date objects to string for insertion safety
                record['resource_type'],
                float(record['cost']),
                record['environment']
            ))
            inserted_count += 1
        conn.commit()
        cur.close()
        print(f"Aggregation pipeline complete: Saved/Updated {inserted_count} records.")
    except Exception as e:
        print(f"Error storing database logs: {str(e)}")
    finally:
        if conn is not None:
            conn.close()

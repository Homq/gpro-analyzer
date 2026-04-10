import os
import psycopg2
from psycopg2.extras import RealDictCursor

# Railway automatically provides this environment variable
# Locally we fall back to SQLite behaviour by checking if it exists
DATABASE_URL = os.environ.get("DATABASE_URL")

def get_connection():
    """Creates and returns a connection to the PostgreSQL database"""
    return psycopg2.connect(DATABASE_URL)

def create_tables():
    """Creates the tables if they don't exist yet"""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS race_setups (
            id SERIAL PRIMARY KEY,
            season INTEGER,
            race INTEGER,
            track_name TEXT,
            track_power INTEGER,
            track_accel INTEGER,
            track_handl INTEGER,
            laps INTEGER,
            set_fwing INTEGER,
            set_rwing INTEGER,
            set_engine INTEGER,
            set_brakes INTEGER,
            set_gear INTEGER,
            set_susp INTEGER,
            start_fuel INTEGER,
            fuel_stop1 INTEGER,
            fuel_stop2 INTEGER,
            fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS race_weather (
            id SERIAL PRIMARY KEY,
            season INTEGER,
            race INTEGER,
            track_name TEXT,
            quarter INTEGER,
            temp_low INTEGER,
            temp_high INTEGER,
            hum_low INTEGER,
            hum_high INTEGER,
            rain_pct_low INTEGER,
            rain_pct_high INTEGER
        )
    """)

    conn.commit()
    cursor.close()
    conn.close()
    print("Database tables created successfully!")

def save_race_setup(data):
    """Saves a race setup into the database"""
    conn = get_connection()
    cursor = conn.cursor()

    season = data.get("season")
    race = data.get("race")

    # Check if we already have this race saved
    cursor.execute("""
        SELECT id FROM race_setups WHERE season = %s AND race = %s
    """, (season, race))

    existing = cursor.fetchone()

    if existing:
        print(f"Race {race} of season {season} already in database, skipping.")
    else:
        cursor.execute("""
            INSERT INTO race_setups (
                season, race, track_name, track_power, track_accel, track_handl,
                laps, set_fwing, set_rwing, set_engine, set_brakes, set_gear,
                set_susp, start_fuel, fuel_stop1, fuel_stop2
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            season, race,
            data.get("trackName"),
            data.get("trackPower"),
            data.get("trackAccel"),
            data.get("trackHandl"),
            data.get("laps"),
            data.get("setFWing"),
            data.get("setRWing"),
            data.get("setEngine"),
            data.get("setBrakes"),
            data.get("setGear"),
            data.get("setSusp"),
            data.get("startFuel"),
            data.get("fuelStop1"),
            data.get("fuelStop2")
        ))
        print(f"Saved race {race} season {season} to database!")

    conn.commit()
    cursor.close()
    conn.close()
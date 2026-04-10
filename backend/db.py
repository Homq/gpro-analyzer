import sqlite3
import os

# Path to our database file
# Works both locally and on Railway
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "gpro.db")


def get_connection():
    """Creates and returns a connection to the database.
    Think of this like opening a door to the database room."""
    return sqlite3.connect(DB_PATH)


def create_tables():
    """Creates the tables in our database if they don't exist yet.
    A table is like a spreadsheet - it has columns and rows."""

    conn = get_connection()
    cursor = conn.cursor()
    # A cursor is like a pen - we use it to write and read from the database

    # Table 1: Store race setup data for every race
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS race_setups
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       season
                       INTEGER,
                       race
                       INTEGER,
                       track_name
                       TEXT,
                       track_power
                       INTEGER,
                       track_accel
                       INTEGER,
                       track_handl
                       INTEGER,
                       laps
                       INTEGER,
                       set_fwing
                       INTEGER,
                       set_rwing
                       INTEGER,
                       set_engine
                       INTEGER,
                       set_brakes
                       INTEGER,
                       set_gear
                       INTEGER,
                       set_susp
                       INTEGER,
                       start_fuel
                       INTEGER,
                       fuel_stop1
                       INTEGER,
                       fuel_stop2
                       INTEGER,
                       fetched_at
                       TIMESTAMP
                       DEFAULT
                       CURRENT_TIMESTAMP
                   )
                   """)

    # Table 2: Store weather forecasts per race
    cursor.execute("""
                   CREATE TABLE IF NOT EXISTS race_weather
                   (
                       id
                       INTEGER
                       PRIMARY
                       KEY
                       AUTOINCREMENT,
                       season
                       INTEGER,
                       race
                       INTEGER,
                       track_name
                       TEXT,
                       quarter
                       INTEGER,
                       temp_low
                       INTEGER,
                       temp_high
                       INTEGER,
                       hum_low
                       INTEGER,
                       hum_high
                       INTEGER,
                       rain_pct_low
                       INTEGER,
                       rain_pct_high
                       INTEGER
                   )
                   """)

    # Save changes and close the connection
    conn.commit()
    conn.close()
    print("Database tables created successfully!")


def save_race_setup(data):
    """Saves a race setup into the database.
    First checks if we already saved this race to avoid duplicates."""

    conn = get_connection()
    cursor = conn.cursor()

    season = int(data.get("season") or 0)
    race = int(data.get("race") or 0)

    # Check if we already have this race saved
    cursor.execute("""
                   SELECT id
                   FROM race_setups
                   WHERE season = ?
                     AND race = ?
                   """, (season, race))

    existing = cursor.fetchone()

    if existing:
        print(f"Race {race} of season {season} already in database, skipping.")
    else:
        cursor.execute("""
                       INSERT INTO race_setups (season, race, track_name, track_power, track_accel, track_handl,
                                                laps, set_fwing, set_rwing, set_engine, set_brakes, set_gear,
                                                set_susp, start_fuel, fuel_stop1, fuel_stop2)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
    conn.close()


if __name__ == "__main__":
    create_tables()
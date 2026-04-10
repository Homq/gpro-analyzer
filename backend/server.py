from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

app = Flask(__name__)
CORS(app)  # This allows the dashboard to talk to this server

# Works both locally and on Railway
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "gpro.db")

def get_connection():
    """Opens a connection to the database"""
    conn = sqlite3.connect(DB_PATH)
    # This makes rows behave like dictionaries
    # so we get {"track_name": "Sakhir"} instead of just ("Sakhir",)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/api/setups")
def get_setups():
    """Returns all race setups as JSON.
    When the dashboard visits /api/setups, this function runs."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM race_setups ORDER BY season, race")
    rows = cursor.fetchall()
    conn.close()
    # Convert rows to a list of dictionaries
    return jsonify([dict(row) for row in rows])

@app.route("/api/setups/latest")
def get_latest_setup():
    """Returns only the most recent race setup"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM race_setups 
        ORDER BY season DESC, race DESC 
        LIMIT 1
    """)
    row = cursor.fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    else:
        return jsonify({"error": "No data found"}), 404

@app.route("/api/tracks")
def get_tracks():
    """Returns a summary of all tracks we have data for"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT track_name, track_power, track_accel, track_handl
        FROM race_setups
        ORDER BY track_name
    """)
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

if __name__ == "__main__":
    # debug=True means the server restarts automatically when you change code
    app.run(debug=True, port=5000)
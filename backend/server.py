from flask import Flask, jsonify
from flask_cors import CORS
import sqlite3
import os

# Set up paths first
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "data", "gpro.db")

# Create the data folder if it doesn't exist
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

# Now import db and create tables
import db
db.create_tables()

app = Flask(__name__)
CORS(app)

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/api/setups")
def get_setups():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM race_setups ORDER BY season, race")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/api/setups/latest")
def get_latest_setup():
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
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
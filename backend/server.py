from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
import psycopg2.extras
import os
import db

# Create tables when server starts
db.create_tables()

app = Flask(__name__)
CORS(app)

def get_connection():
    """Opens a connection to the PostgreSQL database"""
    conn = psycopg2.connect(os.environ.get("DATABASE_URL"))
    return conn

@app.route("/api/setups")
def get_setups():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM race_setups ORDER BY season, race")
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/api/setups/latest")
def get_latest_setup():
    conn = get_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
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
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("""
        SELECT DISTINCT track_name, track_power, track_accel, track_handl
        FROM race_setups
        ORDER BY track_name
    """)
    rows = cursor.fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])

@app.route("/api/fetch")
def fetch_data():
    """Triggers a data fetch from the GPRO API"""
    import fetcher
    fetcher.main()
    return jsonify({"status": "Data fetched successfully!"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, port=port)
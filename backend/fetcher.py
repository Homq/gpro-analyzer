import requests
import json
import os
import db

API_TOKEN = "eyJ0eXAiOiJKV1QiLCAiYWxnIjoiSFMyNTYifQ.eyJpZCI6IDExMzQwMDUsImNyZWF0ZWQiOiJUaHUgQXByIDkgMjE6Mzk6MTUgVVRDKzAyMDAgMjAyNiJ9.IBfi-VrhN6CMNKKOxF2ZUhAvxMt2CSvTTW3_6mvdlD4"
BASE_URL = "https://gpro.net"

HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Content-Type": "application/json"
}

def fetch_race_summary():
    """Fetches the race standings/summary for your group"""
    print("Fetching race summary from GPRO...")
    response = requests.get(f"{BASE_URL}/gb/backend/api/v2/RaceSummary", headers=HEADERS)
    if response.status_code == 200:
        print("Successfully fetched race summary!")
        return response.json()
    else:
        print(f"Error fetching race summary: {response.status_code}")
        return None

def fetch_race_setup():
    """Fetches your personal race setup data"""
    print("Fetching race setup from GPRO...")
    response = requests.get(f"{BASE_URL}/gb/backend/api/v2/RaceSetup", headers=HEADERS)
    if response.status_code == 200:
        print("Successfully fetched race setup!")
        return response.json()
    else:
        print(f"Error fetching race setup: {response.status_code}")
        return None

def save_data(data, filename):
    """Saves fetched data to a JSON file in the data folder"""
    filepath = os.path.join("..", "data", filename)
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filepath}")


def main():
    # Make sure the database tables exist
    db.create_tables()

    # Fetch race summary (group standings)
    race_data = fetch_race_summary()
    if race_data:
        save_data(race_data, "race_summary.json")

    # Fetch personal race setup
    setup_data = fetch_race_setup()
    if setup_data:
        save_data(setup_data, "race_setup.json")

        # Add season and race from summary data into setup data before saving
        if race_data:
            setup_data["season"] = int(race_data.get("season") or 0)
            setup_data["race"] = int(race_data.get("race") or 0)

        # Save to database
        db.save_race_setup(setup_data)


if __name__ == "__main__":
    main()
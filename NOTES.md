# GPRO Analyzer

## Project Structure
- `backend/fetcher.py` — fetches data from GPRO API
- `backend/db.py` — database connection and table setup
- `backend/server.py` — Flask web server with API endpoints
- `docs/index.html` — frontend dashboard
- `requirements.txt` — Python dependencies
- `Procfile` — tells Railway how to start the server

## Live URLs
- Dashboard: https://homq.github.io/gpro-analyzer
- Backend: https://web-production-fc5cc.up.railway.app

## API Endpoints
- `/api/setups` — all race setups
- `/api/setups/latest` — most recent race
- `/api/tracks` — all tracks with characteristics
- `/api/fetch` — manually trigger a data fetch

## Auto-scheduling
Data is fetched automatically every Tuesday and Friday at 22:30 CET
(2.5 hours after GPRO races start at 20:00 CET)

## Local Development
```bash
cd ~/PycharmProjects/PythonProject
source venv/bin/activate
cd backend
python server.py
```

## Pushing updates to production
```bash
cd ~/PycharmProjects/PythonProject
git add .
git commit -m "your message here"
git push
```

## Environment Variables (Railway)
- `GPRO_API_TOKEN` — your GPRO API token
- `DATABASE_URL` — PostgreSQL connection string (public URL)
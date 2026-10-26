# Immune Research Analytics Dashboard

A portfolio project inspired by the *type* of software used in computational immunology. This is an independent demo and is not affiliated with Omniscope. All records are synthetic and must not be used for clinical decisions.

## Features
- FastAPI REST endpoints and interactive browser dashboard
- SQLite persistence with 90 seeded synthetic sample records
- Summary metrics and cohort/response charts
- Search and filters for sample records
- CSV export of filtered records
- Responsive layout and API health endpoint

## Tech stack
Python, FastAPI, SQLite, HTML, CSS, JavaScript, Chart.js.

## Run locally
Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000. API docs: http://127.0.0.1:8000/docs

## API endpoints
- `GET /api/health`
- `GET /api/summary`
- `GET /api/samples?q=IM-0001&cohort=Cohort%20A&response_group=Responder`

## Portfolio note
Explain that this project demonstrates full-stack data exploration, API design, persistence, filtering, and visualization. The biological measurements and response groups are generated sample data, not validated biomedical findings.

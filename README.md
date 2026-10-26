# Immune Research Analytics Dashboard

**Live demo:** https://immune-research-analytics.onrender.com  
**Interactive API docs:** https://immune-research-analytics.onrender.com/docs  
**Health endpoint:** https://immune-research-analytics.onrender.com/api/health

A portfolio project inspired by the *type* of software used in computational immunology. This is an independent demo and is not affiliated with Omniscope. All records are synthetic and must not be used for clinical decisions.

## Features
- FastAPI REST endpoints and interactive browser dashboard
- SQLite database seeded automatically with 90 synthetic sample records
- Summary metrics, cohort/response breakdowns, and monthly trend data
- Search and filters for sample records
- CSV export of filtered records
- Responsive layout and API health endpoint

## Tech stack
Python, FastAPI, SQLite, HTML, CSS, JavaScript, and Chart.js.

## API endpoints
| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/api/health` | Basic service health and synthetic-data status |
| GET | `/api/summary` | Aggregate metrics, cohort counts, response groups, and monthly trend |
| GET | `/api/samples?q=IM-0001&cohort=Cohort%20A&response_group=Responder` | Search/filter synthetic sample records |

## Run locally
Requires Python 3.10+.

```bash
python -m venv .venv
source .venv/bin/activate       # macOS/Linux
# Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

Open http://127.0.0.1:8000. API docs: http://127.0.0.1:8000/docs.

## Portfolio notes
This project demonstrates full-stack data exploration, API design, persistence, filtering, and visualization. The biological measurements and response groups are generated sample data, not validated biomedical findings.

## Deployment
Hosted on Render. The free service may spin down after inactivity, so the first request after a quiet period can take longer to respond.

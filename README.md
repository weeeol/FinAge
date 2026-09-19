# FinAge

FinAge is a one-day hackathon MVP for personal finance decision support. It imports transaction records, normalizes and categorizes them, calculates deterministic financial analytics, identifies recurring obligations, and optionally explains the results with grounded AI.

FinAge is not an investment advisor. It does not provide investment, stock, trading, or financial-product recommendations.

## Foundation

This repository currently contains the project foundation and architecture documentation. Implementation is intentionally delegated to the Antigravity implementation agent in small tasks.

- [Architecture](.agents/ARCHITECTURE.md)
- [Implementation tasks](.agents/TASKS.md)
- [API contract](.agents/API_CONTRACT.md)
- [Data model](.agents/DATA_MODEL.md)
- [Architecture decisions](.agents/DECISIONS.md)
- [Contributor skills](.agents/skills/)

## Target stack

- Frontend: React, Vite, Tailwind CSS, Recharts
- Backend: Python, FastAPI, Pydantic, SQLAlchemy
- Data: SQLite and Pandas
- Documents: PyMuPDF for text PDFs, CSV/XLSX parsing through Pandas
- AI: OpenAI API behind a grounded adapter
- Tests: Pytest and focused frontend smoke tests

## Local setup

1. Copy `.env.example` to `.env`:
   ```text
   cp .env.example .env
   ```

2. Backend setup (Python 3.13):
   ```text
   py -3.13 -m venv .venv
   .venv\Scripts\pip install -r backend/requirements.txt
   .venv\Scripts\uvicorn app.main:app --app-dir backend --reload --port 8000
   ```

3. Frontend setup (Node.js):
   ```text
   cd frontend
   npm install
   npm run dev
   ```

4. Testing:
   ```text
   .venv\Scripts\pytest tests/
   ```

Never commit API keys, uploaded statements, or local SQLite files.

## Operating rules

Before implementation changes, read the five documents under `.agents/`. Architecture, API, schema, folder, and technology-stack changes must be explained and recorded in [DECISIONS.md](.agents/DECISIONS.md) and the affected contract. Deterministic backend calculations are authoritative; AI explains structured results and never replaces arithmetic.
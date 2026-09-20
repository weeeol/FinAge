# FinAge

FinAge is a local-first personal finance decision-support workspace. It imports transaction records, normalizes and categorizes them, calculates deterministic financial analytics, identifies recurring obligations, and optionally explains the results with grounded Gemini AI.

FinAge is not an investment advisor. It does not provide investment, stock, trading, or financial-product recommendations.

All financial calculations are performed by the backend. Amounts are stored as integer paise and displayed as Indian rupees. Gemini receives only structured financial context and cannot change stored financial data.

**Live demo:** [finageai.vercel.app](https://finageai.vercel.app)

## Features

- CSV, XLSX, and text-based PDF statement import
- Deterministic income, expense, net, category, monthly, and recurring-payment analytics
- Monthly budgets with on-track, warning, and exceeded states
- Financial goals with deterministic progress tracking
- Grounded `/api/ask` explanations through Gemini, with graceful no-key behavior
- Synthetic demo statement and a reset-database action for local demos

## Project structure

- `backend/` - FastAPI API, SQLite/SQLAlchemy data layer, parsers, analytics, and Gemini adapter
- `frontend/` - React/Vite dashboard
- `tests/` - backend regression tests
- `docs/demo_transactions.csv` - synthetic demo transactions
- `data/sample_statement.csv` - smaller synthetic import fixture
- `.agents/` - architecture, contracts, decisions, and implementation notes

## Quick start

Requirements: Python 3.13+, Node.js 20+, and npm.

1. Create local configuration:

   ```powershell
   Copy-Item .env.example .env
   ```

   Add a Gemini API key to `.env` only if you want to use the assistant:

   ```text
   GEMINI_API_KEY=your_key_here
   GEMINI_MODEL=gemini-3.6-flash
   ```

2. Create the Python environment and install backend dependencies:

   ```powershell
   py -3.13 -m venv .venv
   .\.venv\Scripts\pip install -r backend\requirements.txt
   ```

3. Start the backend from the repository root:

   ```powershell
   .\.venv\Scripts\uvicorn app.main:app --app-dir backend --reload --port 8000
   ```

4. In a second terminal, start the frontend:

   ```powershell
   Set-Location frontend
   npm install
   npm run dev
   ```

Open `http://localhost:5173`.

## Docker Compose

The local stack can also be started with:

```powershell
Copy-Item .env.example .env
docker compose up --build
```

Gemini remains optional. Without a key, deterministic dashboard features continue to work and the assistant returns a controlled unavailable response.

## Demo data

Upload [docs/demo_transactions.csv](docs/demo_transactions.csv) from the dashboard. It is synthetic data only. Amounts follow the project convention: positive values are income and negative values are expenses.

The database icon in the header resets local financial records, including uploaded transactions, budgets, goals, recurring payments, and summaries. It preserves the demo user and category catalog and asks for confirmation first.

## API

- `GET /health` - readiness check
- `POST /api/upload` - import CSV, XLSX, or text PDF data
- `GET /api/transactions` - paginated transaction list
- `GET /api/analytics/monthly` - monthly totals
- `GET /api/analytics/categories` - category totals
- `GET /api/analytics/recurring` - recurring-payment candidates
- `POST /api/budgets` and `GET /api/analytics/budgets` - budget management
- `GET /api/goals` and `POST /api/goals` - goal management
- `POST /api/ask` - grounded Gemini explanation
- `POST /api/reset-database` - clear local demo financial data

Interactive API documentation is available at `http://localhost:8000/docs` while the backend is running.

## Testing

```powershell
.\.venv\Scripts\pytest -q
Set-Location frontend
npm run build
```

## Privacy and security

- Never commit `.env`, API keys, uploaded statements, or SQLite files.
- The application is designed for local development and demo use. Do not expose it publicly without authentication, authorization, HTTPS, and database protections.
- The reset endpoint is intentionally unauthenticated because this is a single-user local MVP; keep it off any public deployment.
- Demo files in this repository contain synthetic transactions only.

## Architecture documentation

- [Architecture](.agents/ARCHITECTURE.md)
- [Implementation tasks](.agents/TASKS.md)
- [API contract](.agents/API_CONTRACT.md)
- [Data model](.agents/DATA_MODEL.md)
- [Architecture decisions](.agents/DECISIONS.md)

## Target stack

- Frontend: React, Vite, Tailwind CSS, Recharts
- Backend: Python, FastAPI, Pydantic, SQLAlchemy
- Data: SQLite and Pandas
- Documents: PyMuPDF for text PDFs, CSV/XLSX parsing through Pandas
- AI: Gemini API behind a grounded adapter
- Tests: Pytest and focused frontend smoke tests

## Operating rules

Before implementation changes, read the five documents under `.agents/`. Architecture, API, schema, folder, and technology-stack changes must be explained and recorded in [DECISIONS.md](.agents/DECISIONS.md) and the affected contract. Deterministic backend calculations are authoritative; AI explains structured results and never replaces arithmetic.
# FinAge Architecture

## 1. System overview
FinAge is a single-user, local-first personal finance decision-support MVP. A React/Vite frontend calls one FastAPI application. The backend extracts and normalizes uploaded records, stores structured data in SQLite, performs deterministic analytics, and optionally asks OpenAI to explain those results. The product does not provide investment, stock, trading, or financial-product recommendations.

Primary flow:

`Upload -> Extract -> Normalize -> Store -> Analyze -> Present -> Explain with grounded AI`

The backend is the source of truth for financial arithmetic. The MVP assumes one local user profile and does not require authentication.

## 2. Component architecture
- **Frontend:** React, Vite, Tailwind CSS, Recharts. Dashboard, upload flow, filters, budgets/goals forms, insights, and Q&A.
- **API:** FastAPI routes with Pydantic request/response models and consistent error envelopes.
- **Application services:** Upload orchestration, transaction service, analytics service, budget/goal service, insight service, and Q&A service.
- **Data processing:** Pandas for CSV/XLSX, PyMuPDF for text PDFs, normalization and categorization rules, recurring-payment and anomaly heuristics.
- **Persistence:** SQLAlchemy models and repositories over SQLite.
- **AI adapter:** OpenAI client behind a small service boundary. It receives a compact structured financial context, not raw documents.

Keep the application modular inside one backend process. Do not add microservices, queues, or event buses.

## 3. Frontend architecture
Use feature-oriented folders under `frontend/src`: `components/`, `features/transactions/`, `features/analytics/`, `features/budgets/`, `features/goals/`, `features/assistant/`, `lib/`, and `types/`. Keep API calls in one typed client module. Use server responses rather than duplicating financial calculations in the browser. Recharts is for monthly trends, category distribution, and recurring obligations. Provide loading, empty, error, and upload-progress states. The visual direction is a light, calm finance workspace with editorial serif headings, restrained muted green/coral/gold accents, clear hierarchy, and minimal decorative chrome; avoid dark gradient-heavy status dashboards and generic card grids.

## 4. Backend architecture
Use a thin route layer: validate input, call a service, map result to a response model. Services own business rules. Parsers return normalized transaction candidates and do not write directly to the database. SQLAlchemy models represent persisted state. Configuration comes from environment variables with safe local defaults. Keep dependencies explicit and avoid a generic repository framework unless repetition proves it useful.

Suggested modules: `app/main.py`, `app/api/`, `app/core/`, `app/db/`, `app/models/`, `app/schemas/`, `app/services/`, `app/processing/`, and `app/ai/`.

## 5. Data processing pipeline
1. Validate file type and size.
2. Extract rows from CSV/XLSX or text from PDF using the appropriate parser.
3. Map provider-specific columns to date, description, amount, and optional account fields.
4. Normalize dates, signs, currency, whitespace, and duplicate rows.
5. Assign a category using deterministic keyword/rule matching with an `Other` fallback.
6. Persist transactions with source metadata.
7. Recompute recurring payments, monthly totals, category totals, budget comparisons, and anomaly candidates from stored transactions.
8. Return structured results to the UI; only then create optional AI explanations.

OCR is out of scope for the initial MVP. Unsupported or image-only PDFs should produce a clear actionable error.

## 6. AI architecture
The AI adapter accepts a structured context containing selected date range, aggregates, transaction excerpts, recurring items, budgets, goals, and user question. Prompts require the model to use only supplied data, state when data is insufficient, avoid investment advice, and return a bounded response. The service must never let model output alter persisted financial values. OpenAI is optional: deterministic dashboard features must work without an API key, while AI endpoints return a controlled unavailable response when it is absent.

## 7. Database architecture
SQLite is the MVP database. SQLAlchemy manages schema access; use a lightweight initialization path for the demo. Store money as integer minor units (for example cents) plus an ISO currency code to avoid floating-point arithmetic. Dates are timezone-naive ISO dates for statement-level data. A single default user is sufficient for the demo, but records retain `user_id` for clean extension later.

## 8. API architecture
All application routes are under `/api`. JSON responses use stable names and ISO dates. Upload is multipart form data. List endpoints support simple `from_date`, `to_date`, `category`, and pagination parameters only where useful. Errors use `{ "error": { "code": "...", "message": "...", "details": {} } }`. OpenAPI generated by FastAPI is the contract reference, while `.agents/API_CONTRACT.md` defines MVP intent.

## 9. Security considerations
- Keep `OPENAI_API_KEY` in environment variables and exclude `.env` files.
- Enforce an upload size limit and allow only CSV, XLSX, and text-readable PDF extensions.
- Sanitize filenames and never execute uploaded content.
- Do not log raw transaction descriptions or document contents unnecessarily.
- Use parameterized SQL through SQLAlchemy.
- Treat AI responses as untrusted display text; do not execute or interpret them as commands.
- Authentication and multi-user isolation are deferred; do not expose the demo database publicly.

## 10. Error handling
Use typed application exceptions mapped to HTTP 400 for invalid files/input, 404 for missing resources, 422 for schema validation, 503 for unavailable optional AI, and 500 for unexpected failures. Return useful user-facing messages without stack traces. Log server-side context with request IDs where practical. Partial parsing failures should report skipped rows and continue only when the result remains trustworthy.

## 11. Deployment architecture
For the hackathon, run frontend and backend locally with SQLite on a mounted local data directory. `docker-compose.yml` may orchestrate the two development containers, but no cloud services are required. The frontend uses a Vite proxy or `VITE_API_BASE_URL`; the backend serves API and OpenAPI docs. A future deployment can package the same FastAPI process and SQLite volume, but production-grade auth, backups, and concurrency are outside MVP scope.

# FinAge Implementation Tasks

Antigravity owns implementation. Tasks are ordered by dependency but can be assigned independently once prerequisites are complete. Every implementation task must preserve the documented API and data model or update the relevant architecture record first.

## Continuation checkpoint

The previous implementation run completed the main P0-07 data-backed dashboard and partially completed P0-09. Do not rebuild P0-07 from scratch.

- **P0-08 status:** Not started. No `/api/ask`, AI adapter, grounded context builder, or assistant UI currently exists.
- **P0-09 status:** Partially complete. FinAge naming and the light editorial visual system are present in the current frontend/backend implementation. Remaining work is a full stale-name audit, browser metadata/package-name consistency, responsive verification, and regression checks.
- **Resume order:** P0-08 backend contract and tests -> P0-08 assistant UI -> P0-09 rename audit and visual regression -> full focused validation.
- **Ownership boundary:** Antigravity may modify implementation files listed by the tasks. Copilot-owned architecture and contract documents must not be changed unless an API/schema/design decision actually changes.

## P0: Required for demo

### P0-01 Project setup
- **Description:** Create Vite React frontend, FastAPI backend package, dependency manifests, environment example, and local run commands.
- **Files likely affected:** `frontend/`, `backend/`, `README.md`, `docker-compose.yml`
- **Dependencies:** None
- **Acceptance criteria:** Frontend and backend start locally; `/health` responds; no secrets committed.

### P0-02 Database and seed data
- **Description:** Implement SQLAlchemy models, SQLite initialization, default user/categories, and session management for the schema in `DATA_MODEL.md`.
- **Files likely affected:** `backend/app/db/`, `backend/app/models/`, `backend/app/core/`
- **Dependencies:** P0-01
- **Acceptance criteria:** Database initializes reproducibly; relationships and unique constraints work; seed data supports a blank demo.

### P0-03 Transaction import and normalization
- **Description:** Accept CSV/XLSX uploads, map common columns, normalize signs/dates/descriptions, reject unsafe or unusable files, and persist transactions.
- **Files likely affected:** `backend/app/api/upload.py`, `backend/app/processing/`, `backend/app/services/import_service.py`
- **Dependencies:** P0-02
- **Acceptance criteria:** Sample statement imports with counts and warnings; invalid rows are handled transparently; duplicate imports do not blindly duplicate rows.

### P0-04 Categorization
- **Description:** Add deterministic category rules with an `Other` fallback and assign categories during import.
- **Files likely affected:** `backend/app/processing/categorizer.py`, `backend/app/services/import_service.py`, `backend/tests/`
- **Dependencies:** P0-02, P0-03
- **Acceptance criteria:** Common merchants map to stable categories; unmatched transactions remain visible; categorization is unit tested.

### P0-05 Monthly and category analytics
- **Description:** Implement backend calculations for income, expenses, net, monthly trends, category totals, and summary endpoints.
- **Files likely affected:** `backend/app/services/analytics_service.py`, `backend/app/api/analytics.py`, `backend/app/schemas/`
- **Dependencies:** P0-02, P0-03, P0-04
- **Acceptance criteria:** Totals use integer arithmetic; empty periods return valid zero-valued responses; API responses match `API_CONTRACT.md`.

### P0-06 Recurring payment detection
- **Description:** Detect repeated merchant/amount patterns, estimate frequency and next date, and expose upcoming obligations.
- **Files likely affected:** `backend/app/services/recurring_service.py`, `backend/app/api/analytics.py`
- **Dependencies:** P0-03, P0-05
- **Acceptance criteria:** Monthly repeats are detected from fixture data with confidence; irregular transactions are not presented as certain subscriptions.

### P0-07 Dashboard
- **Description:** Build the primary responsive dashboard with upload, summary cards, monthly chart, category chart, recurring obligations, and clear loading/error/empty states.
- **Files likely affected:** `frontend/src/`
- **Dependencies:** P0-01, P0-05, P0-06
- **Acceptance criteria:** A new user can upload a statement and see refreshed totals and charts; mobile layout remains usable; browser never calculates authoritative totals.

### P0-08 Grounded AI Q&A
- **Description:** Build a structured-context AI adapter and `/api/ask`, with optional API-key behavior, refusal boundaries, and source facts in responses.
- **Files likely affected:** `backend/app/ai/`, `backend/app/services/qa_service.py`, `backend/app/api/ask.py`, `frontend/src/features/assistant/`
- **Dependencies:** P0-05, P0-06
- **Acceptance criteria:** Questions answer from supplied aggregates; missing data is acknowledged; no investment recommendations; endpoint works in controlled unavailable mode without a key.
- **Implementation sequence:**
	1. Build a bounded context DTO from existing summary, monthly, category, recurring, and transaction services; do not pass uploaded files or unrestricted database dumps to the model.
	2. Add Pydantic request/response schemas matching `API_CONTRACT.md` and a thin `/api/ask` route.
	3. Add a Gemini adapter behind a service boundary. If `GEMINI_API_KEY` is absent, return the documented `503 ai_unavailable` response without breaking the dashboard.
	4. Add mocked tests for grounding, insufficient data, refusal of investment questions, malformed provider output, and no-key behavior.
	5. Add the smallest useful assistant panel to the existing FinAge UI; preserve current loading/error/refresh/upload flows.

### P0-09 FinAge visual system recovery and product rename
- **Description:** Restore the approved FinAge dashboard direction after the P0-07 implementation: light workspace shell, restrained editorial typography, muted green/coral/gold palette, clear financial hierarchy, and responsive layouts. Replace all user-visible and runtime product references from FinPilot to FinAge without changing API paths or financial behavior.
- **Files likely affected:** `frontend/src/`, `frontend/package.json`, `frontend/package-lock.json`, `backend/app/core/config.py`, `backend/app/main.py`, `backend/app/db/`, `backend/app/services/`, `README.md`
- **Dependencies:** P0-07
- **Acceptance criteria:**
	- Header, page title, metadata, backend title/description, seed identity, and user-facing errors consistently say FinAge.
	- Dashboard no longer presents as a dark generic status/card wall; it presents the finance workspace described in `ARCHITECTURE.md` with summary, trends, categories, recurring obligations, transactions, and upload action.
	- Existing upload, refresh, loading, empty, error, pagination, and chart data flows remain functional.
	- Responsive behavior is verified at desktop and narrow mobile widths.
	- No new investment, stock, trading, or financial-product recommendation language is introduced.
	- `npm run build` and focused backend/frontend checks pass.
- **Current implementation note:** The current `frontend/src/components/` already contains the light FinAge palette and serif treatment. Review and refine those files in place; do not replace them with a new dark template.
- **Rename audit:** Search tracked source/config/docs for `FinPilot`; remaining occurrences should be intentional historical references only. Runtime strings, package metadata, page title, API metadata, seed email, logs, and user-facing errors must use `FinAge`.

## P1: Important

### P1-01 Text PDF parsing
- **Description:** Extract tables/text from text-based PDFs with PyMuPDF and feed the same normalization pipeline.
- **Files likely affected:** `backend/app/processing/pdf_parser.py`, `backend/app/services/import_service.py`
- **Dependencies:** P0-03
- **Acceptance criteria:** A representative text PDF imports or returns a precise unsupported-layout warning; image-only PDFs do not silently produce bad data.

### P1-02 Budgets
- **Description:** Add budget CRUD, month/category comparisons, and dashboard status indicators.
- **Files likely affected:** `backend/app/api/budgets.py`, `backend/app/services/budget_service.py`, `frontend/src/features/budgets/`
- **Dependencies:** P0-05, P0-07
- **Acceptance criteria:** Over-budget and on-track states are deterministic and tested; API matches contract.

### P1-03 Financial goals
- **Description:** Add goal CRUD and deterministic progress/spending-impact indicators.
- **Files likely affected:** `backend/app/api/goals.py`, `backend/app/services/goal_service.py`, `frontend/src/features/goals/`
- **Dependencies:** P0-05, P0-07
- **Acceptance criteria:** Goal progress is calculated from stored values; copy clearly states decision support, not advice.

### P1-04 Monthly summary
- **Description:** Compose a monthly summary from persisted analytics, recurring obligations, budgets, goals, and optional AI prose.
- **Files likely affected:** `backend/app/api/monthly_summary.py`, `backend/app/services/summary_service.py`, `frontend/src/features/summary/`
- **Dependencies:** P0-05, P0-06, P1-02, P1-03
- **Acceptance criteria:** Summary is reproducible without AI and includes the main deterministic facts.

## P2: Optional polish

### P2-01 OCR
- **Description:** Explore OCR only for a clearly supported statement sample.
- **Files likely affected:** `backend/app/processing/`
- **Dependencies:** P1-01
- **Acceptance criteria:** OCR is isolated, time-bounded, and never blocks normal imports.

### P2-02 Advanced anomaly detection
- **Description:** Add explainable outlier heuristics beyond basic unusual-spend flags.
- **Files likely affected:** `backend/app/services/analytics_service.py`, `frontend/src/`
- **Dependencies:** P0-05
- **Acceptance criteria:** Alerts include the comparison window and threshold used.

### P2-03 Authentication and deployment polish
- **Description:** Add authentication, production configuration, backup guidance, and hosted deployment only if demo needs it.
- **Files likely affected:** `backend/app/`, `frontend/`, deployment files
- **Dependencies:** All required MVP tasks
- **Acceptance criteria:** Security review covers user isolation and secret handling before any public exposure.

## Dependency summary
`P0-01 -> P0-02 -> P0-03 -> P0-04 -> P0-05 -> P0-06 -> P0-07`

`P0-05 + P0-06 -> P0-08`

`P0-03 -> P1-01`; `P0-05 + P0-07 -> P1-02/P1-03`; `P1-02 + P1-03 -> P1-04`.

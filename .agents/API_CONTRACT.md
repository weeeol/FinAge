# FinAge API Contract

Base path: `/api`. JSON dates are `YYYY-MM-DD`; money is integer minor units. Unless noted, responses are JSON. Error shape:

```json
{"error":{"code":"validation_error","message":"Readable explanation","details":{}}}
```

## Health
### GET `/health`
Purpose: process readiness check.
Response: `{ "status": "ok" }`.

### POST `/api/reset-database`
Purpose: clear local demo financial data while preserving the seeded demo user and category catalog.
Response: `{ "status": "ok", "message": "Demo financial data was reset." }`.

## Upload
### POST `/api/upload`
Request: multipart form field `file`; accepted `.csv`, `.xlsx`, `.pdf`.
Response `201`: `{ "imported": 42, "skipped": 1, "categories_assigned": 38, "warnings": [] }`.
Errors: `400 invalid_file`, `413 file_too_large`, `422 unsupported_format`.

## Transactions
### GET `/api/transactions`
Query: `from_date`, `to_date`, `category`, `page=1`, `page_size=50`.
Response: `{ "items": [{ "id": 1, "date": "2026-01-05", "description": "Market", "amount_minor": -4200, "currency": "USD", "category": "Groceries" }], "page": 1, "page_size": 50, "total": 1 }`.

### GET `/api/transactions/summary`
Query: optional `from_date`, `to_date`.
Response: `{ "income_minor": 500000, "expense_minor": 210000, "net_minor": 290000, "transaction_count": 52, "currency": "USD" }`.

## Analytics
### GET `/api/analytics/monthly`
Query: optional `months=6`.
Response: `{ "items": [{ "month": "2026-01", "income_minor": 500000, "expense_minor": 210000, "net_minor": 290000 }] }`.

### GET `/api/analytics/categories`
Query: optional `month`.
Response: `{ "items": [{ "category": "Groceries", "amount_minor": 42000, "transaction_count": 12, "share": 0.2 }] }`.

### GET `/api/analytics/recurring`
Response: `{ "items": [{ "merchant_name": "Stream Co", "typical_amount_minor": 1599, "frequency": "monthly", "next_expected_date": "2026-10-01", "confidence": 0.92 }] }`.

### GET `/api/analytics/budgets`
Query: optional `month`.
Response: `{ "items": [{ "budget_id": 1, "category": "Groceries", "limit_minor": 50000, "spent_minor": 42000, "remaining_minor": 8000, "percent_used": 0.84, "status": "on_track" }] }`.

## Budgets
### POST `/api/budgets`
Request: `{ "category": "Groceries", "month": "2026-10", "limit_minor": 50000, "currency": "USD" }`.
Response `201`: created budget object. Errors: `400 invalid_amount`, `409 duplicate_budget`.

## Goals
### GET `/api/goals`
Response: `{ "items": [{ "id": 1, "name": "Emergency fund", "target_minor": 1000000, "current_minor": 250000, "target_date": "2027-06-01", "progress": 0.25 }] }`.

### POST `/api/goals`
Request: `{ "name": "Emergency fund", "target_minor": 1000000, "current_minor": 250000, "target_date": "2027-06-01", "currency": "USD" }`.
Response `201`: created goal object. Errors: `400 invalid_goal`.

## AI and summaries
### GET `/api/insights`
Query: optional `month`.
Response: `{ "items": [{ "type": "anomaly|recurring|budget|goal", "title": "...", "description": "...", "severity": "info|warning" }] }`.
The deterministic service creates the facts; AI wording is optional.

### POST `/api/ask`
Request: `{ "question": "Where did I spend the most last month?", "from_date": "2026-09-01", "to_date": "2026-09-30" }`.
Response `200`: `{ "answer": "...", "sources": [{ "kind": "category_total", "label": "Groceries", "amount_minor": 42000 }] }`.
Errors: `400 empty_question`, `503 ai_unavailable`. Responses must state when data is insufficient and must not give investment advice.

### GET `/api/monthly-summary`
Query: required `month=YYYY-MM`.
Response: `{ "month": "2026-09", "income_minor": 500000, "expense_minor": 210000, "net_minor": 290000, "top_categories": [], "recurring_obligations": [], "insights": [] }`.

## Contract rules
- Unknown query filters are rejected or ignored consistently; prefer Pydantic validation and a documented allowlist.
- Amount calculations happen in backend services, never in the LLM or from client-submitted totals.
- Every endpoint returns a stable error envelope and no stack traces.

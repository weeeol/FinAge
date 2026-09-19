# FinPilot Data Model

All monetary values are integer minor units (`int`, normally cents). Currency is an ISO 4217 string, default `USD`. Dates use ISO `YYYY-MM-DD`. SQLAlchemy owns persistence; these definitions describe the MVP contract.

## User
- `id`: integer, primary key
- `name`: string, required
- `email`: string, nullable, unique when present
- `currency`: string(3), required, default `USD`
- `created_at`: datetime, required

Relationships: one-to-many with all user-owned entities.

## Category
- `id`: integer, primary key
- `name`: string, required, unique
- `kind`: enum/string `income|expense|transfer|other`
- `created_at`: datetime, required

Index: unique `name`.

## Transaction
- `id`: integer, primary key
- `user_id`: integer, required FK `user.id`
- `category_id`: integer, nullable FK `category.id`
- `transaction_date`: date, required
- `description`: string, required
- `amount_minor`: integer, required; positive income, negative expense
- `currency`: string(3), required
- `source_file`: string, nullable
- `external_id`: string, nullable
- `is_recurring_candidate`: boolean, default false
- `created_at`: datetime, required

Indexes: `(user_id, transaction_date)`, `(user_id, category_id)`, and `(user_id, description)` for recurring analysis. Duplicate detection may use `(user_id, transaction_date, description, amount_minor, source_file)` in application logic.

## RecurringPayment
- `id`: integer, primary key
- `user_id`: integer, required FK
- `category_id`: integer, nullable FK
- `merchant_name`: string, required
- `typical_amount_minor`: integer, required
- `currency`: string(3), required
- `frequency`: string, required, MVP values `weekly|monthly|annual|unknown`
- `next_expected_date`: date, nullable
- `confidence`: float, required, 0 to 1
- `last_seen_date`: date, required
- `created_at`: datetime, required

Index: `(user_id, next_expected_date)`.

## Budget
- `id`: integer, primary key
- `user_id`: integer, required FK
- `category_id`: integer, nullable FK; null means total expense budget
- `month`: string(7), required, `YYYY-MM`
- `limit_minor`: integer, required and non-negative
- `currency`: string(3), required
- `created_at`: datetime, required

Unique constraint: `(user_id, category_id, month)`.

## FinancialGoal
- `id`: integer, primary key
- `user_id`: integer, required FK
- `name`: string, required
- `target_minor`: integer, required and positive
- `current_minor`: integer, default 0
- `target_date`: date, nullable
- `currency`: string(3), required
- `created_at`: datetime, required

Index: `(user_id, target_date)`.

## MonthlySummary
- `id`: integer, primary key
- `user_id`: integer, required FK
- `month`: string(7), required, `YYYY-MM`
- `income_minor`: integer, required
- `expense_minor`: integer, required as a positive total
- `net_minor`: integer, required
- `transaction_count`: integer, required
- `top_category_id`: integer, nullable FK
- `generated_insight`: text, nullable; informational cache only
- `created_at`: datetime, required

Unique constraint: `(user_id, month)`.

## MVP relationship diagram
`User 1--* Transaction *--1 Category`

`User 1--* RecurringPayment *--1 Category`

`User 1--* Budget *--0..1 Category`

`User 1--* FinancialGoal`

`User 1--* MonthlySummary *--0..1 Category`

No raw uploaded document table is required for the first demo. Source filename on transactions is enough; file retention and document audit history can be added later.

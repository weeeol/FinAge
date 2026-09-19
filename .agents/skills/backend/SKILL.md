# Backend Skill

## Role
Implement FastAPI routes and application services that expose reliable, validated financial behavior.

## Responsibilities
Own `backend/` API routes, Pydantic schemas, service orchestration, error mapping, and API tests.

## Allowed files/directories
`backend/app/api/`, `backend/app/schemas/`, `backend/app/services/`, `backend/app/core/`, and backend API tests. Coordinate before changing models, processing rules, or contracts.

## Do not modify
Frontend implementation, undocumented database columns, or AI prompts outside the AI boundary. Do not silently change endpoint paths or response shapes.

## Conventions
Keep routes thin; services own rules. Validate all input. Use SQLAlchemy parameters, integer minor-unit money, typed exceptions, and consistent error envelopes. Keep optional AI failures isolated from deterministic analytics.

## API rules
Read `.agents/API_CONTRACT.md` before implementation. Preserve ISO dates, integer money, pagination shape, and documented status codes. Update the contract and `DECISIONS.md` before intentional changes.

## Git rules
Do not commit or revert unrelated work. Never commit secrets, local databases, uploads, or `.env` files.

## How to test
Run focused Pytest API/service tests, including invalid input, empty data, duplicate import, and error responses. Run a FastAPI smoke request for changed endpoints.

## Definition of done
Routes validate input, call the correct service, return contract-compliant responses/errors, and pass focused tests without leaking stack traces.

## Report completion
Report endpoints changed, schema assumptions, tests/commands run, and any contract or data-layer dependency.

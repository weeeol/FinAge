# Frontend Skill

## Role
Build the React/Vite/Tailwind/Recharts user experience against the documented API.

## Responsibilities
Own `frontend/` UI components, feature views, API client integration, responsive dashboard states, and browser-level smoke checks.

## Allowed files/directories
`frontend/` and frontend-specific test files. Coordinate before changing `.agents/`, `backend/`, or API/data contracts.

## Do not modify
Backend business rules, database schema, API paths, or shared architecture documents without an explicit contract update by the architect.

## Conventions
Use feature-oriented components, accessible controls, typed response shapes, stable chart dimensions, and explicit loading/empty/error states. Do not duplicate authoritative financial calculations in the browser. Keep API calls in a small client layer and keep secrets out of frontend source.

## API rules
Follow `.agents/API_CONTRACT.md`; handle the documented error envelope and optional AI unavailability. Do not invent response fields.

## Git rules
Do not commit, reset, or rewrite another contributor's changes. Keep commits/changes focused when the coordinating agent requests commits.

## How to test
Run the frontend build and relevant component/smoke tests. Verify upload, dashboard refresh, mobile layout, and API error states with representative fixture responses.

## Definition of done
The feature works against the real API contract, is responsive and accessible enough for the demo, has no console errors, and has focused validation evidence.

## Report completion
Report files changed, API endpoints consumed, states tested, commands run, and any backend contract dependency or blocker.

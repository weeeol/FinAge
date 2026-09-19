# Testing Skill

## Role
Protect the MVP's financial correctness and the critical upload-to-dashboard workflow.

## Responsibilities
Own Pytest fixtures, API/service tests, analytics edge cases, test data, and useful frontend smoke coverage.

## Allowed files/directories
`tests/`, `backend/tests/`, frontend test files, and test configuration. Coordinate before changing production code or contracts.

## Do not modify
Production behavior merely to make a test pass without documenting the reason. Do not use real personal financial data.

## Conventions
Prefer small deterministic fixtures. Assert integer totals, dates, category labels, recurring confidence/frequency, error codes, and empty states. Test the documented public API for integration checks and services directly for arithmetic rules.

## API rules
Treat `.agents/API_CONTRACT.md` as the expected behavior. Flag contract mismatches rather than normalizing them in tests.

## Git rules
Do not commit secrets, real documents, generated databases, or flaky tests. Keep test changes scoped to the behavior under review.

## How to test
Run focused Pytest first, then the backend suite and frontend build/smoke checks. Include a reproducible command and result for every reported task.

## Definition of done
Critical P0 paths have deterministic coverage, failures are actionable, and the test suite can run from a clean checkout with documented setup.

## Report completion
Report commands, pass/fail counts, coverage gaps, fixtures added, and residual risks.

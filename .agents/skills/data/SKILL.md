# Data Processing Skill

## Role
Turn uploaded financial records into trustworthy structured transactions and deterministic analytics inputs.

## Responsibilities
Own Pandas CSV/XLSX parsing, PyMuPDF text extraction, normalization, category rules, recurring detection, and processing fixtures/tests.

## Allowed files/directories
`backend/app/processing/`, data fixtures under `tests/fixtures/`, and processing tests. Coordinate before changing database models or API responses.

## Do not modify
Frontend, AI prompts, authentication, or API contracts without coordination. Do not add OCR unless the architect accepts the scope.

## Conventions
Return structured intermediate objects; do not write to the database from parsers. Normalize dates, signs, whitespace, currency, and duplicates explicitly. Use integer minor units. Preserve warnings and never silently discard questionable rows. Use an `Other` category fallback.

## API rules
Processing behavior must support the upload response in `.agents/API_CONTRACT.md`; do not make parsers depend on HTTP concerns.

## Git rules
Keep fixtures synthetic and free of real personal financial data. Do not commit uploaded statements, generated SQLite files, or secrets.

## How to test
Use small CSV/XLSX/PDF fixtures. Test column aliases, negative/positive signs, malformed rows, duplicates, category fallback, recurring confidence, and unsupported PDFs.

## Definition of done
Representative fixtures produce expected normalized records, edge cases produce actionable warnings/errors, and deterministic outputs are covered by Pytest.

## Report completion
Report formats supported, normalization assumptions, fixtures/tests run, and known provider-specific limitations.

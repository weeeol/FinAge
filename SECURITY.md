# Security Policy

## Scope

FinAge is a local-first hackathon MVP and is not configured for public production use. It has no authentication, authorization, or multi-user isolation at the HTTP boundary.

## Reporting a vulnerability

Do not open a public issue containing secrets, API keys, uploaded financial documents, or exploitable details. Contact the repository maintainer privately through the hosting provider's security contact process.

## Local safety

- Keep `.env` out of version control.
- Use synthetic data for demos and tests.
- Do not expose the unauthenticated API or `/api/reset-database` endpoint to the public internet.
- Rotate any API key that may have been committed or shared accidentally.
# FinAge Architecture Decisions

## Decision: FinAge is the canonical product name
Reason:
The product identity is FinAge. Consistent naming across the UI, API metadata, package metadata, seed data, and documentation prevents confusing demo output and handoff drift.

Alternatives:
Keep the earlier FinPilot name in implementation internals.

Why not:
Mixed names make the product look unfinished and can leak into user-visible errors, browser metadata, and generated API documentation.

## Decision: SQLite
Reason:
Simple zero-configuration database suitable for a one-day MVP and local demo.

Alternatives:
PostgreSQL

Why not:
Adds setup and deployment complexity before the core workflow is proven.

## Decision: Monolithic FastAPI backend
Reason:
A single process keeps routing, processing, analytics, and persistence easy to run and debug.

Alternatives:
Microservices, serverless functions

Why not:
Distributed deployment and contracts would consume hackathon time without improving the demo.

## Decision: Deterministic analytics before AI
Reason:
Financial totals, dates, categories, budgets, and recurring-payment calculations need predictable and testable results.

Alternatives:
Ask the LLM to analyze raw statements

Why not:
Raw-document prompting is less reliable, harder to test, and risks invented arithmetic.

## Decision: Integer minor-unit money
Reason:
Integer arithmetic avoids floating-point rounding errors in totals and budget comparisons.

Alternatives:
Python floats

Why not:
Small rounding errors are unacceptable in financial summaries.

## Decision: Single local demo user
Reason:
The MVP needs a usable live demo, not a complete identity system.

Alternatives:
OAuth, password authentication, multi-tenant authorization

Why not:
Authentication adds setup and security surface; user-owned foreign keys preserve a future migration path.

## Decision: CSV/XLSX first, text PDF second

## Decision: Gemini for grounded AI explanations
Reason:
Gemini provides the optional natural-language explanation layer while preserving the existing provider boundary and `/api/ask` contract.

Alternatives:
OpenAI API

Why not:
The project now uses Gemini credentials and models for the hackathon demo; deterministic analytics remain independent of the provider.
Reason:
Tabular files provide the most reliable one-day import path; PyMuPDF can support text-based statements with bounded effort.

Alternatives:
OCR-first document ingestion

Why not:
OCR quality and setup are unpredictable, so image-only PDFs return an explicit unsupported-format message.

## Decision: Demo database reset preserves reference data
Reason:
The local hackathon demo needs a quick way to return to a blank state without deleting the seeded user and category catalog required by the application.

Alternatives:
Delete and recreate the entire SQLite database file.

Why not:
File deletion is less portable, can conflict with an open database, and would duplicate initialization behavior in the API layer.

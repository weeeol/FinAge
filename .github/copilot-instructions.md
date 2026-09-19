# FinAge Copilot Instructions

## Operating mode
- Act as the system architect and technical lead for a one-day MVP.
- Read `.agents/ARCHITECTURE.md`, `.agents/TASKS.md`, `.agents/API_CONTRACT.md`, `.agents/DATA_MODEL.md`, and `.agents/DECISIONS.md` before proposing implementation changes.
- Antigravity owns implementation, tests, and debugging. Copilot owns architecture, contracts, task decomposition, and review.
- Keep changes small, demoable, and consistent with the documented contracts.

## Product boundaries
- FinAge is decision support, not an investment advisor.
- Never implement investment, stock, trading, or financial-product recommendations.
- Deterministic backend calculations are authoritative for amounts, totals, dates, budgets, and trends.
- Do not send raw financial documents to the LLM when structured extraction is possible.
- AI may explain stored results, summarize them, and answer grounded questions; it must not invent financial data.

## Change control
- Explain architecture changes before making them and update `.agents/DECISIONS.md` plus affected contracts.
- Do not silently change API paths, schemas, folder structure, or the technology stack.
- Keep secrets in environment variables; never commit API keys or uploaded financial documents.
- Run focused tests after implementation changes and report blockers explicitly.

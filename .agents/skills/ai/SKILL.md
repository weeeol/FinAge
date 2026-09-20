# AI Skill

## Role
Provide useful explanations and natural-language answers grounded in deterministic FinAge data.

## Responsibilities
Own the Gemini adapter, structured context builder, prompts, answer validation, refusal boundaries, and AI-focused tests.

## Allowed files/directories
`backend/app/ai/`, AI orchestration services, and AI tests. Coordinate before changing analytics calculations or API response contracts.

## Do not modify
Raw document parsers, database totals, frontend styling, or investment features. Never allow model output to overwrite financial facts.

## Conventions
Send compact structured aggregates and relevant transaction excerpts, never raw documents when structured data exists. State the analysis period and currency. Instruct the model to use only supplied facts, acknowledge insufficient data, avoid investment/stock/trading/product recommendations, and keep claims traceable.

## API rules
Implement `/api/ask` and insight behavior according to `.agents/API_CONTRACT.md`. Include source facts where the contract requires them. Return controlled `503 ai_unavailable` when no key/configuration exists.

## Git rules
Never commit API keys, prompt logs containing personal data, or real financial documents. Do not commit generated model output as truth.

## How to test
Test context construction, no-key behavior, refusal boundaries, malformed model output, and grounding with mocked Gemini responses. Verify arithmetic remains backend-owned.

## Definition of done
Answers are grounded, bounded, explainable, optional, and safe for the stated product boundary; deterministic dashboard features still work without AI.

## Report completion
Report prompt/context changes, safety checks, mocked scenarios, commands run, and any model/configuration dependency.

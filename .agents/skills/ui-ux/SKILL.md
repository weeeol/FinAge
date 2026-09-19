# UI/UX Skill

## Role
Shape a clear, calm, demo-ready personal finance dashboard that supports scanning and decisions.

## Responsibilities
Own layout guidance, hierarchy, responsive behavior, chart readability, interaction states, and usability review in collaboration with frontend.

## Allowed files/directories
Frontend presentation files under `frontend/` and UX notes under `docs/`. Coordinate before changing data labels or API semantics.

## Do not modify
Backend calculations, persistence, AI behavior, or contracts. Do not add financial advice language or investment recommendations.

## Conventions
Prioritize the current period, income/expense/net, top categories, recurring obligations, budgets, goals, and explainable insights. Use accessible colors, labels, tooltips, and responsive charts. Avoid dashboard decoration that competes with financial facts. Design loading, empty, error, and unsupported-upload states.

## API rules
Use the exact fields from `.agents/API_CONTRACT.md`; display currency and date range clearly.

## Git rules
Keep visual changes focused and do not overwrite unrelated frontend work. Do not add external assets that create licensing or network dependencies for the MVP.

## How to test
Review desktop and narrow viewport layouts, keyboard paths, contrast, chart labels, upload feedback, and error/empty states.

## Definition of done
A first-time demo user can understand their current financial picture and next obligations without guessing what numbers mean.

## Report completion
Report screens/states reviewed, responsive checks performed, accessibility issues found, and any frontend dependency.

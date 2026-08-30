# Judging evidence map

This file gives judges a fast route from each rubric category to working product evidence.

| Category | Product evidence | Code or test evidence |
|---|---|---|
| Full-stack completeness | Deployed login, CSV upload, batch view, exception review, verification, audit, export | `routers/uploads.py`, `routers/workflow.py`, `frontend/src/main.jsx`, `test_app.py` |
| Backend architecture and modeling | Separate raw evidence, normalized loans, validation results, exceptions, AI reviews, decisions, verified snapshots, audits | `services.py`, `database.py`, `schemas/loan.py`, `validators/` |
| Frontend workflow and UX | Role-specific navigation and workspaces, filters, source comparison, clear loading/error states, responsive UI | `Sidebar.jsx`, `AiReviewPanel.jsx`, `main.jsx`, `styles.css` |
| AI feature quality | On-demand exception review, source-aware comparison, batch summary, rule proposal, malformed-output fallback | `workflow.ai_review`, `advanced.py`, `test_ai_controls.py`, `test_ai_evaluation_dataset.py` |
| Agentic coding | Prompts, rejected designs, human corrections, commit references, verification lessons | `docs/ai-development-log.md`, Git history |
| Traceability and auditability | Raw row, normalization changes, validation evidence, source records, decision history, verified hash, audit timeline | `services.import_csv`, `revalidate_loan`, `_verify_loan`, `test_ai_controls.py` |
| Demo quality | One timed script using coordinated primary, servicer, document, and clean files | `docs/demo-script.md`, `data/hackathon_test_*.csv` |

## Test evidence worth showing

- AI generation does not modify the loan.
- AI thinking text is removed from structured output.
- Conflicting sources are shown side by side.
- Human acceptance applies only a stored suggestion for that exception.
- Unsafe edits to raw evidence are rejected.
- Correction requests preserve the loan and block verification.
- Final verification requires clean deterministic validation.
- A loan version receives only one verified snapshot.
- Canonical hashes are stable for equivalent data.
- Dataset-driven malformed AI outputs fail closed.

## Honest limitations

- CSV ingestion is synchronous and designed for the hackathon's small synthetic datasets.
- MongoDB evidence is append-oriented by application convention, not protected by a separate immutable storage service.
- The current AI evaluation tests safety and response contracts; it is not a large expert-labelled accuracy benchmark.
- Demo authentication is not production identity management.
- The React MVP is concentrated in `main.jsx`; production work would split pages, hooks, and feature modules.

## Production roadmap

1. Background ingestion workers, idempotency keys, progress events, retries, and dead-letter handling.
2. SSO/OIDC, generic authentication failures, secret rotation, rate limiting, and security monitoring.
3. Append-only evidence storage, audit hash chaining, retention controls, and database-level permissions.
4. Expert-labelled AI evaluation with field accuracy, unsafe-suggestion rate, reviewer override rate, latency, and cost by model version.
5. Frontend route and feature decomposition, focus management, semantic tables, and automated accessibility testing.

# AI-assisted development log

## Development policy

Codex assisted with architecture, scaffolding, tests, deployment debugging, UI iteration, and documentation. Groq is used inside the product only when a reviewer requests it. AI-generated work was treated as a draft: workflow, security, data lineage, and deployment changes were reviewed by a human before they were retained.

Approximately 60% of first-draft code and documentation was AI-assisted. The human owner selected the requirements, approved changes, performed the live deployment, exercised the workflow, and rejected or corrected unsafe or inaccurate suggestions.

## Evidence cases

### 1. Duplicate evidence was blocked by the first database index

- **Prompt:** “Debug why a CSV containing duplicate loan IDs fails during ingestion instead of generating duplicate exceptions.”
- **AI draft/problem:** The early design treated `(loan_id, upload_id)` as unique. That looked reasonable as a data-integrity rule, but it prevented the system from preserving an intentionally duplicated source row.
- **Human review:** Duplicate input is evidence of a data-quality problem. Rejecting it at the storage layer destroys the evidence needed by the validator.
- **Correction:** Physical CSV rows are unique by `(loan_id, upload_id, source_row_number)`. Duplicate business identifiers are stored and flagged by `DUPLICATE_LOAN_ID`.
- **Verification:** Validator tests assert duplicate behavior, and `database.py` removes the legacy unique index when present.
- **Lesson:** Database integrity constraints must reflect evidence identity, not assume business-data correctness.

### 2. MongoDB truthiness caused startup failure

- **Prompt:** “Find why FastAPI fails when checking the MongoDB database object during startup.”
- **AI draft/problem:** An initial conditional relied on MongoDB database-object truthiness. PyMongo does not support implicit boolean evaluation for this object.
- **Human review:** The connection object must be compared explicitly.
- **Correction:** Startup and dependency code use `is not None`.
- **Verification:** Public health and OpenAPI smoke tests load the application.
- **Lesson:** Generated code still needs library-specific semantic review.

### 3. AI recommendation was separated from human mutation

- **Prompt:** “Add reviewer AI guidance without allowing the model to modify or approve a loan.”
- **AI risk considered:** A convenient first design could apply the model’s proposed value immediately.
- **Human control decision:** AI output must be stored in `ai_reviews`. Only a reviewer decision endpoint may apply an allowed field/value, and acceptance must reference the stored review belonging to that exception.
- **Correction:** `ai_review()` stores recommendations; `decide()` performs explicit acceptance or editing; `_verify_loan()` reruns deterministic validation.
- **Verification:** `test_ai_recommendation_is_logged_but_never_changes_loan`, `test_only_explicit_human_acceptance_applies_the_stored_ai_suggestion`, and unsafe-field tests.
- **Lesson:** Human-in-the-loop control must be enforced by backend state transitions, not just explanatory UI text.

### 4. Model reasoning and malformed output were rejected

- **Prompt:** “Parse Qwen/Groq output safely when it includes thinking tags, markdown fences, or malformed text.”
- **AI draft/problem:** Displaying the raw model response could expose reasoning text and give unstructured content the appearance of an approved recommendation.
- **Human review:** The reviewer UI needs a small, explicit contract rather than arbitrary model text.
- **Correction:** The parser extracts one JSON object into controlled fields. Invalid output fails closed with no suggested field or value.
- **Verification:** `data/ai_evaluation_cases.json`, `test_ai_evaluation_dataset.py`, and parser tests cover thinking text, fenced JSON, empty output, malformed output, and a valid zero value.
- **Lesson:** Model output is untrusted input and needs validation like any external API response.

### 5. Render frontend asset failed after deployment

- **Prompt:** “Diagnose why the deployed static page loads HTML but its hashed JavaScript asset returns missing.”
- **AI investigation:** The deployment and built asset paths were compared rather than changing backend behavior.
- **Human decision:** Use a stable Vite entry filename so the static host and generated HTML agree reliably.
- **Correction:** Vite produces `assets/app.js`; commit `d032da2` records the deployment fix.
- **Verification:** The deployed frontend loaded, login succeeded, and authenticated API data appeared.
- **Lesson:** A successful build is not the same as a successful deployed artifact; the public URL must be exercised.

### 6. API objects appeared as `[object Object]`

- **Prompt:** “Make every API failure readable, including FastAPI validation arrays and nested detail objects.”
- **AI draft/problem:** Passing `payload.detail` directly into `Error` converted object-shaped validation details to `[object Object]`.
- **Human review:** Users need short, actionable messages, while server failures should not leak sensitive internals.
- **Correction:** A shared error extractor handles strings, arrays, nested objects, HTTP statuses, network failures, validation problems, permissions, conflicts, rate limits, and server errors.
- **Verification:** Wrong credentials and short-password paths were manually exercised in the deployed login screen; commits `2a63d75` and `353d18f` record the changes.
- **Lesson:** Error payload shape is part of the frontend/backend contract.

## Representative prompts

1. “Design a FastAPI and MongoDB workflow for a human-in-the-loop loan validation console.”
2. “Generate deterministic tests for balance-over-principal, invalid state, and duplicate-ID validation rules.”
3. “Add a reviewer-decision endpoint that never lets AI update a loan directly.”
4. “Preserve the primary row and secondary-source evidence without silently overwriting values.”
5. “Create a concise five-minute demo showing upload, conflict review, optional AI, verification, hashing, and audit.”
6. “Review the implementation against the official judging criteria and identify evidence gaps.”

## Human review checklist used

- Does the change preserve the original source evidence?
- Can AI mutate or verify a loan without a reviewer?
- Is the action protected by backend role checks?
- Is an audit event written for a material state change?
- Does final verification rerun deterministic validation?
- Does a failure produce a safe and understandable response?
- Is the limitation documented honestly?

## Current limitations

- Prompt and output examples are representative development evidence, not exported transcripts from every coding session.
- The AI evaluation measures response-contract safety, not statistically significant domain accuracy.
- Production work would add expert-labelled evaluation data, automated deployment checks, rate limiting, private identity management, and model-version monitoring.

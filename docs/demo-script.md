# Five-minute hackathon demo

Use only the coordinated `hackathon_test_*` files below. Reset the demo database before the presentation so counts and statuses are predictable.

## Before the timer starts

- Open the deployed frontend and backend `/health` page once to avoid a free-tier cold start.
- Confirm Groq shows as connected. The deterministic workflow still works if Groq is unavailable.
- Keep MongoDB Atlas closed unless a judge asks to inspect persistence.
- Sign out so the demo begins at the role-aware login page.

## 0:00-0:35 - Problem and architecture

Say: “Loan data arrives from different systems with missing, inconsistent, or conflicting values. We preserve every source, normalize formatting, run deterministic rules, route exceptions to a human reviewer, and publish only traceable verified records. AI assists but never approves or changes a loan.”

Show the three demo roles and sign in as `operator@demo.local`.

## 0:35-1:35 - Operator ingestion

1. Upload `data/hackathon_test_loan_tape.csv` as **Loan tape**.
2. Show the upload summary and one normalized batch row.
3. Explain that `raw_csv_row` remains evidence and normalization has its own change metadata.
4. Upload `data/hackathon_test_servicer_update.csv` as **Servicer update**.
5. Upload `data/hackathon_test_document_manifest.csv` as **Document manifest**.

Say: “Secondary sources are stored separately. They never silently overwrite the primary tape.”

## 1:35-3:15 - Reviewer conflict and AI control

1. Sign out and sign in as `reviewer@demo.local`.
2. Open **Exceptions** and search for `LN-30002`.
3. Claim a conflicting-source exception.
4. Expand source lineage and compare the primary, servicer, and document values.
5. Request **Groq AI Review**.
6. Point out the stored model, prompt summary, source comparison, recommendation, and confidence.
7. Say: “Nothing has changed yet. The recommendation is separate from the canonical loan.”
8. Add a reviewer comment and choose an appropriate human action: edit, reject, or request correction.
9. Explain that an edit triggers deterministic revalidation and a new audit event.

If Groq is unavailable, show the AI status and say: “AI is optional. The rule engine, exception queue, human decision, verification, and audit trail continue to work.”

## 3:15-4:05 - Clean verification

1. Sign in as the operator and upload `data/hackathon_test_clean_loans.csv` as **Loan tape** if it is not already loaded.
2. Return as the reviewer, open **Batches**, select the clean batch, and verify `LN-40001`.
3. Explain that final verification reruns every deterministic rule.
4. Point out that only one verified snapshot can be created for that loan version.

## 4:05-4:45 - Consumer trust output

1. Sign in as `consumer@demo.local`.
2. Open **Verified**.
3. Show `LN-40001`, its quality score, SHA-256 hash, verification time, and audit timeline.
4. Use the CSV export action.

Say: “The consumer receives trusted output but cannot upload, correct, or self-approve data.”

## 4:45-5:00 - Close

Say: “Our differentiator is controlled trust: preserved source evidence, deterministic validation, optional AI explanation, accountable human decisions, and a hash-backed verified record.”

## Judge-question backup

- **Why MongoDB?** Flexible preservation of heterogeneous raw source rows and lineage metadata; verified output can later be published to a relational analytical store.
- **Can AI change a loan?** No. Backend tests prove generation does not mutate the loan; a reviewer must explicitly accept or edit.
- **What if Groq fails?** Deterministic validation and all human workflows remain available.
- **How would this scale?** Move synchronous ingestion to a queue/worker, add progress polling, retries, idempotency, and object storage.
- **Production limitations?** Private SSO, generic login errors, secret rotation, rate limits, stronger append-only evidence controls, monitoring, and a larger labelled AI evaluation set.

Never use the shared demo password for real users or production data.

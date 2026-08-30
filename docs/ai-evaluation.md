# AI quality and safety evaluation

## What is measured

The repeatable evaluation dataset is `data/ai_evaluation_cases.json`. It contains saved representative provider outputs for valid recommendations, zero-valued corrections, reasoning-text removal, fenced JSON, malformed output, and empty output.

`backend/tests/test_ai_evaluation_dataset.py` runs every saved output through the same parser used by the reviewer workflow and verifies that:

- structured recommendations retain the expected field, value, and confidence;
- a valid numeric zero is preserved;
- private reasoning text is not shown;
- markdown fences do not break the structured response;
- malformed or empty output fails closed with no editable field or value; and
- fallback guidance explicitly says that no loan data was changed.

## Human-control tests

`backend/tests/test_ai_controls.py` separately verifies that:

- generating an AI review never changes the loan;
- source evidence is stored side by side for conflict reviews;
- only explicit human acceptance applies a stored suggestion;
- an acceptance must reference an AI review belonging to that exception;
- raw evidence fields cannot be edited;
- requesting a correction preserves the loan and blocks verification;
- resolved exceptions cannot receive another AI request or decision; and
- a verified record requires clean final deterministic validation.

## Honest interpretation

These tests evaluate the product contract and failure behavior, not the general intelligence of the Groq model. They do not claim a statistically significant recommendation-accuracy score. A production evaluation would add a domain-expert-labelled set of at least 100 exceptions, compare model suggestions with reviewer decisions, measure field/value accuracy and unsafe-suggestion rate, and monitor those metrics by model version.

## Running the evaluation

From `backend/`:

```powershell
python -m pytest tests/test_ai_evaluation_dataset.py tests/test_ai_controls.py -q
```

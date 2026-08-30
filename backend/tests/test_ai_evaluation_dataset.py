import json
from pathlib import Path

from app.routers.workflow import _parse_ai_review_response


CASES_PATH = Path(__file__).resolve().parents[2] / "data" / "ai_evaluation_cases.json"


def test_saved_ai_outputs_meet_the_reviewer_contract():
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    assert len(cases) >= 5

    for case in cases:
        result = _parse_ai_review_response(case["model_output"], case["exception"])
        expected = case["expected"]
        assert result["suggested_field"] == expected["suggested_field"], case["id"]
        assert result["suggested_value"] == expected["suggested_value"], case["id"]
        assert result["confidence"] == expected["confidence"], case["id"]
        if expected.get("forbidden_text"):
            assert expected["forbidden_text"].lower() not in str(result).lower(), case["id"]


def test_malformed_ai_outputs_never_create_an_editable_suggestion():
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    malformed = [case for case in cases if "fails-closed" in case["id"]]
    assert malformed
    for case in malformed:
        result = _parse_ai_review_response(case["model_output"], case["exception"])
        assert result["suggested_field"] is None
        assert result["suggested_value"] is None
        assert "no loan data was changed" in result["reasoning"].lower()

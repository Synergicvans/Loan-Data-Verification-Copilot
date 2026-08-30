import sys
from types import SimpleNamespace

from app.groq_support import groq_failure, probe_groq


def provider_error(name, status_code):
    error_type = type(name, (Exception,), {})
    error = error_type("provider detail must not leak")
    error.status_code = status_code
    return error


def test_groq_authentication_error_is_actionable_and_safe():
    result = groq_failure(provider_error("AuthenticationError", 401))
    assert result.status_code == 503
    assert "GROQ_API_KEY" in result.detail
    assert "provider detail" not in result.detail


def test_groq_rate_limit_uses_retryable_http_status():
    result = groq_failure(provider_error("RateLimitError", 429))
    assert result.status_code == 429
    assert "rate limit" in result.detail.lower()


def test_groq_model_errors_identify_configuration_without_leaking_provider_text():
    result = groq_failure(provider_error("NotFoundError", 404))
    assert result.status_code == 503
    assert "GROQ_MODEL" in result.detail
    assert "provider detail" not in result.detail


def test_probe_groq_accepts_slash_model_ids(monkeypatch):
    class FakeModels:
        def list(self):
            return SimpleNamespace(data=[SimpleNamespace(id="openai/gpt-oss-20b")])

    class FakeGroq:
        def __init__(self, api_key):
            self.models = FakeModels()

    monkeypatch.setitem(sys.modules, "groq", SimpleNamespace(Groq=FakeGroq))

    assert probe_groq("test-key", "openai/gpt-oss-20b") == {
        "enabled": True,
        "reason": None,
    }


def test_probe_groq_reports_project_model_mismatch(monkeypatch):
    class FakeModels:
        def list(self):
            return SimpleNamespace(data=[SimpleNamespace(id="qwen/qwen3.6-27b")])

    class FakeGroq:
        def __init__(self, api_key):
            self.models = FakeModels()

    monkeypatch.setitem(sys.modules, "groq", SimpleNamespace(Groq=FakeGroq))

    result = probe_groq("test-key", "openai/gpt-oss-20b")
    assert result["enabled"] is False
    assert "GROQ_MODEL" in result["reason"]

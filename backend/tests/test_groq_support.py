from types import SimpleNamespace

from app.groq_support import groq_failure


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

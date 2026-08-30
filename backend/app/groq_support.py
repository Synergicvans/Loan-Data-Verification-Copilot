from fastapi import HTTPException


def groq_failure(exc: Exception) -> HTTPException:
    """Translate provider failures into safe, actionable API errors."""
    name = type(exc).__name__.lower()
    status = getattr(exc, "status_code", None)
    if status == 401 or "authentication" in name:
        return HTTPException(503, "Groq rejected the API key. Update GROQ_API_KEY in Render and redeploy the backend.")
    if status == 403 or "permission" in name:
        return HTTPException(503, "This Groq project cannot use the configured model. Check GROQ_MODEL or project access.")
    if status == 404 or "notfound" in name:
        return HTTPException(503, "The configured Groq model was not found. Check GROQ_MODEL in Render.")
    if status == 429 or "ratelimit" in name:
        return HTTPException(429, "Groq rate limit or quota reached. Wait briefly, then try again.")
    if "timeout" in name or "connection" in name:
        return HTTPException(503, "Groq is temporarily unreachable. Please try again shortly.")
    return HTTPException(502, "Groq could not generate a review. Check the backend logs and Groq project status.")


def probe_groq(api_key: str | None, model: str) -> dict:
    if not api_key:
        return {"enabled": False, "reason": "GROQ_API_KEY is not configured."}
    try:
        from groq import Groq

        # Listing models avoids path-encoding problems in the retrieve endpoint
        # for IDs containing a slash (for example ``openai/gpt-oss-20b``).
        available = {item.id for item in Groq(api_key=api_key).models.list().data}
        if model not in available:
            return {
                "enabled": False,
                "reason": "The configured Groq model is not available to this project. Check GROQ_MODEL in Render.",
            }
        return {"enabled": True, "reason": None}
    except Exception as exc:
        failure = groq_failure(exc)
        return {"enabled": False, "reason": failure.detail}

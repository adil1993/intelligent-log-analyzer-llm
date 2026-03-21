
import json
from pydantic import ValidationError
from .log_parser import parse_logs
from .llm_service import analyze_with_llm
from ..config import settings
from ..schemas import IncidentReport
from datetime import datetime
import uuid

async def analyze_logs(raw_logs: str):
    parsed = parse_logs(raw_logs, settings.MAX_LOG_LINES)
    log_summary = parsed["log_summary"]
    metrics = parsed["metrics"]

    raw_response = await analyze_with_llm(log_summary)

    try:
        cleaned = raw_response.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("```")[1]

        data = json.loads(cleaned)
        validated = IncidentReport(**data)

        return {
            "incident": validated.dict(),
            "metrics": metrics,
            "request_id": str(uuid.uuid4()),
            "analyzed_at": datetime.utcnow().isoformat()
        }

    except (json.JSONDecodeError, ValidationError):
        return {
            "error": "Invalid AI response format",
            "raw_output": raw_response,
            "metrics": metrics
        }

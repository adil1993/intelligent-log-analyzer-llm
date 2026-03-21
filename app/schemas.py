
from pydantic import BaseModel
from typing import List

class IncidentReport(BaseModel):
    primary_issue: str
    severity: str
    probable_root_cause: str
    recommended_actions: List[str]
    confidence_score: float

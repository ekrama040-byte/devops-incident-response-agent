import operator
from typing import Annotated, List, Optional, TypedDict
from langchain_core.messages import BaseMessage

class IncidentState(TypedDict):
    alert_id: str
    service: str
    message: str
    timestamp: str
    severity: str
    messages: Annotated[List[BaseMessage], operator.add]
    investigation_findings: Annotated[List[str], operator.add]
    tools_used: Annotated[List[str], operator.add]
    root_cause: Optional[str]
    confidence_score: Optional[float]
    review_notes: Optional[str]
    is_root_cause_valid: Optional[bool]
    proposed_action: Optional[str]
    fix_risk: Optional[str]
    human_decision: Optional[str]
    fix_result: Optional[str]
    final_report: Optional[str]
    retry_count: Optional[int]
    notification_status: Optional[str]
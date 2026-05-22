"""
Pydantic Models - Diagnostics
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from enum import Enum


class Severity(str, Enum):
    """Niveaux de sévérité"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"


class DiagnosticIssue(BaseModel):
    """Problème diagnostiqué"""
    id: str
    title: str
    message: str
    severity: Severity
    category: str
    campaign_id: Optional[str] = None
    campaign_name: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    recommendation: Optional[str] = None
    impact: Optional[str] = None
    created_at: str


class DiagnosticSummary(BaseModel):
    """Résumé des diagnostics"""
    total: int = 0
    by_severity: Dict[str, int] = {
        "critical": 0,
        "high": 0,
        "medium": 0,
        "low": 0
    }
    by_category: Dict[str, int] = {}


class DiagnosticResponse(BaseModel):
    """Response pour diagnostics"""
    issues: List[DiagnosticIssue]
    summary: DiagnosticSummary

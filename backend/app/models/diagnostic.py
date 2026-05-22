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
    title: str
    message: str
    severity: Severity
    category: str
    campaign_id: Optional[str] = None
    campaign_name: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    action: Optional[str] = None


class DiagnosticResponse(BaseModel):
    """Response pour diagnostics"""
    issues: List[DiagnosticIssue]
    total: int


class DiagnosticSummary(BaseModel):
    """Résumé des diagnostics"""
    critical: int = 0
    high: int = 0
    medium: int = 0
    low: int = 0
    total: int = 0

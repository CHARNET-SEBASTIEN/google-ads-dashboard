"""
API Routes - Diagnostics
Analyse automatique et recommandations
"""

from fastapi import APIRouter, Query
from typing import List, Optional

from app.models.diagnostic import (
    DiagnosticResponse,
    DiagnosticSummary,
    Severity
)
from app.services.data_loader_service import data_loader_service
from app.services.diagnostics_service import diagnostics_service


router = APIRouter()


@router.get("", response_model=DiagnosticResponse)
async def run_diagnostics(
    campaign_ids: Optional[List[str]] = Query(None),
    severity: Optional[List[str]] = Query(None),
    category: Optional[List[str]] = Query(None)
):
    """
    Lance l'analyse diagnostique sur les campagnes

    Args:
        campaign_ids: Analyser uniquement ces campagnes
        severity: Filtrer par sévérité (CRITICAL, HIGH, MEDIUM, LOW)
        category: Filtrer par catégorie

    Returns:
        Liste des problèmes détectés
    """
    # Charger les campagnes
    campaigns = data_loader_service.get_campaigns()

    # Filtrer par campaign_ids si fourni
    if campaign_ids:
        campaigns = [c for c in campaigns if str(c.get('id')) in campaign_ids]

    # Convertir severity strings en Enum
    severity_filter = None
    if severity:
        severity_filter = [Severity(s.upper()) for s in severity]

    # Analyser toutes les campagnes
    issues = diagnostics_service.analyze_all_campaigns(
        campaigns=campaigns,
        severity_filter=severity_filter,
        category_filter=category
    )

    return DiagnosticResponse(issues=issues, total=len(issues))


@router.get("/summary", response_model=DiagnosticSummary)
async def diagnostics_summary(
    campaign_ids: Optional[List[str]] = Query(None)
):
    """
    Résumé des diagnostics (count par sévérité)

    Args:
        campaign_ids: Analyser uniquement ces campagnes

    Returns:
        Statistiques des problèmes par sévérité
    """
    # Charger les campagnes
    campaigns = data_loader_service.get_campaigns()

    # Filtrer par campaign_ids si fourni
    if campaign_ids:
        campaigns = [c for c in campaigns if str(c.get('id')) in campaign_ids]

    # Analyser
    issues = diagnostics_service.analyze_all_campaigns(campaigns=campaigns)

    # Compter par sévérité
    summary = DiagnosticSummary()

    for issue in issues:
        summary.total += 1

        if issue.severity == Severity.CRITICAL:
            summary.critical += 1
        elif issue.severity == Severity.HIGH:
            summary.high += 1
        elif issue.severity == Severity.MEDIUM:
            summary.medium += 1
        elif issue.severity == Severity.LOW:
            summary.low += 1

    return summary


@router.get("/rules")
async def diagnostics_rules():
    """
    Liste des règles de diagnostic disponibles

    Returns:
        Liste des règles
    """
    rules = [
        {
            "id": "campaign_paused",
            "name": "Campagne en pause",
            "category": "Configuration",
            "severity": "MEDIUM"
        },
        {
            "id": "budget_limited",
            "name": "Budget limité",
            "category": "Budget",
            "severity": "HIGH"
        },
        {
            "id": "no_conversions",
            "name": "Aucune conversion",
            "category": "Performances",
            "severity": "CRITICAL"
        },
        {
            "id": "low_ctr",
            "name": "CTR très faible",
            "category": "Performances",
            "severity": "HIGH"
        },
        {
            "id": "high_cpa",
            "name": "Coût par conversion élevé",
            "category": "Performances",
            "severity": "MEDIUM"
        },
        {
            "id": "low_impressions",
            "name": "Volume d'impressions faible",
            "category": "Performances",
            "severity": "MEDIUM"
        },
        {
            "id": "low_conversion_rate",
            "name": "Taux de conversion faible",
            "category": "Performances",
            "severity": "MEDIUM"
        }
    ]

    return {"rules": rules, "total": len(rules)}

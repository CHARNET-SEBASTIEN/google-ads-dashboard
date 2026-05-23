"""
API Routes - Campaigns
Gestion des campagnes Google Ads
"""

from fastapi import APIRouter, Query, HTTPException, status
from typing import List, Optional

from app.models.campaign import (
    CampaignListResponse,
    Campaign,
    KeywordListResponse,
    Keyword,
    AdListResponse,
    Ad,
    PerformanceResponse,
    Performance,
    DevicePerformance,
    DevicePerformanceResponse,
    DayOfWeekPerformance,
    DayOfWeekPerformanceResponse
)
from app.services.data_loader_service import data_loader_service


router = APIRouter()


@router.get("", response_model=CampaignListResponse)
async def get_campaigns(
    status_filter: Optional[List[str]] = Query(None, alias="status"),
    search: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    """
    Liste toutes les campagnes avec filtres

    Args:
        status_filter: Filtrer par statut (ENABLED, PAUSED, REMOVED)
        search: Recherche par nom
        limit: Nombre max de résultats
        offset: Offset pagination

    Returns:
        Liste de campagnes avec total
    """
    campaigns_data = data_loader_service.get_campaigns()

    # Filtrer par statut
    if status_filter:
        campaigns_data = [c for c in campaigns_data if c.get('status') in status_filter]

    # Filtrer par recherche
    if search:
        search_lower = search.lower()
        campaigns_data = [
            c for c in campaigns_data
            if search_lower in c.get('name', '').lower()
        ]

    total = len(campaigns_data)

    # Pagination
    campaigns_data = campaigns_data[offset:offset + limit]

    # Convertir en modèles Pydantic
    campaigns = [
        Campaign(
            id=str(c.get('id')),
            name=c.get('name', 'Unknown'),
            status=c.get('status', 'UNKNOWN'),
            budget=c.get('budget'),
            impressions=c.get('impressions', 0),
            clicks=c.get('clicks', 0),
            ctr=c.get('ctr', 0.0),
            cpc=c.get('averageCpc', 0.0),
            cost=c.get('cost', 0.0),
            conversions=c.get('conversions', 0.0)
        )
        for c in campaigns_data
    ]

    return CampaignListResponse(campaigns=campaigns, total=total)


@router.get("/{campaign_id}", response_model=Campaign)
async def get_campaign(campaign_id: str):
    """
    Détail d'une campagne

    Args:
        campaign_id: ID de la campagne

    Returns:
        Détails de la campagne
    """
    campaigns_data = data_loader_service.get_campaigns()

    # Trouver la campagne
    campaign_data = next(
        (c for c in campaigns_data if str(c.get('id')) == campaign_id),
        None
    )

    if not campaign_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Campaign {campaign_id} not found"
        )

    return Campaign(
        id=str(campaign_data.get('id')),
        name=campaign_data.get('name', 'Unknown'),
        status=campaign_data.get('status', 'UNKNOWN'),
        budget=campaign_data.get('budget'),
        impressions=campaign_data.get('impressions', 0),
        clicks=campaign_data.get('clicks', 0),
        ctr=campaign_data.get('ctr', 0.0),
        cpc=campaign_data.get('averageCpc', 0.0),
        cost=campaign_data.get('cost', 0.0),
        conversions=campaign_data.get('conversions', 0.0)
    )


@router.get("/{campaign_id}/keywords", response_model=KeywordListResponse)
async def get_campaign_keywords(
    campaign_id: str,
    match_type: Optional[List[str]] = Query(None),
    search: Optional[str] = None,
    min_clicks: int = 0
):
    """
    Mots-clés d'une campagne

    Args:
        campaign_id: ID de la campagne
        match_type: Filtrer par type de correspondance
        search: Recherche dans le texte
        min_clicks: Minimum de clics

    Returns:
        Liste de mots-clés
    """
    keywords_data = data_loader_service.get_keywords(campaign_id=campaign_id)

    # Filtrer par match type
    if match_type:
        keywords_data = [kw for kw in keywords_data if kw.get('matchType') in match_type]

    # Filtrer par recherche
    if search:
        search_lower = search.lower()
        keywords_data = [
            kw for kw in keywords_data
            if search_lower in kw.get('text', kw.get('keywordText', '')).lower()
        ]

    # Filtrer par min_clicks
    if min_clicks > 0:
        keywords_data = [kw for kw in keywords_data if kw.get('clicks', 0) >= min_clicks]

    total = len(keywords_data)

    # Convertir en modèles
    keywords = [
        Keyword(
            id=str(kw.get('id')),
            campaign_id=str(kw.get('campaignId')),
            text=kw.get('text', kw.get('keywordText', '')),  # Support both field names
            match_type=kw.get('matchType', 'UNKNOWN'),
            status=kw.get('status', 'UNKNOWN'),
            impressions=kw.get('impressions', 0),
            clicks=kw.get('clicks', 0),
            ctr=kw.get('ctr', 0.0),
            cpc=kw.get('averageCpc', 0.0),
            cost=kw.get('cost', 0.0)
        )
        for kw in keywords_data
    ]

    return KeywordListResponse(keywords=keywords, total=total)


@router.get("/{campaign_id}/ads", response_model=AdListResponse)
async def get_campaign_ads(campaign_id: str):
    """
    Annonces d'une campagne

    Args:
        campaign_id: ID de la campagne

    Returns:
        Liste d'annonces
    """
    ads_data = data_loader_service.get_ads(campaign_id=campaign_id)

    total = len(ads_data)

    # Convertir en modèles
    ads = [
        Ad(
            id=str(ad.get('id')),
            campaign_id=str(ad.get('campaignId')),
            type=ad.get('type', 'UNKNOWN'),
            status=ad.get('status', 'UNKNOWN'),
            headline1=ad.get('headline1'),
            headline2=ad.get('headline2'),
            description=ad.get('description'),
            impressions=ad.get('impressions', 0),
            clicks=ad.get('clicks', 0)
        )
        for ad in ads_data
    ]

    return AdListResponse(ads=ads, total=total)


@router.get("/{campaign_id}/performance", response_model=PerformanceResponse)
async def get_campaign_performance(
    campaign_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    granularity: str = "DAY"
):
    """
    Performance d'une campagne (séries temporelles)

    Args:
        campaign_id: ID de la campagne
        start_date: Date de début (YYYY-MM-DD)
        end_date: Date de fin (YYYY-MM-DD)
        granularity: Granularité (DAY, WEEK, MONTH)

    Returns:
        Séries temporelles de performance
    """
    performance_data = data_loader_service.get_performance(campaign_id=campaign_id)

    # Filtrer par dates si fournies
    # TODO: Implémenter filtrage par dates
    # TODO: Implémenter agrégation par granularity

    # Convertir en modèles
    performance = [
        Performance(
            date=p.get('date', ''),
            impressions=p.get('impressions', 0),
            clicks=p.get('clicks', 0),
            cost=p.get('cost', 0.0),
            conversions=p.get('conversions', 0.0)
        )
        for p in performance_data
    ]

    return PerformanceResponse(performance=performance)


@router.get("/{campaign_id}/performance/device", response_model=DevicePerformanceResponse)
async def get_campaign_performance_by_device(campaign_id: str):
    """
    Performance d'une campagne par appareil

    Args:
        campaign_id: ID de la campagne

    Returns:
        Performance segmentée par appareil (Desktop, Mobile, Tablet)
    """
    device_data = data_loader_service.get_performance_by_device(campaign_id=campaign_id)

    devices = [
        DevicePerformance(
            campaign_id=str(d.get('campaignId', '')),
            campaign_name=d.get('campaignName', ''),
            device=d.get('device', ''),
            impressions=d.get('impressions', 0),
            clicks=d.get('clicks', 0),
            cost=d.get('cost', 0.0),
            conversions=d.get('conversions', 0.0),
            ctr=d.get('ctr', 0.0),
            cpc=d.get('averageCpc', 0.0)
        )
        for d in device_data
    ]

    return DevicePerformanceResponse(devices=devices)


@router.get("/{campaign_id}/performance/day-of-week", response_model=DayOfWeekPerformanceResponse)
async def get_campaign_performance_by_day_of_week(campaign_id: str):
    """
    Performance d'une campagne par jour de la semaine

    Args:
        campaign_id: ID de la campagne

    Returns:
        Performance agrégée par jour de la semaine (Lundi-Dimanche)
    """
    day_data = data_loader_service.get_performance_by_day_of_week(campaign_id=campaign_id)

    days = [
        DayOfWeekPerformance(
            day_of_week=d.get('day_of_week', ''),
            day_number=d.get('day_number', 0),
            impressions=d.get('impressions', 0),
            clicks=d.get('clicks', 0),
            cost=d.get('cost', 0.0),
            conversions=d.get('conversions', 0.0),
            ctr=d.get('ctr', 0.0),
            cpc=d.get('cpc', 0.0)
        )
        for d in day_data
    ]

    return DayOfWeekPerformanceResponse(days=days)

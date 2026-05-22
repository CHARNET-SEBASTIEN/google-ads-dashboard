"""
API Routes - Search Terms
Termes de recherche utilisateurs
"""

from fastapi import APIRouter, Query
from typing import List, Optional

from app.models.search_term import (
    SearchTermListResponse,
    SearchTerm,
    SuspectTermsResponse
)
from app.services.data_loader_service import data_loader_service


router = APIRouter()


# Mots suspects à détecter
SUSPECT_KEYWORDS = [
    'gratuit', 'free', 'emploi', 'job', 'stage', 'télécharger',
    'download', 'crack', 'torrent', 'streaming', 'formation',
    'cours', 'tutorial', 'pdf', 'documentation'
]


def is_suspect_query(query: str) -> bool:
    """Vérifie si un terme de recherche est suspect"""
    query_lower = query.lower()
    return any(suspect in query_lower for suspect in SUSPECT_KEYWORDS)


@router.get("", response_model=SearchTermListResponse)
async def get_search_terms(
    campaign_ids: Optional[List[str]] = Query(None),
    min_clicks: int = 0,
    search: Optional[str] = None,
    limit: int = 100,
    offset: int = 0
):
    """
    Liste des termes de recherche avec filtres

    Args:
        campaign_ids: Filtrer par IDs de campagnes
        min_clicks: Minimum de clics
        search: Recherche dans le texte
        limit: Nombre max de résultats
        offset: Offset pagination

    Returns:
        Liste de termes de recherche
    """
    # Charger tous les termes de recherche
    all_search_terms = data_loader_service.get_search_terms()

    # Filtrer par campagnes
    if campaign_ids:
        all_search_terms = [
            st for st in all_search_terms
            if str(st.get('campaignId')) in campaign_ids
        ]

    # Filtrer par min_clicks
    if min_clicks > 0:
        all_search_terms = [
            st for st in all_search_terms
            if st.get('clicks', 0) >= min_clicks
        ]

    # Filtrer par recherche
    if search:
        search_lower = search.lower()
        all_search_terms = [
            st for st in all_search_terms
            if search_lower in st.get('query', '').lower()
        ]

    total = len(all_search_terms)

    # Pagination
    all_search_terms = all_search_terms[offset:offset + limit]

    # Convertir en modèles Pydantic
    search_terms = [
        SearchTerm(
            id=str(st.get('id', '')),
            campaign_id=str(st.get('campaignId', '')),
            campaign_name=st.get('campaignName'),
            ad_group_id=str(st.get('adGroupId', '')),
            keyword_id=str(st.get('keywordId', '')),
            query=st.get('query', ''),
            impressions=st.get('impressions', 0),
            clicks=st.get('clicks', 0),
            ctr=st.get('ctr', 0.0),
            cost=st.get('cost', 0.0),
            conversions=st.get('conversions', 0.0),
            is_suspect=is_suspect_query(st.get('query', ''))
        )
        for st in all_search_terms
    ]

    return SearchTermListResponse(search_terms=search_terms, total=total)


@router.get("/suspects", response_model=SuspectTermsResponse)
async def get_suspect_terms(
    campaign_ids: Optional[List[str]] = Query(None),
    limit: int = 100
):
    """
    Termes suspects (gratuit, emploi, etc.)

    Args:
        campaign_ids: Filtrer par IDs de campagnes
        limit: Nombre max de résultats

    Returns:
        Liste de termes suspects
    """
    # Charger tous les termes
    all_search_terms = data_loader_service.get_search_terms()

    # Filtrer par campagnes
    if campaign_ids:
        all_search_terms = [
            st for st in all_search_terms
            if str(st.get('campaignId')) in campaign_ids
        ]

    # Filtrer les termes suspects
    suspects_data = [
        st for st in all_search_terms
        if is_suspect_query(st.get('query', ''))
    ]

    total = len(suspects_data)

    # Limiter
    suspects_data = suspects_data[:limit]

    # Convertir en modèles
    suspects = [
        SearchTerm(
            id=str(st.get('id', '')),
            campaign_id=str(st.get('campaignId', '')),
            campaign_name=st.get('campaignName'),
            ad_group_id=str(st.get('adGroupId', '')),
            keyword_id=str(st.get('keywordId', '')),
            query=st.get('query', ''),
            impressions=st.get('impressions', 0),
            clicks=st.get('clicks', 0),
            ctr=st.get('ctr', 0.0),
            cost=st.get('cost', 0.0),
            conversions=st.get('conversions', 0.0),
            is_suspect=True
        )
        for st in suspects_data
    ]

    return SuspectTermsResponse(suspects=suspects, total=total)


@router.post("/export")
async def export_search_terms():
    """
    Export des termes de recherche en CSV

    Returns:
        Fichier CSV
    """
    # TODO: Implémenter export CSV
    from fastapi.responses import PlainTextResponse

    search_terms = data_loader_service.get_search_terms()

    # Créer CSV simple
    csv_lines = ["Campaign ID,Query,Impressions,Clicks,CTR,Cost,Conversions"]

    for st in search_terms:
        line = f"{st.get('campaignId')},{st.get('query')},{st.get('impressions')},{st.get('clicks')},{st.get('ctr')},{st.get('cost')},{st.get('conversions')}"
        csv_lines.append(line)

    csv_content = "\n".join(csv_lines)

    return PlainTextResponse(
        content=csv_content,
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=search_terms.csv"}
    )

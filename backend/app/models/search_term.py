"""
Pydantic Models - Search Terms
"""

from typing import Optional, List
from pydantic import BaseModel


class SearchTerm(BaseModel):
    """Modèle de terme de recherche"""
    id: Optional[str] = None
    campaign_id: str
    campaign_name: Optional[str] = None
    ad_group_id: Optional[str] = None
    keyword_id: Optional[str] = None
    query: str
    impressions: int = 0
    clicks: int = 0
    ctr: float = 0.0
    cost: float = 0.0
    conversions: float = 0.0
    is_suspect: bool = False


class SearchTermListResponse(BaseModel):
    """Response pour liste de termes de recherche"""
    search_terms: List[SearchTerm]
    total: int


class SuspectTermsResponse(BaseModel):
    """Response pour termes suspects"""
    suspects: List[SearchTerm]
    total: int

"""
Pydantic Models - Campaigns
"""

from typing import Optional, List
from pydantic import BaseModel


class Campaign(BaseModel):
    """Modèle de campagne"""
    id: str
    name: str
    status: str
    budget: Optional[float] = None
    impressions: Optional[int] = 0
    clicks: Optional[int] = 0
    ctr: Optional[float] = 0.0
    cpc: Optional[float] = 0.0
    cost: Optional[float] = 0.0
    conversions: Optional[float] = 0.0


class Keyword(BaseModel):
    """Modèle de mot-clé"""
    id: str
    campaign_id: str
    text: str
    match_type: str
    status: str
    impressions: Optional[int] = 0
    clicks: Optional[int] = 0
    ctr: Optional[float] = 0.0
    cpc: Optional[float] = 0.0
    cost: Optional[float] = 0.0


class Ad(BaseModel):
    """Modèle d'annonce"""
    id: str
    campaign_id: str
    type: str
    status: str
    headline1: Optional[str] = None
    headline2: Optional[str] = None
    description: Optional[str] = None
    impressions: Optional[int] = 0
    clicks: Optional[int] = 0


class Performance(BaseModel):
    """Modèle de performance"""
    date: str
    impressions: int
    clicks: int
    cost: float
    conversions: Optional[float] = 0.0


class CampaignListResponse(BaseModel):
    """Response pour liste de campagnes"""
    campaigns: List[Campaign]
    total: int


class KeywordListResponse(BaseModel):
    """Response pour liste de mots-clés"""
    keywords: List[Keyword]
    total: int


class AdListResponse(BaseModel):
    """Response pour liste d'annonces"""
    ads: List[Ad]
    total: int


class PerformanceResponse(BaseModel):
    """Response pour performance"""
    performance: List[Performance]


class DevicePerformance(BaseModel):
    """Performance par appareil"""
    campaign_id: str
    campaign_name: str
    device: str
    impressions: int
    clicks: int
    cost: float
    conversions: float
    ctr: float
    cpc: float


class DayOfWeekPerformance(BaseModel):
    """Performance par jour de semaine"""
    day_of_week: str
    day_number: int
    impressions: int
    clicks: int
    cost: float
    conversions: float
    ctr: float
    cpc: float


class HourOfDayPerformance(BaseModel):
    """Performance par heure"""
    hour: int
    impressions: int
    clicks: int
    cost: float
    conversions: float
    ctr: float
    cpc: float


class DevicePerformanceResponse(BaseModel):
    """Response performance par appareil"""
    devices: List[DevicePerformance]


class DayOfWeekPerformanceResponse(BaseModel):
    """Response performance par jour"""
    days: List[DayOfWeekPerformance]


class HourOfDayPerformanceResponse(BaseModel):
    """Response performance par heure"""
    hours: List[HourOfDayPerformance]
